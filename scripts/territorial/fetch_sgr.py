"""SGR completo mediante paginación; si la fuente falla, declara cobertura parcial."""
from __future__ import annotations

import sys
from collections import defaultdict
from typing import Any

from common import CACHE, PUBLIC, get_json, now, write_json

URL = "https://www.datos.gov.co/resource/mzgh-shtp.json"
PAGE_SIZE = 20_000

FIELD_CANDIDATES = {
    "bpin": ("bpin", "codigo_bpin", "c_digo_bpin", "codigobpin"),
    "name": ("nombre_del_proyecto", "nombre_proyecto", "proyecto", "nombre"),
    "status": ("estado_del_proyecto", "estado", "estado_proyecto"),
    "value": ("valor_total_del_proyecto", "valor_total", "valor_sgr", "valortotal"),
    "sector": ("sector", "sector_de_inversion"),
    "executor": ("ejecutor", "nombre_ejecutor", "entidad_ejecutora", "entidadejecutora"),
    "territory_code": ("codigo_dane", "c_digo_dane", "codigo_municipio", "divipola"),
    "department": ("departamento", "nombre_departamento", "departamento_entidad"),
    "municipality": ("municipio", "nombre_municipio"),
    "date": ("fecha_de_aprobacion", "fecha_aprobacion", "fecha"),
}


def pick(row: dict[str, Any], logical: str) -> Any:
    return next((row[key] for key in FIELD_CANDIDATES[logical] if row.get(key) not in (None, "")), None)


def decimal(value: Any) -> float | None:
    try:
        return float(str(value).replace(",", "").strip())
    except (TypeError, ValueError):
        return None


def aggregate_rows(rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    unique: dict[str, dict[str, Any]] = {}
    without_bpin = 0
    duplicates = 0
    for index, row in enumerate(rows):
        bpin = str(pick(row, "bpin") or "").strip()
        if not bpin:
            without_bpin += 1
            key = f"missing:{index}"
        else:
            key = bpin
        if key in unique:
            duplicates += 1
            continue
        unique[key] = row

    groups: dict[tuple[str, str, str, str, str], dict[str, Any]] = defaultdict(
        lambda: {"records": 0, "value": 0.0, "valueRecords": 0}
    )
    for row in unique.values():
        territory_code = str(pick(row, "territory_code") or "").strip()
        department = str(pick(row, "department") or "Sin dato disponible").strip()
        municipality = str(pick(row, "municipality") or "Sin dato disponible").strip()
        sector = str(pick(row, "sector") or "Sin dato disponible").strip()
        status = str(pick(row, "status") or "Sin dato disponible").strip()
        executor = str(pick(row, "executor") or "Sin dato disponible").strip()
        group = groups[(territory_code, department, municipality, sector, status, executor)]
        group["records"] += 1
        value = decimal(pick(row, "value"))
        if value is not None and value >= 0:
            group["value"] += value
            group["valueRecords"] += 1

    records = [
        {
            "source": "dnp-sgr-mzgh-shtp",
            "territoryCode": key[0] or None,
            "department": key[1],
            "municipality": key[2],
            "sector": key[3],
            "status": key[4],
            "executor": key[5],
            "records": values["records"],
            "value": round(values["value"], 2) if values["valueRecords"] else None,
            "valueCoverage": values["valueRecords"],
            "resultType": "calculated",
        }
        for key, values in sorted(groups.items())
    ]
    quality = {
        "inputRows": len(rows),
        "uniqueProjects": len(unique),
        "duplicateBpinRows": duplicates,
        "rowsWithoutBpin": without_bpin,
        "aggregatedProjectCount": sum(record["records"] for record in records),
        "valid": sum(record["records"] for record in records) == len(unique),
    }
    return records, quality


def fetch_all() -> tuple[list[dict[str, Any]], int, bool, str | None]:
    total = int(get_json(URL, {"$select": "count(*) as total"})[0]["total"])
    rows: list[dict[str, Any]] = []
    error: str | None = None
    for offset in range(0, total, PAGE_SIZE):
        try:
            page = get_json(URL, {"$limit": PAGE_SIZE, "$offset": offset, "$order": ":id"})
        except Exception as exc:
            error = str(exc)
            break
        rows.extend(page)
        if len(page) < PAGE_SIZE:
            break
    return rows, total, len(rows) == total, error


def run(offline: bool = False) -> None:
    output = PUBLIC / "indicators" / "sgr-aggregates.json"
    if offline:
        if not output.exists():
            write_json(output, {"source": "dnp-sgr-mzgh-shtp", "status": "unavailable", "records": []})
        return
    cached = "--cached" in sys.argv
    cache_path = CACHE / "sgr-mzgh-shtp-raw.json"
    if cached and cache_path.exists():
        cached_document = __import__("json").loads(cache_path.read_text(encoding="utf-8"))
        rows = cached_document["rows"]
        expected = int(cached_document["expectedRows"])
        complete = len(rows) == expected
        fetch_error = None
    else:
        rows, expected, complete, fetch_error = fetch_all()
    CACHE.mkdir(parents=True, exist_ok=True)
    write_json(CACHE / "sgr-mzgh-shtp-raw.json", {"sourceUrl": URL, "retrievedAt": now(), "expectedRows": expected, "rows": rows})
    records, quality = aggregate_rows(rows)
    status = "current" if complete and quality["valid"] else "partial"
    write_json(
        output,
        {
            "source": "dnp-sgr-mzgh-shtp",
            "status": status,
            "updatedAt": now(),
            "expectedRows": expected,
            "retrievedRows": len(rows),
            "coverageRatio": round(len(rows) / expected, 6) if expected else 1,
            "complete": complete,
            "fetchError": fetch_error,
            "quality": quality,
            "records": records,
            "limitations": (
                "Cobertura completa según count(*) de Socrata."
                if complete
                else "Cobertura parcial explícita; no se extrapolan filas no recuperadas."
            ),
        },
    )
    print(f"SGR: {len(rows)}/{expected} filas; {quality['uniqueProjects']} proyectos únicos; {status}")


if __name__ == "__main__":
    run("--offline" in sys.argv)
