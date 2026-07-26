"""Agrega el directorio oficial SIGEP por DIVIPOLA sin publicar datos personales."""
from collections import defaultdict
import sys
from common import PUBLIC, get_json, now, write_json

URL = "https://www.datos.gov.co/resource/kqut-4h4r.json"

def digits(value):
    text = "".join(character for character in str(value or "") if character.isdigit())
    return text.zfill(5)[-5:] if text else ""

def run(offline=False):
    output = PUBLIC / "government" / "entities-by-territory.json"
    if offline:
        if not output.exists():
            write_json(output, {"source": "sigep-entities-kqut-4h4r", "status": "unavailable", "updatedAt": now(), "records": []})
        return
    rows = get_json(URL, {"$limit": "50000"})
    grouped = defaultdict(lambda: {"entityCount": 0, "sectors": set(), "orders": set(), "classifications": set()})
    for row in rows:
        code = digits(row.get("divipola_municipio"))
        if not code:
            continue
        item = grouped[code]
        item["entityCount"] += 1
        for source, target in (("sector", "sectors"), ("orden", "orders"), ("clasificaci_n_org_nica", "classifications")):
            if row.get(source):
                item[target].add(str(row[source]).strip())
    records = [
        {"code": code, "entityCount": item["entityCount"], "sectors": sorted(item["sectors"]),
         "orders": sorted(item["orders"]), "classifications": sorted(item["classifications"]),
         "resultType": "calculated"}
        for code, item in sorted(grouped.items())
    ]
    write_json(output, {
        "source": "sigep-entities-kqut-4h4r", "status": "current", "updatedAt": now(),
        "sourceRows": len(rows), "records": records,
        "limitations": "Conteo por sede municipal publicada. No equivale a planta de personal ni a cobertura efectiva de servicios."
    })
    print(f"SIGEP: {len(rows)} filas; {len(records)} códigos DIVIPOLA")

if __name__ == "__main__":
    run("--offline" in sys.argv)
