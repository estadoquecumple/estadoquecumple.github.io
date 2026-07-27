from __future__ import annotations
import json, re
from common import PUBLIC, read_json
from platform_v4 import load_catalog

ALLOWED={"current","stale","partial","manual-required","unavailable"}
def run():
    errors=[]; warnings=[]
    required=["geography/departments.geojson","geography/municipalities-index.json","geography/municipality-centroids.json","geography/geography-manifest.json","indicators/population.json","indicators/fiscal.json","indicators/sgr-aggregates.json","indicators/secop-aggregates.json","government/entities-by-territory.json","official-sources.json","scenarios/current.json","scenarios/regional-exploratory.json","scenarios/shared-services.json","catalog/sources.json","catalog/snapshot-status.json","analytics/catalog.parquet","analytics/indicators.parquet","analytics/series.parquet","analytics/entities.parquet","analytics/secop-aggregates.parquet","analytics/sgr-aggregates.parquet","analytics/departments.geoparquet","analytics/h3-divipola.parquet","analytics/manifest.json","current/foundation-v4.json","manifest.json"]
    for rel in required:
        path=PUBLIC/rel
        if not path.exists(): errors.append(f"falta {rel}"); continue
        if path.suffix in (".parquet", ".geoparquet"):
            continue
        try:
            text=path.read_text(encoding="utf-8")
            json.loads(text)
            if re.search(r"\b(?:NaN|Infinity|-Infinity)\b",text): errors.append(f"{rel}: valor no finito")
        except Exception as exc: errors.append(f"{rel}: JSON inválido ({exc})")
    try:
        catalog=load_catalog()
        if len(catalog.sources)<8: errors.append("catálogo V4: cobertura de fuentes insuficiente")
    except Exception as exc:
        errors.append(f"catálogo V4 inválido ({exc})")
    try:
        import geopandas as gpd
        import pandas as pd
        catalog_parquet=pd.read_parquet(PUBLIC/"analytics"/"catalog.parquet")
        if catalog_parquet.empty: errors.append("catalog.parquet vacío")
        geo=gpd.read_parquet(PUBLIC/"analytics"/"departments.geoparquet")
        if geo.crs is None or geo.empty: errors.append("GeoParquet sin CRS o geometrías")
        h3_frame=pd.read_parquet(PUBLIC/"analytics"/"h3-divipola.parquet")
        secop_frame=pd.read_parquet(PUBLIC/"analytics"/"secop-aggregates.parquet")
        secop_doc=read_json(PUBLIC/"indicators"/"secop-aggregates.json")
        if len(secop_frame)!=secop_doc.get("quality",{}).get("aggregatedRows"):
            errors.append("SECOP Parquet no conserva todos los agregados")
        if secop_doc.get("status")!="current":
            errors.append("SECOP no tiene una versión completa publicable")
        sgr_frame=pd.read_parquet(PUBLIC/"analytics"/"sgr-aggregates.parquet")
        sgr_doc=read_json(PUBLIC/"indicators"/"sgr-aggregates.json")
        if len(sgr_frame)!=len(sgr_doc.get("records",[])) or not sgr_doc.get("complete"):
            errors.append("SGR Parquet o cobertura incompletos")
        if h3_frame.empty or h3_frame["h3"].duplicated().all(): errors.append("H3 sin asociaciones útiles")
    except Exception as exc:
        errors.append(f"productos Parquet/GeoParquet inválidos ({exc})")
    snapshot_status=PUBLIC/"catalog"/"snapshot-status.json"
    if snapshot_status.exists():
        for item in read_json(snapshot_status).get("sources",[]):
            if item.get("promoted") and not re.fullmatch(r"[a-f0-9]{64}",item.get("rawHash","")):
                errors.append(f"snapshot {item.get('sourceId')}: hash inválido")
    idx=PUBLIC/"geography"/"municipalities-index.json"
    if idx.exists():
        rows=read_json(idx); codes=[x.get("code","") for x in rows]
        if any(not re.fullmatch(r"\d{5}",c) for c in codes): errors.append("municipalities-index: DIVIPOLA no tiene cinco caracteres")
        if len(codes)!=len(set(codes)): errors.append("municipalities-index: códigos duplicados")
    for path in (PUBLIC/"indicators").glob("*.json"):
        doc=read_json(path)
        if "status" in doc and doc["status"] not in ALLOWED: errors.append(f"{path.name}: estado inválido")
        if doc.get("status")=="manual-required": warnings.append(f"{doc.get('source')}: manual-required")
    government=PUBLIC/"government"/"entities-by-territory.json"
    if government.exists():
        doc=read_json(government); records=doc.get("records",[]); codes=[item.get("code","") for item in records]
        if doc.get("source")!="sigep-entities-kqut-4h4r": errors.append("government: fuente inesperada")
        if any(not re.fullmatch(r"\d{5}",code) for code in codes): errors.append("government: DIVIPOLA inválido")
        if len(codes)!=len(set(codes)): errors.append("government: DIVIPOLA duplicado")
    registry=PUBLIC/"official-sources.json"
    if registry.exists():
        for source in read_json(registry).get("sources",[]):
            if not str(source.get("url","")).startswith("https://"): errors.append(f"official-sources: URL insegura en {source.get('id')}")
    for path in (PUBLIC/"scenarios").glob("*.json"):
        doc=read_json(path)
        for key in ("version","authorship","status","objective","units","assignments","assumptions","risks","legalRequirements","uncertainty","sources","history"):
            if key not in doc: errors.append(f"{path.name}: falta {key}")
    if errors:
        print("DATA VALIDATE: ERROR")
        print("\n".join(f"- {x}" for x in errors)); raise SystemExit(1)
    print(f"DATA VALIDATE OK: {len(required)} archivos obligatorios; catálogo, Pandera, Parquet, GeoParquet, H3, snapshots, DIVIPOLA y escenarios verificados.")
    for item in warnings: print(f"AVISO: {item}")
if __name__=="__main__": run()
