import hashlib
import json
import unicodedata
from pathlib import Path

from sqlalchemy import text

from services.shared.db import engine

ROOT = Path(".")
DATA_ROOT = ROOT / "public/data/territorial"
DANE_SOURCE = "dane-divipola-mgn-2025"


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def json_text(value) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalized_type(value: str) -> str:
    folded = unicodedata.normalize("NFKD", value)
    return "".join(char for char in folded if not unicodedata.combining(char)).lower().replace(" ", "_")


def main():
    source_catalog = read_json(DATA_ROOT / "catalog/sources.json")
    sources = source_catalog if isinstance(source_catalog, list) else source_catalog.get("sources", [])
    manifests = sorted((ROOT / "data/snapshots").glob("*/*/manifest.json"))
    departments = read_json(DATA_ROOT / "geography/departments.geojson")
    municipality_files = sorted((DATA_ROOT / "geography/municipalities").glob("*.geojson"))
    products = []
    for path in sorted((DATA_ROOT / "indicators").glob("*.json")):
        payload = read_json(path)
        if path.name != "index.json" and isinstance(payload.get("source"), str) and payload["source"].strip():
            products.append((path, payload))

    with engine.begin() as db:
        db.execute(text("DELETE FROM dataset_versions WHERE parent_id IN (SELECT id FROM datasets WHERE dataset_key='phase1-index')"))
        db.execute(text("DELETE FROM datasets WHERE dataset_key='phase1-index'"))
        db.execute(text("DELETE FROM indicators WHERE indicator_key='index'"))
        db.execute(text("DELETE FROM sources WHERE source_key='index'"))

        for item in sources:
            key = str(item.get("id") or item.get("source_id"))
            db.execute(
                text("""INSERT INTO sources(source_key,name,metadata,quality_status)
                  VALUES(:key,:name,CAST(:meta AS jsonb),'valid')
                  ON CONFLICT(source_key) DO UPDATE
                  SET name=excluded.name,metadata=excluded.metadata,updated_at=now()"""),
                {"key": key, "name": item.get("name") or item.get("entity") or key, "meta": json_text(item)},
            )

        for path in manifests:
            manifest = read_json(path)
            source_key = str(manifest.get("source_id") or path.parts[-3])
            source_id = db.execute(text("SELECT id FROM sources WHERE source_key=:key"), {"key": source_key}).scalar()
            if not source_id:
                source_id = db.execute(
                    text("INSERT INTO sources(source_key,name) VALUES(:key,:key) RETURNING id"), {"key": source_key}
                ).scalar()
            content_hash = manifest.get("sha256") or manifest.get("combined_sha256") or digest(path)
            schema_hash = hashlib.sha256(json_text(sorted(manifest.keys())).encode("utf-8")).hexdigest()
            valid = str(manifest.get("quality_status", manifest.get("status", "valid"))).lower() not in {"invalid", "failed"}
            db.execute(
                text("""INSERT INTO source_snapshots(parent_id,content_hash,schema_hash,is_valid,metadata,quality_status)
                  SELECT :parent,:hash,:schema,:valid,CAST(:meta AS jsonb),CAST(:quality AS quality_state)
                  WHERE NOT EXISTS(SELECT 1 FROM source_snapshots WHERE parent_id=:parent AND content_hash=:hash)"""),
                {"parent": source_id, "hash": content_hash, "schema": schema_hash, "valid": valid,
                 "meta": json_text(manifest), "quality": "valid" if valid else "invalid"},
            )
            quality_path = path.parent / "quality" / "results.json"
            if quality_path.exists():
                quality = read_json(quality_path)
                db.execute(
                    text("""INSERT INTO quality_results(event_type,payload,quality_status)
                      SELECT 'phase1_snapshot',CAST(:payload AS jsonb),CAST(:state AS quality_state)
                      WHERE NOT EXISTS (
                        SELECT 1 FROM quality_results WHERE payload->>'manifest_path'=:manifest_path)"""),
                    {"payload": json_text({"manifest_path": path.as_posix(), "result": quality}),
                     "manifest_path": path.as_posix(), "state": "valid" if valid else "invalid"},
                )

        for product, payload in products:
            source_key = payload["source"].strip()
            source_id = db.execute(text("SELECT id FROM sources WHERE source_key=:key"), {"key": source_key}).scalar()
            if not source_id:
                source_id = db.execute(
                    text("INSERT INTO sources(source_key,name) VALUES(:key,:key) RETURNING id"), {"key": source_key}
                ).scalar()
            dataset_id = db.execute(
                text("""INSERT INTO datasets(dataset_key,name,source_id,quality_status)
                  VALUES(:key,:name,:source,'valid')
                  ON CONFLICT(dataset_key) DO UPDATE SET source_id=excluded.source_id,updated_at=now()
                  RETURNING id"""),
                {"key": f"phase1-{product.stem}", "name": product.stem, "source": source_id},
            ).scalar_one()
            content_hash = digest(product)
            schema_hash = hashlib.sha256(json_text(sorted(payload.keys())).encode("utf-8")).hexdigest()
            valid = str(payload.get("status", "current")).lower() not in {"invalid", "failed"}
            summary = {key: payload.get(key) for key in ("source", "status", "records", "quality", "limitations")}
            db.execute(
                text("""INSERT INTO dataset_versions(parent_id,content_hash,schema_hash,is_valid,metadata,quality_status)
                  SELECT :parent,:hash,:schema,:valid,CAST(:meta AS jsonb),CAST(:quality AS quality_state)
                  WHERE NOT EXISTS(SELECT 1 FROM dataset_versions WHERE parent_id=:parent AND content_hash=:hash)"""),
                {"parent": dataset_id, "hash": content_hash, "schema": schema_hash, "valid": valid,
                 "meta": json_text({"path": product.as_posix(), "summary": summary}),
                 "quality": "valid" if valid else "invalid"},
            )
            db.execute(
                text("""INSERT INTO indicators(indicator_key,name,quality_status)
                  VALUES(:key,:name,CAST(:quality AS quality_state))
                  ON CONFLICT(indicator_key) DO UPDATE SET updated_at=now()"""),
                {"key": product.stem, "name": product.stem.replace("-", " ").title(),
                 "quality": "valid" if valid else "invalid"},
            )

        source_id = db.execute(text("SELECT id FROM sources WHERE source_key=:key"), {"key": DANE_SOURCE}).scalar_one()
        snapshot_id = db.execute(
            text("""SELECT id FROM source_snapshots WHERE parent_id=:source AND is_valid
              ORDER BY created_at DESC LIMIT 1"""), {"source": source_id},
        ).scalar()

        for feature in departments.get("features", []):
            props = feature.get("properties", {})
            code = str(props.get("DPTO_CCDGO") or props.get("code") or "")
            name = props.get("DPTO_CNMBR") or props.get("DPTO_CNMBRE") or props.get("name") or code
            if not code:
                continue
            feature_hash = hashlib.sha256(json_text(feature).encode("utf-8")).hexdigest()
            db.execute(
                text("""INSERT INTO territorial_units(
                    canonical_code,name,unit_type,geom,quality_status,level,literal_type,
                    normalized_type,source_id,snapshot_id,content_hash,geometry_reference)
                  VALUES(:code,:name,'department',ST_Multi(ST_SetSRID(ST_GeomFromGeoJSON(:geom),4326)),
                    'valid','department','DEPARTAMENTO','departamento',:source,:snapshot,:hash,:reference)
                  ON CONFLICT(canonical_code) DO UPDATE SET name=excluded.name,unit_type=excluded.unit_type,
                    geom=excluded.geom,level=excluded.level,literal_type=excluded.literal_type,
                    normalized_type=excluded.normalized_type,source_id=excluded.source_id,
                    snapshot_id=excluded.snapshot_id,content_hash=excluded.content_hash,
                    geometry_reference=excluded.geometry_reference,quality_status='valid',updated_at=now()"""),
                {"code": code, "name": name, "geom": json_text(feature["geometry"]), "source": source_id,
                 "snapshot": snapshot_id, "hash": feature_hash, "reference": "geography/departments.geojson"},
            )

        department_ids = dict(db.execute(
            text("SELECT canonical_code,id FROM territorial_units WHERE level='department'")
        ).all())
        local_count = 0
        for path in municipality_files:
            for feature in read_json(path).get("features", []):
                props = feature.get("properties", {})
                code = str(props.get("code") or "")
                department_code = str(props.get("departmentCode") or code[:2])
                literal = str(props.get("MPIO_TIPO") or props.get("type") or "")
                if not code or department_code not in department_ids:
                    continue
                feature_hash = hashlib.sha256(json_text(feature).encode("utf-8")).hexdigest()
                unit_id = db.execute(
                    text("""INSERT INTO territorial_units(
                        canonical_code,name,unit_type,geom,quality_status,level,literal_type,
                        normalized_type,department_id,source_id,snapshot_id,content_hash,geometry_reference)
                      VALUES(:code,:name,:unit_type,ST_Multi(ST_SetSRID(ST_GeomFromGeoJSON(:geom),4326)),
                        'valid','local',:literal,:normalized,:department,:source,:snapshot,:hash,:reference)
                      ON CONFLICT(canonical_code) DO UPDATE SET name=excluded.name,unit_type=excluded.unit_type,
                        geom=excluded.geom,level=excluded.level,literal_type=excluded.literal_type,
                        normalized_type=excluded.normalized_type,department_id=excluded.department_id,
                        source_id=excluded.source_id,snapshot_id=excluded.snapshot_id,
                        content_hash=excluded.content_hash,geometry_reference=excluded.geometry_reference,
                        quality_status='valid',updated_at=now() RETURNING id"""),
                    {"code": code, "name": str(props.get("name") or code),
                     "unit_type": props.get("unitType") or normalized_type(literal),
                     "geom": json_text(feature["geometry"]), "literal": literal,
                     "normalized": normalized_type(literal), "department": department_ids[department_code],
                     "source": source_id, "snapshot": snapshot_id, "hash": feature_hash,
                     "reference": f"geography/municipalities/{path.name}"},
                ).scalar_one()
                db.execute(
                    text("""INSERT INTO territorial_unit_versions(
                        territorial_unit_id,source_snapshot_id,content_hash,geom,metadata,quality_status)
                      SELECT :unit,:snapshot,:hash,ST_Multi(ST_SetSRID(ST_GeomFromGeoJSON(:geom),4326)),
                        CAST(:metadata AS jsonb),'valid'
                      WHERE NOT EXISTS(SELECT 1 FROM territorial_unit_versions
                        WHERE territorial_unit_id=:unit AND content_hash=:hash)"""),
                    {"unit": unit_id, "snapshot": snapshot_id, "hash": feature_hash,
                     "geom": json_text(feature["geometry"]), "metadata": json_text(props)},
                )
                local_count += 1

        db.execute(text("""
          INSERT INTO graph_nodes(node_type,canonical_key,name,properties,source_id,quality_status)
          SELECT 'territory',canonical_code,name,
            jsonb_build_object('level',level,'literal_type',literal_type,'identifiers',
              jsonb_build_object('divipola',canonical_code),'result_kind','observed'),
            source_id,'valid'
          FROM territorial_units
          ON CONFLICT(node_type,canonical_key) DO UPDATE SET
            name=excluded.name,properties=excluded.properties,source_id=excluded.source_id,updated_at=now()
        """))
        db.execute(text("""
          INSERT INTO graph_nodes(node_type,canonical_key,name,properties,source_id,quality_status)
          SELECT 'entity',id::text,name,
            jsonb_build_object('identifiers',coalesce(metadata->'identifiers','{}'::jsonb),
              'result_kind','observed'),NULL,'valid'
          FROM entities WHERE name IS NOT NULL
          ON CONFLICT(node_type,canonical_key) DO UPDATE SET name=excluded.name,properties=excluded.properties
        """))
        db.execute(text("""
          INSERT INTO graph_nodes(node_type,canonical_key,name,properties,source_id,quality_status)
          SELECT 'source',source_key,name,
            jsonb_build_object('identifiers',jsonb_build_object('source_key',source_key),
              'result_kind','observed'),id,'valid'
          FROM sources
          ON CONFLICT(node_type,canonical_key) DO UPDATE SET name=excluded.name,properties=excluded.properties
        """))
        db.execute(text("""
          INSERT INTO graph_edges(source_node_id,target_node_id,relation_type,valid_from,source_id,
            evidence,confidence,method,review_status)
          SELECT parent.id,child.id,'contains',now(),:source,
            jsonb_build_object('basis','DIVIPOLA parent code','result_kind','calculated'),
            1.0,'deterministic_divipola','approved'
          FROM graph_nodes child
          JOIN graph_nodes parent ON parent.node_type='territory'
            AND parent.canonical_key=left(child.canonical_key,2)
          WHERE child.node_type='territory' AND length(child.canonical_key)=5
            AND NOT EXISTS(SELECT 1 FROM graph_edges e WHERE e.source_node_id=parent.id
              AND e.target_node_id=child.id AND e.relation_type='contains' AND e.valid_to IS NULL)
        """), {"source": source_id})

        db.execute(
            text("""INSERT INTO lineage_events(event_type,payload,commit_sha,quality_status)
              SELECT 'phase1_import',
                jsonb_build_object('manifests',:count,'departments',:departments,'local_units',:locals),
                current_setting('application_name',true),'valid'
              WHERE NOT EXISTS(SELECT 1 FROM lineage_events WHERE event_type='phase1_import'
                AND payload->>'departments'=:department_text AND payload->>'local_units'=:local_text)"""),
            {"count": len(manifests), "departments": len(departments.get("features", [])),
             "locals": local_count, "department_text": str(len(departments.get("features", []))),
             "local_text": str(local_count)},
        )

    report = {"manifests_seen": len(manifests), "products_seen": len(products),
              "departments_seen": len(departments.get("features", [])), "local_units_seen": local_count,
              "territories_seen": len(departments.get("features", [])) + local_count,
              "encoding": "UTF-8", "idempotent": True}
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
