import hashlib
import json
from pathlib import Path
from sqlalchemy import text
from services.shared.db import engine

ROOT = Path(".")
def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    sources = json.loads((ROOT / "public/data/territorial/catalog/sources.json").read_text(encoding="utf-8"))
    manifests = sorted((ROOT / "data/snapshots").glob("*/*/manifest.json"))
    territories = json.loads((ROOT / "public/data/territorial/geography/departments.geojson").read_text(encoding="utf-8"))
    products = sorted((ROOT / "public/data/territorial/indicators").glob("*.json"))
    with engine.begin() as db:
        for item in sources if isinstance(sources, list) else sources.get("sources", []):
            key = str(item.get("id") or item.get("source_id"))
            db.execute(text("""INSERT INTO sources(source_key,name,metadata,quality_status)
              VALUES(:key,:name,CAST(:meta AS jsonb),'valid')
              ON CONFLICT(source_key) DO UPDATE SET metadata=excluded.metadata,updated_at=now()"""),
              {"key": key, "name": item.get("name") or key, "meta": json.dumps(item)})
        for path in manifests:
            manifest = json.loads(path.read_text(encoding="utf-8"))
            source_key = str(manifest.get("source_id") or path.parts[-3])
            source_id = db.execute(text("SELECT id FROM sources WHERE source_key=:key"), {"key": source_key}).scalar()
            if not source_id:
                source_id = db.execute(text("INSERT INTO sources(source_key,name) VALUES(:k,:k) RETURNING id"), {"k": source_key}).scalar()
            content_hash = manifest.get("sha256") or manifest.get("combined_sha256") or digest(path)
            schema_hash = hashlib.sha256(json.dumps(sorted(manifest.keys())).encode()).hexdigest()
            valid = str(manifest.get("quality_status", manifest.get("status", "valid"))).lower() not in {"invalid", "failed"}
            db.execute(text("""INSERT INTO source_snapshots(parent_id,content_hash,schema_hash,is_valid,metadata,quality_status)
              SELECT :parent,:hash,:schema,:valid,CAST(:meta AS jsonb),CAST(:quality AS quality_state)
              WHERE NOT EXISTS(SELECT 1 FROM source_snapshots WHERE parent_id=:parent AND content_hash=:hash)"""),
              {"parent": source_id, "hash": content_hash, "schema": schema_hash, "valid": valid,
               "meta": json.dumps(manifest), "quality": "valid" if valid else "invalid"})
            quality_path = path.parent / "quality" / "results.json"
            if quality_path.exists():
                quality = json.loads(quality_path.read_text(encoding="utf-8"))
                db.execute(text("""INSERT INTO quality_results(event_type,payload,quality_status)
                  SELECT 'phase1_snapshot',CAST(:payload AS jsonb),CAST(:state AS quality_state)
                  WHERE NOT EXISTS (
                    SELECT 1 FROM quality_results
                    WHERE payload->>'manifest_path'=:manifest_path)"""),
                  {"payload": json.dumps({"manifest_path": path.as_posix(), "result": quality}),
                   "manifest_path": path.as_posix(), "state": "valid" if valid else "invalid"})
        for product in products:
            payload = json.loads(product.read_text(encoding="utf-8"))
            source_key = str(payload.get("source") or product.stem)
            source_id = db.execute(text("SELECT id FROM sources WHERE source_key=:key"), {"key": source_key}).scalar()
            if not source_id:
                source_id = db.execute(text("INSERT INTO sources(source_key,name) VALUES(:k,:k) RETURNING id"), {"k": source_key}).scalar()
            dataset_key = f"phase1-{product.stem}"
            dataset_id = db.execute(text("""INSERT INTO datasets(dataset_key,name,source_id,quality_status)
              VALUES(:key,:name,:source,'valid')
              ON CONFLICT(dataset_key) DO UPDATE SET updated_at=now() RETURNING id"""),
              {"key": dataset_key, "name": product.stem, "source": source_id}).scalar_one()
            content_hash = digest(product)
            schema_hash = hashlib.sha256(json.dumps(sorted(payload.keys())).encode()).hexdigest()
            valid = str(payload.get("status", "current")).lower() not in {"invalid", "failed"}
            db.execute(text("""INSERT INTO dataset_versions(parent_id,content_hash,schema_hash,is_valid,metadata,quality_status)
              SELECT :parent,:hash,:schema,:valid,CAST(:meta AS jsonb),CAST(:quality AS quality_state)
              WHERE NOT EXISTS(SELECT 1 FROM dataset_versions WHERE parent_id=:parent AND content_hash=:hash)"""),
              {"parent": dataset_id, "hash": content_hash, "schema": schema_hash, "valid": valid,
               "meta": json.dumps({"path": product.as_posix(), "summary": {k: payload.get(k) for k in ("source","status","records","quality","limitations")}}),
               "quality": "valid" if valid else "invalid"})
            db.execute(text("""INSERT INTO indicators(indicator_key,name,quality_status)
              VALUES(:key,:name,CAST(:quality AS quality_state))
              ON CONFLICT(indicator_key) DO UPDATE SET updated_at=now()"""),
              {"key": product.stem, "name": product.stem.replace("-", " ").title(),
               "quality": "valid" if valid else "invalid"})
        for feature in territories.get("features", []):
            props = feature.get("properties", {})
            code = str(props.get("DPTO_CCDGO") or props.get("code") or "")
            name = props.get("DPTO_CNMBR") or props.get("name") or code
            if code:
                db.execute(text("""INSERT INTO territorial_units(canonical_code,name,unit_type,geom,quality_status)
                  VALUES(:code,:name,'department',ST_Multi(ST_SetSRID(ST_GeomFromGeoJSON(:geom),4326)),'valid')
                  ON CONFLICT(canonical_code) DO UPDATE SET name=excluded.name,updated_at=now()"""),
                  {"code": code, "name": name, "geom": json.dumps(feature["geometry"])})
        db.execute(text("""INSERT INTO lineage_events(event_type,payload,commit_sha,quality_status)
          VALUES('phase1_import',jsonb_build_object('manifests',:count,'territories',:territories),
          current_setting('application_name',true),'valid')"""),
          {"count": len(manifests), "territories": len(territories.get("features", []))})
    report = {"manifests_seen": len(manifests), "products_seen": len(products),
              "territories_seen": len(territories.get("features", [])), "idempotent": True}
    print(json.dumps(report, ensure_ascii=False))

if __name__ == "__main__":
    main()
