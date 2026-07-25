from __future__ import annotations
import json, re, sys
from pathlib import Path
from common import PUBLIC, ROOT, read_json

ALLOWED={"current","stale","partial","manual-required","unavailable"}
def run():
    errors=[]; warnings=[]
    required=["geography/departments.geojson","geography/municipalities-index.json","geography/municipality-centroids.json","geography/geography-manifest.json","indicators/population.json","indicators/fiscal.json","indicators/sgr-aggregates.json","indicators/secop-aggregates.json","scenarios/current.json","scenarios/regional-exploratory.json","scenarios/shared-services.json","manifest.json"]
    for rel in required:
        path=PUBLIC/rel
        if not path.exists(): errors.append(f"falta {rel}"); continue
        try:
            text=path.read_text(encoding="utf-8")
            json.loads(text)
            if re.search(r"\b(?:NaN|Infinity|-Infinity)\b",text): errors.append(f"{rel}: valor no finito")
        except Exception as exc: errors.append(f"{rel}: JSON inválido ({exc})")
    idx=PUBLIC/"geography"/"municipalities-index.json"
    if idx.exists():
        rows=read_json(idx); codes=[x.get("code","") for x in rows]
        if any(not re.fullmatch(r"\d{5}",c) for c in codes): errors.append("municipalities-index: DIVIPOLA no tiene cinco caracteres")
        if len(codes)!=len(set(codes)): errors.append("municipalities-index: códigos duplicados")
    for path in (PUBLIC/"indicators").glob("*.json"):
        doc=read_json(path)
        if "status" in doc and doc["status"] not in ALLOWED: errors.append(f"{path.name}: estado inválido")
        if doc.get("status")=="manual-required": warnings.append(f"{doc.get('source')}: manual-required")
    for path in (PUBLIC/"scenarios").glob("*.json"):
        doc=read_json(path)
        for key in ("version","authorship","status","objective","units","assignments","assumptions","risks","legalRequirements","uncertainty","sources","history"):
            if key not in doc: errors.append(f"{path.name}: falta {key}")
    if errors:
        print("DATA VALIDATE: ERROR")
        print("\n".join(f"- {x}" for x in errors)); raise SystemExit(1)
    print(f"DATA VALIDATE OK: {len(required)} archivos obligatorios; DIVIPOLA, escenarios, JSON, estados y valores finitos verificados.")
    for item in warnings: print(f"AVISO: {item}")
if __name__=="__main__": run()
