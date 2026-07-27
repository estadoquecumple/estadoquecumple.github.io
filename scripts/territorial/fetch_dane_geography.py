"""Descarga DANE MGN 2025 preservando atributos y productos geométricos separados."""
from collections import Counter
from common import CACHE, PUBLIC, feature_collection, get_json, normalize_divipola, now, write_json
from platform_v4 import representative_point, validate_territorial_types

SERVICE = "https://geoportal.dane.gov.co/mparcgis/rest/services/Divipola/Serv_DIVIPOLA_MGN_2025/FeatureServer"

def _layer_metadata(layer_id):
    return get_json(f"{SERVICE}/{layer_id}", {"f": "json"})

def _query(layer_id, where="1=1", geometry=True, simplified=True):
    endpoint=f"{SERVICE}/{layer_id}/query"
    identifiers=get_json(endpoint,{"f":"json","where":where,"returnIdsOnly":"true"}).get("objectIds",[])
    features=[]
    for start in range(0,len(identifiers),200):
        params={"f":"geojson","objectIds":",".join(map(str,identifiers[start:start+200])),"outFields":"*","outSR":"4326","returnGeometry":str(geometry).lower()}
        if geometry and simplified:
            params.update({"maxAllowableOffset":"0.01","geometryPrecision":"5"})
        batch=get_json(endpoint,params)
        if "error" in batch: raise RuntimeError(batch["error"])
        features.extend(batch.get("features",[]))
    return {"type":"FeatureCollection","features":features}

def _field(meta, candidates, required=True):
    names = [f["name"] for f in meta.get("fields", [])]
    for candidate in candidates:
        if candidate in names:
            return candidate
    for name in names:
        if any(candidate.lower() in name.lower() for candidate in candidates):
            return name
    if required:
        raise RuntimeError(f"No se encontró campo entre {candidates}; disponibles: {names}")
    return None

def _municipality_code(raw, department):
    digits="".join(c for c in str(raw or "").split(".")[0] if c.isdigit())
    return normalize_divipola(digits) if len(digits)>3 else f"{department}{digits.zfill(3)}"

def _type_properties(raw):
    literal = raw if raw not in (None, "") else "Sin dato disponible"
    normalized = str(literal).strip().lower()
    return {"MPIO_TIPO": literal, "type": literal, "unitType": normalized}

def run():
    root_meta = get_json(SERVICE, {"f":"json"})
    layers = {x["name"].lower(): x["id"] for x in root_meta["layers"]}
    dep_id = next(v for k,v in layers.items() if "departamento" in k)
    mun_id = next(v for k,v in layers.items() if "municipio" in k)
    dep_meta, mun_meta = _layer_metadata(dep_id), _layer_metadata(mun_id)
    dep_code = _field(dep_meta, ["DPTO_CCDGO","COD_DPTO","DPT_COD"])
    dep_name = _field(dep_meta, ["DPTO_CNMBRE","DPTO_CNMBR","NOM_DPTO","DPT_NOMBRE"])
    mun_code = _field(mun_meta, ["MPIO_CCDGO","COD_MPIO","MUN_COD"])
    mun_name = _field(mun_meta, ["MPIO_CNMBR","NOM_MPIO","MUN_NOMBRE"])
    mun_dep = _field(mun_meta, ["DPTO_CCDGO","COD_DPTO","DPT_COD"])
    mun_type = _field(mun_meta, ["MPIO_TIPO"], required=False)
    mun_area = _field(mun_meta, ["MPIO_NAREA"], required=False)
    mun_year = _field(mun_meta, ["MPIO_NANO"], required=False)
    mun_resolution = _field(mun_meta, ["MPIO_CRSLCION", "MPIO_CRSL"], required=False)
    downloaded = now()

    departments = _query(dep_id)
    for feature in departments["features"]:
        p = feature["properties"]
        feature["properties"] = {"code":normalize_divipola(p.get(dep_code),"department"),"name":p.get(dep_name),"originalCode":p.get(dep_code),"originalName":p.get(dep_name),"resultType":"observed","source":"dane-divipola-mgn-2025","year":2025}
    out = PUBLIC / "geography" / "departments.geojson"
    write_json(out, feature_collection(departments["features"], source="DANE DIVIPOLA MGN 2025", downloadedAt=downloaded, crs="EPSG:4326", simplification="ArcGIS maxAllowableOffset=0.01 grados y geometryPrecision=5; solo visualización web"))

    index_data = _query(mun_id, geometry=False)
    index = []
    for feature in index_data["features"]:
        p = feature["properties"]
        department=normalize_divipola(p.get(mun_dep),"department")
        code = _municipality_code(p.get(mun_code),department)
        if code:
            type_properties = _type_properties(p.get(mun_type) if mun_type else None)
            index.append({
                "code":code, "departmentCode":department, "name":p.get(mun_name),
                "originalCode":p.get(mun_code), "originalName":p.get(mun_name),
                **type_properties,
                "MPIO_NAREA":p.get(mun_area) if mun_area else None,
                "MPIO_NANO":p.get(mun_year) if mun_year else None,
                "MPIO_CRSLCION":p.get(mun_resolution) if mun_resolution else None,
                "areaName":p.get(mun_area) if mun_area else None,
                "creationYear":p.get(mun_year) if mun_year else None,
                "creationResolution":p.get(mun_resolution) if mun_resolution else None,
                "resultType":"observed","source":"dane-divipola-mgn-2025","year":2025,
            })
    index.sort(key=lambda x:x["code"])
    validate_territorial_types(index)
    write_json(PUBLIC/"geography"/"municipalities-index.json", index)
    counts = Counter(str(item["type"]) for item in index)
    write_json(PUBLIC/"geography"/"territorial-unit-types.json", {
        "source":"dane-divipola-mgn-2025", "status":"current", "updatedAt":downloaded,
        "field":"MPIO_TIPO", "total":len(index),
        "counts":[{"type":key,"count":value} for key,value in sorted(counts.items())],
    })

    centroids = []
    for department in sorted({x["departmentCode"] for x in index if x["departmentCode"]}):
        official = _query(mun_id, f"{mun_dep}='{department}'", simplified=False)
        collection = _query(mun_id, f"{mun_dep}='{department}'", simplified=True)
        CACHE.mkdir(parents=True, exist_ok=True)
        write_json(CACHE/"dane-geography-official"/f"{department}.geojson", official)
        features = []
        for feature in collection["features"]:
            p = feature["properties"]; code = _municipality_code(p.get(mun_code),department)
            type_properties = _type_properties(p.get(mun_type) if mun_type else None)
            feature["properties"] = {
                "code":code,"departmentCode":department,"name":p.get(mun_name),
                "originalCode":p.get(mun_code),"originalName":p.get(mun_name),
                **type_properties,
                "MPIO_NAREA":p.get(mun_area) if mun_area else None,
                "MPIO_NANO":p.get(mun_year) if mun_year else None,
                "MPIO_CRSLCION":p.get(mun_resolution) if mun_resolution else None,
                "areaName":p.get(mun_area) if mun_area else None,
                "creationYear":p.get(mun_year) if mun_year else None,
                "creationResolution":p.get(mun_resolution) if mun_resolution else None,
                "resultType":"observed","source":"dane-divipola-mgn-2025","year":2025,
            }
            features.append(feature)
            geom = feature.get("geometry")
            if geom:
                centroids.append({"code":code,"coordinates":representative_point(geom),"method":"Shapely representative_point"})
        write_json(PUBLIC/"geography"/"municipalities"/f"{department}.geojson", feature_collection(features, source="DANE DIVIPOLA MGN 2025", downloadedAt=downloaded, crs="EPSG:4326", simplification="ArcGIS maxAllowableOffset=0.01 grados y geometryPrecision=5; solo visualización web"))
    write_json(PUBLIC/"geography"/"municipality-centroids.json", centroids)
    write_json(PUBLIC/"geography"/"geography-manifest.json", {"version":"4.0.0","status":"current","source":SERVICE,"downloadedAt":downloaded,"layers":{"departments":dep_id,"municipalities":mun_id},"departmentCount":len(departments["features"]),"territorialUnitCount":len(index),"municipalityCount":counts.get("MUNICIPIO",0),"nonMunicipalizedAreaCount":counts.get("ÁREA NO MUNICIPALIZADA",0),"typeCounts":dict(counts),"crs":"EPSG:4326","partition":"unidades territoriales por departamento","officialGeometry":"data/cache/dane-geography-official; sin simplificación, destinada a snapshot/GeoParquet","simplification":{"method":"ArcGIS maxAllowableOffset and geometryPrecision","toleranceDegrees":0.01,"precisionDecimals":5,"purpose":"visualización web; no sustituye cartografía oficial"},"representativePoint":"Shapely representative_point; no promedio de vértices"})
    print(f"DANE geography: {len(departments['features'])} departamentos; {len(index)} municipios/distritos")

if __name__ == "__main__": run()
