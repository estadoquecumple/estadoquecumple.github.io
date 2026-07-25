"""Consulta paginada y acotada del dataset oficial SGR; publica agregado, nunca la base masiva."""
from collections import Counter
import sys
from common import PUBLIC, get_json, now, write_json
URL="https://www.datos.gov.co/resource/mzgh-shtp.json"

def run(offline=False):
    output=PUBLIC/"indicators"/"sgr-aggregates.json"
    if offline:
        if not output.exists(): write_json(output,{"source":"dnp-sgr-mzgh-shtp","status":"unavailable","updatedAt":now(),"records":[]})
        return
    rows=get_json(URL,{"$limit":"5000","$order":":id"})
    # Los nombres de campo cambian; conservar solamente agrupaciones literales publicadas.
    territorial_keys=("departamento","nombre_departamento","departamento_entidad","municipio","nombre_municipio")
    counts=Counter()
    for row in rows:
        territory=next((str(row[k]).strip() for k in territorial_keys if row.get(k)), "Sin dato disponible")
        counts[territory]+=1
    records=[{"territoryLabel":k,"projectCount":v,"resultType":"calculated","source":"dnp-sgr-mzgh-shtp","valueAvailable":False} for k,v in sorted(counts.items())]
    write_json(output,{"source":"dnp-sgr-mzgh-shtp","status":"partial","updatedAt":now(),"dataDate":"Fecha informada por cada registro; muestra API de hasta 5.000 filas","recordSampleSize":len(rows),"records":records,"limitations":"Agregado de cobertura de muestra; no se extrapola ni se presenta como total nacional."})
    print(f"SGR: {len(rows)} filas oficiales consultadas; {len(records)} agrupaciones literales")
if __name__=="__main__": run("--offline" in sys.argv)
