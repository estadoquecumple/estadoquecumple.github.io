"""Adaptador conservador de archivos tabulares oficiales del DNP."""
from __future__ import annotations

from typing import Any

from common import PUBLIC, ROOT, now, read_json, sha256, write_json

DNP_TYPOLOGIES_URL = (
    "https://colaboracion.dnp.gov.co/CDT/Desarrollo%20Territorial/"
    "2026_Descentral%C3%ADzacion/01_ResultadosTipologias2026.xlsx"
)


def _clean(value: Any) -> Any:
    if value is None:
        return None
    try:
        import pandas as pd

        if pd.isna(value):
            return None
    except (TypeError, ValueError):
        pass
    return value.item() if hasattr(value, "item") else value


def _code(value: Any, width: int) -> str | None:
    value = _clean(value)
    if value is None:
        return None
    return str(value).strip().split(".")[0].zfill(width)


def _records(frame, level: str, metric: str) -> list[dict[str, Any]]:
    is_municipality = level == "municipality"
    code_column = "CodDANE_txt" if is_municipality else "cod_dep_txt"
    name_column = "Municipio" if is_municipality else "Departamento"
    result = []
    for _, row in frame.iterrows():
        code = _code(row.get(code_column), 5)
        value = _clean(row.get(metric))
        if not code or value is None:
            continue
        result.append(
            {
                "territoryCode": code,
                "territoryLevel": level,
                "department": _clean(row.get("Departamento")),
                "name": _clean(row.get(name_column)),
                "value": value,
            }
        )
    return result


def _process_dnp_workbook(source_id: str, source, target) -> None:
    import pandas as pd

    municipalities = pd.read_excel(source, sheet_name="Municipios", header=1)
    departments = pd.read_excel(source, sheet_name="Departamentos", header=2)
    profiles = {
        "dnp-typologies-2026": ("Tipología_2026", "2026", "typology"),
        "dnp-idf-2024": ("IDF_2024", "2024", "index"),
        "dnp-mdm": ("MDM_2024", "2024", "index"),
    }
    metric, period, value_kind = profiles[source_id]
    records = _records(municipalities, "municipality", metric)
    records.extend(_records(departments, "department", metric))
    municipal_count = sum(row["territoryLevel"] == "municipality" for row in records)
    department_count = sum(row["territoryLevel"] == "department" for row in records)
    if municipal_count < 1_100 or department_count < 32:
        raise ValueError(
            f"Cobertura DNP insuficiente: {municipal_count} municipios y "
            f"{department_count} departamentos"
        )
    write_json(
        target,
        {
            "source": source_id,
            "status": "current",
            "updatedAt": now(),
            "dataPeriod": period,
            "sourceUrl": DNP_TYPOLOGIES_URL,
            "inputFile": str(source.relative_to(ROOT)).replace("\\", "/"),
            "inputHash": sha256(source),
            "valueKind": value_kind,
            "coverage": {
                "municipalities": municipal_count,
                "departments": department_count,
                "complete": True,
            },
            "records": records,
            "limitations": [
                "La vigencia del indicador se conserva separada de la fecha de descarga.",
                "Las tipologías no reemplazan las categorías legales de la Ley 617 de 2000.",
            ],
        },
    )
    print(f"{source_id}: {len(records)} registros oficiales; vigencia {period}")


def process(source_id: str, filename: str, output: str) -> None:
    source = ROOT / "data" / "manual" / filename
    target = PUBLIC / "indicators" / output
    if not source.exists():
        if target.exists() and read_json(target).get("status") == "current":
            print(f"{source_id}: original ausente; se conserva la última versión válida")
            return
        write_json(
            target,
            {
                "source": source_id,
                "status": "manual-required",
                "updatedAt": now(),
                "records": [],
                "message": f"Importe data/manual/{filename}; consulte data/manual/README.md",
            },
        )
        print(f"{source_id}: manual-required")
        return
    try:
        _process_dnp_workbook(source_id, source, target)
    except Exception as exc:
        failure = ROOT / "data" / "cache" / "dnp" / source_id / "failed-update.json"
        write_json(
            failure,
            {
                "source": source_id,
                "status": "unavailable",
                "updatedAt": now(),
                "records": [],
                "message": str(exc),
                "retainedPublishedVersion": target.exists(),
            },
        )
        raise
