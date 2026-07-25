"""Descarga ArcGIS REST DIVIPOLA MGN 2025, reproyectada por el servidor a EPSG:4326."""
from pathlib import Path
from common import PUBLIC, feature_collection, get_json, normalize_divipola, now, write_json

SERVICE = "https://geoportal.dane.gov.co/mparcgis/rest/services/Divipola/Serv_DIVIPOLA_MGN_2025/FeatureServer"

def _layer_metadata(layer_id):
    return get_json(f"{SERVICE}/{layer_id}", {"f": "json"})

def _query(layer_id, where="1=1", geometry=True):
    endpoint=f"{SERVICE}/{layer_id}/query"
    identifiers=get_json(endpoint,{"f":"json","where":where,"returnIdsOnly":"true"}).get("objectIds",[])
    features=[]
    for start in range(0,len(identifiers),200):
        params={"f":"geojson","objectIds":",".join(map(str,identifiers[start:start+200])),"outFields":"*","outSR":"4326","returnGeometry":str(geometry).lower(),"maxAllowableOffset":"0.01","geometryPrecision":"5"}
        batch=get_json(endpoint,params)
        if "error" in batch: raise RuntimeError(batch["error"])
        features.extend(batch.get("features",[]))
    return {"type":"FeatureCollection","features":features}

def _field(meta, candidates):
    names = [f["name"] for f in meta.get("fields", [])]
    for candidate in candidates:
        if candidate in names:
            return candidate
    for name in names:
        if any(candidate.lower() in name.lower() for candidate in candidates):
            return name
    raise RuntimeError(f"No se encontró campo entre {candidates}; disponibles: {names}")

def _municipality_code(raw, department):
    digits="".join(c for c in str(raw or "").split(".")[0] if c.isdigit())
    return normalize_divipola(digits) if len(digits)>3 else f"{department}{digits.zfill(3)}"

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
    downloaded = now()

    departments = _query(dep_id)
    for feature in departments["features"]:
        p = feature["properties"]
        feature["properties"] = {"code":normalize_divipola(p.get(dep_code),"department"),"name":p.get(dep_name),"resultType":"observed","source":"dane-divipola-mgn-2025","year":2025}
    out = PUBLIC / "geography" / "departments.geojson"
    write_json(out, feature_collection(departments["features"], source="DANE DIVIPOLA MGN 2025", downloadedAt=downloaded, crs="EPSG:4326", simplification="ArcGIS maxAllowableOffset=0.01 grados y geometryPrecision=5; solo visualización web"))

    index_data = _query(mun_id, geometry=False)
    index = []
    for feature in index_data["features"]:
        p = feature["properties"]
        department=normalize_divipola(p.get(mun_dep),"department")
        code = _municipality_code(p.get(mun_code),department)
        if code:
            index.append({"code":code,"departmentCode":department,"name":p.get(mun_name),"resultType":"observed","source":"dane-divipola-mgn-2025","year":2025})
    index.sort(key=lambda x:x["code"])
    write_json(PUBLIC/"geography"/"municipalities-index.json", index)

    centroids = []
    for department in sorted({x["departmentCode"] for x in index if x["departmentCode"]}):
        collection = _query(mun_id, f"{mun_dep}='{department}'")
        features = []
        for feature in collection["features"]:
            p = feature["properties"]; code = _municipality_code(p.get(mun_code),department)
            feature["properties"] = {"code":code,"departmentCode":department,"name":p.get(mun_name),"resultType":"observed","source":"dane-divipola-mgn-2025","year":2025}
            features.append(feature)
            geom = feature.get("geometry") or {}
            coords = geom.get("coordinates", [])
            flat = []
            def walk(item):
                if item and isinstance(item[0], (int,float)): flat.append(item)
                else:
                    for child in item: walk(child)
            if coords: walk(coords)
            if flat: centroids.append({"code":code,"coordinates":[sum(x[0] for x in flat)/len(flat),sum(x[1] for x in flat)/len(flat)]})
        write_json(PUBLIC/"geography"/"municipalities"/f"{department}.geojson", feature_collection(features, source="DANE DIVIPOLA MGN 2025", downloadedAt=downloaded, crs="EPSG:4326", simplification="ArcGIS maxAllowableOffset=0.01 grados y geometryPrecision=5; solo visualización web"))
    write_json(PUBLIC/"geography"/"municipality-centroids.json", centroids)
    write_json(PUBLIC/"geography"/"geography-manifest.json", {"version":"1.0.0","status":"current","source":SERVICE,"downloadedAt":downloaded,"layers":{"departments":dep_id,"municipalities":mun_id},"departmentCount":len(departments["features"]),"municipalityCount":len(index),"crs":"EPSG:4326","partition":"municipalities by department","simplification":{"method":"ArcGIS maxAllowableOffset and geometryPrecision","toleranceDegrees":0.01,"precisionDecimals":5,"purpose":"visualización web; no sustituye cartografía oficial"}})
    print(f"DANE geography: {len(departments['features'])} departamentos; {len(index)} municipios/distritos")

if __name__ == "__main__": run()
