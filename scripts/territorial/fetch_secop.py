"""Adaptador SoQL agregado para SECOP II con separación explícita de datasets."""
from common import PUBLIC, get_json, now, write_json
import sys
DATASETS={"processes":"p6dx-8zbt","contracts":"jbjy-vk9h","locations":"gra4-pcp2","execution":"mfmm-jqmq"}

def run(offline=False):
    output=PUBLIC/"indicators"/"secop-aggregates.json"
    if offline:
        if not output.exists(): write_json(output,{"source":"secop-ii","status":"unavailable","updatedAt":now(),"records":[]})
        return
    records=[]
    for kind,dataset in DATASETS.items():
        try:
            row=get_json(f"https://www.datos.gov.co/resource/{dataset}.json",{"$select":"count(*) as records","$limit":"1"})[0]
            records.append({"dataset":dataset,"kind":kind,"recordCount":int(row["records"]),"resultType":"calculated","territorialDimension":"execution" if kind in ("locations","execution") else "contracting-entity"})
        except Exception as exc:
            records.append({"dataset":dataset,"kind":kind,"recordCount":None,"resultType":"calculated","error":str(exc)})
    status="partial" if any(x["recordCount"] is None for x in records) else "current"
    write_json(output,{"source":"secop-ii","status":status,"updatedAt":now(),"records":records,"limitations":"Conteos API verificables. Las agregaciones municipales se habilitan al confirmar campos estables por dataset; no se descargan filas masivas al navegador."})
    print("SECOP:", ", ".join(f"{x['dataset']}={x['recordCount']}" for x in records))
if __name__=="__main__": run("--offline" in sys.argv)
