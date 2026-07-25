"""Adaptador conservador de fuentes tabulares oficiales suministradas manualmente."""
from pathlib import Path
from common import ROOT, PUBLIC, now, sha256, write_json

def process(source_id: str, filename: str, output: str):
    source = ROOT / "data" / "manual" / filename
    target = PUBLIC / "indicators" / output
    if not source.exists():
        write_json(target, {"source":source_id,"status":"manual-required","updatedAt":now(),"records":[],"message":f"Importe data/manual/{filename}; consulte data/manual/README.md"})
        print(f"{source_id}: manual-required")
        return
    try:
        import pandas as pd
        frame = pd.read_excel(source)
        columns = {str(c).strip().lower(): c for c in frame.columns}
        code_col = next((original for key,original in columns.items() if "divipola" in key or "código" in key or "codigo" in key), None)
        if code_col is None: raise ValueError("No se encontró columna DIVIPOLA/código")
        records = frame.where(frame.notna(), None).to_dict(orient="records")
        write_json(target, {"source":source_id,"status":"current","updatedAt":now(),"inputHash":sha256(source),"columns":[str(c) for c in frame.columns],"records":records})
        print(f"{source_id}: {len(records)} registros")
    except Exception as exc:
        write_json(target, {"source":source_id,"status":"unavailable","updatedAt":now(),"records":[],"message":str(exc)})
        raise
