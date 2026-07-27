"""Agregados SECOP II por dimensiones confirmadas en metadatos Socrata."""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from typing import Any

from common import CACHE, PUBLIC, get_json, now, read_json, sha256, write_json

DATASET = "jbjy-vk9h"
RESOURCE = f"https://www.datos.gov.co/resource/{DATASET}.json"
METADATA = f"https://www.datos.gov.co/api/views/{DATASET}"
EXECUTION_DATASET = "gra4-pcp2"
EXECUTION_RESOURCE = f"https://www.datos.gov.co/resource/{EXECUTION_DATASET}.json"
MODIFICATIONS_DATASET = "cb9c-h8sn"
MODIFICATIONS_RESOURCE = f"https://www.datos.gov.co/resource/{MODIFICATIONS_DATASET}.json"
PAGE_SIZE = 20_000

CANDIDATES = {
    "year": ("fecha_de_firma", "fecha_de_inicio_del_contrato", "fecha_de_publicacion"),
    "department": ("departamento", "departamento_entidad"),
    "municipality": ("ciudad", "municipio"),
    "entity": ("nombre_entidad",),
    "execution_department": ("departamento_ejecucion", "departamento_de_ejecucion"),
    "execution_municipality": ("municipio_ejecucion", "municipio_de_ejecucion"),
    "sector": ("sector",),
    "modality": ("modalidad_de_contratacion",),
    "status": ("estado_contrato",),
    "supplier": ("proveedor_adjudicado", "nombre_del_proveedor"),
    "unspsc": ("codigo_de_categoria_principal",),
    "value": ("valor_del_contrato", "valor_contrato"),
    "duration": ("duraci_n_del_contrato", "duracion_del_contrato"),
    "additions": ("valor_pendiente_de_ejecucion", "valor_facturado"),
}


def metadata_fields(metadata: dict[str, Any]) -> set[str]:
    return {column["fieldName"] for column in metadata.get("columns", []) if column.get("fieldName")}


def resolve_fields(fields: set[str]) -> dict[str, str | None]:
    return {logical: next((candidate for candidate in candidates if candidate in fields), None) for logical, candidates in CANDIDATES.items()}


def aggregate_query(
    dimensions: list[tuple[str, str]],
    value_field: str | None,
    *,
    fetch=None,
    max_groups: int | None = None,
    resource: str = RESOURCE,
) -> list[dict[str, Any]]:
    def expression(field: str) -> str:
        return field if "(" in field else f"`{field}`"

    aliases = [f"{expression(field)} as {logical}" for logical, field in dimensions]
    select = aliases + ["count(*) as records"]
    if value_field:
        select.append(f"sum(`{value_field}`) as value")
    group = ",".join(expression(field) for _, field in dimensions)
    rows: list[dict[str, Any]] = []
    offset = 0
    while True:
        params = {
            "$select": ",".join(select),
            "$group": group,
            "$order": group,
            "$limit": PAGE_SIZE if max_groups is None else min(PAGE_SIZE, max_groups - offset),
            "$offset": offset,
        }
        page = (fetch or (lambda url, query: get_json(url, query, retries=3, timeout=180)))(resource, params)
        rows.extend(page)
        if len(page) < PAGE_SIZE or (max_groups is not None and len(rows) >= max_groups):
            break
        offset += PAGE_SIZE
    return rows


def normalize_aggregate(rows: list[dict[str, Any]], dimension: str) -> list[dict[str, Any]]:
    normalized = []
    for row in rows:
        value = row.get("value")
        normalized.append(
            {
                "source": "secop-ii",
                "dataset": DATASET,
                "dimension": dimension,
                **{key: value for key, value in row.items() if key not in ("records", "value")},
                "records": int(row["records"]),
                "value": float(value) if value not in (None, "") else None,
                "resultType": "calculated",
            }
        )
    return normalized


def publish_analytics(records: list[dict[str, Any]]) -> dict[str, Any]:
    import pandas as pd

    target = PUBLIC / "analytics" / "secop-aggregates.parquet"
    target.parent.mkdir(parents=True, exist_ok=True)
    frame = pd.DataFrame(records)
    frame.to_parquet(target, index=False, compression="zstd")
    return {
        "path": "data/territorial/analytics/secop-aggregates.parquet",
        "rows": len(frame),
        "bytes": target.stat().st_size,
        "sha256": sha256(target),
    }


def compact_existing() -> None:
    output = PUBLIC / "indicators" / "secop-aggregates.json"
    document = read_json(output)
    records = document.get("records", [])
    document["analytics"] = publish_analytics(records)
    document["records"] = [row for row in records if row.get("dimension") != "supplier"]
    document["fallback"] = {
        "excludedDimensions": ["supplier"],
        "recordCount": len(document["records"]),
        "reason": "El detalle completo de alta cardinalidad se consulta en Parquet con DuckDB-Wasm.",
    }
    write_json(output, document)
    print(
        f"SECOP compacto: {document['analytics']['rows']} filas Parquet; "
        f"{len(document['records'])} filas JSON fallback"
    )


def aggregate_years(date_field: str, value_field: str | None) -> list[dict[str, Any]]:
    current_year = datetime.now(timezone.utc).year
    records = []
    for year in range(2015, current_year + 1):
        select = ["count(*) as records"]
        if value_field:
            select.append(f"sum(`{value_field}`) as value")
        rows = get_json(
            RESOURCE,
            {
                "$select": ",".join(select),
                "$where": (
                    f"`{date_field}` >= '{year}-01-01T00:00:00.000' "
                    f"AND `{date_field}` < '{year + 1}-01-01T00:00:00.000'"
                ),
                "$limit": 1,
            },
            retries=3,
            timeout=180,
        )
        if rows and int(rows[0].get("records", 0)):
            records.append({"year": year, **rows[0]})
    return records


def run(offline: bool = False) -> None:
    output = PUBLIC / "indicators" / "secop-aggregates.json"
    if offline:
        if not output.exists():
            write_json(output, {"source": "secop-ii", "status": "unavailable", "records": []})
        return
    metadata = get_json(METADATA)
    CACHE.mkdir(parents=True, exist_ok=True)
    resolved = resolve_fields(metadata_fields(metadata))
    value_field = resolved["value"]
    year_expression = f"date_extract_y(`{resolved['year']}`)" if resolved["year"] else None
    plans = {
        "contracting-territory": [("department", resolved["department"]), ("municipality", resolved["municipality"])],
        "contracting-entity": [("entity", resolved["entity"])],
        "sector": [("sector", resolved["sector"])],
        "modality": [("modality", resolved["modality"])],
        "status": [("status", resolved["status"])],
        "supplier": [("supplier", resolved["supplier"])],
        "unspsc": [("unspsc", resolved["unspsc"])],
    }
    records: list[dict[str, Any]] = []
    limitations: list[str] = []
    if year_expression and resolved["year"]:
        try:
            year_rows = aggregate_years(resolved["year"], value_field)
            write_json(CACHE / f"secop-{DATASET}-year-raw-aggregate.json", {
                "sourceUrl": RESOURCE, "queryDimension": "year", "retrievedAt": now(), "rows": year_rows,
            })
            records.extend(normalize_aggregate(year_rows, "year"))
        except Exception as exc:
            limitations.append(f"year: consulta no disponible ({exc})")
    else:
        limitations.append("year: campo de fecha ausente")
    if "--year-only" in sys.argv and output.exists():
        previous = read_json(output)
        records.extend(row for row in previous.get("records", []) if row.get("dimension") != "year")
        plans = {key: value for key, value in plans.items()}
    else:
        previous = None
    for dimension, fields in plans.items():
        if "--year-only" in sys.argv:
            break
        available = [(logical, field) for logical, field in fields if field]
        missing = [logical for logical, field in fields if not field]
        if missing:
            limitations.append(f"{dimension}: campos ausentes {', '.join(missing)}")
        if not available:
            continue
        try:
            dimension_value = None if dimension in ("supplier", "contracting-entity") else value_field
            rows = aggregate_query(available, dimension_value)
        except Exception as exc:
            limitations.append(f"{dimension}: consulta no disponible ({exc})")
            continue
        write_json(CACHE / f"secop-{DATASET}-{dimension}-raw-aggregate.json", {
            "sourceUrl": RESOURCE,
            "queryDimension": dimension,
            "retrievedAt": now(),
            "rows": rows,
        })
        records.extend(normalize_aggregate(rows, dimension))

    external_plans = {
        "execution-location": (
            EXECUTION_RESOURCE,
            [("executionLocation", "ubicacion")],
        ),
        "modifications": (
            MODIFICATIONS_RESOURCE,
            [("modificationType", "tipo")],
        ),
    }
    for dimension, (resource, fields) in external_plans.items():
        try:
            rows = aggregate_query(fields, None, resource=resource)
        except Exception as exc:
            limitations.append(f"{dimension}: consulta no disponible ({exc})")
            continue
        write_json(
            CACHE / f"secop-{dimension}-raw-aggregate.json",
            {
                "sourceUrl": resource,
                "queryDimension": dimension,
                "retrievedAt": now(),
                "rows": rows,
            },
        )
        records.extend(normalize_aggregate(rows, dimension))

    write_json(CACHE / f"secop-{DATASET}-metadata.json", metadata)
    status = "current" if not limitations else "partial"
    dimensions = ["year", *plans, *external_plans]
    analytics = publish_analytics(records)
    fallback_records = [row for row in records if row.get("dimension") != "supplier"]
    candidate = {
            "source": "secop-ii",
            "dataset": DATASET,
            "status": status,
            "updatedAt": now(),
            "dimensions": dimensions,
            "resolvedFields": resolved,
            "analytics": analytics,
            "records": fallback_records,
            "fallback": {
                "excludedDimensions": ["supplier"],
                "recordCount": len(fallback_records),
                "reason": "El detalle completo de alta cardinalidad se consulta en Parquet con DuckDB-Wasm.",
            },
            "quality": {
                "aggregatedRows": len(records),
                "contractCountByDimension": {
                    dimension: sum(row["records"] for row in records if row["dimension"] == dimension)
                    for dimension in dimensions
                },
                "valid": bool(records),
            },
            "limitations": limitations
            + [
                "Ubicación de la entidad, lugar de ejecución y procedencia del proveedor permanecen separados.",
                "El dataset de contratos no publica municipio/departamento de ejecución estructurado; no se equipara la dirección libre con DIVIPOLA.",
                "La procedencia territorial del proveedor no está estructurada en los conjuntos oficiales consultados; no se infiere desde nombres o documentos.",
                "No se publica ni descarga el conjunto crudo en el navegador.",
            ],
        }
    if status != "current":
        write_json(
            CACHE / f"secop-{DATASET}-failed-update.json",
            {
                "failedAt": now(),
                "candidate": candidate,
                "retainedPublishedVersion": output.exists(),
            },
        )
        print(
            f"SECOP: actualización no promovida ({len(records)} agregados; "
            f"{len(limitations)} fallos); se conserva la última versión válida"
        )
        return
    write_json(output, candidate)
    print(f"SECOP: {len(records)} agregados reales; estado {status}")


if __name__ == "__main__":
    if "--compact-existing" in sys.argv:
        compact_existing()
    else:
        run("--offline" in sys.argv)
