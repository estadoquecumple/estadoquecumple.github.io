"""Fundación reproducible V4: catálogo, calidad, snapshots y productos analíticos."""
from __future__ import annotations

import hashlib
import json
import os
import shutil
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any, Iterable

import geopandas as gpd
import h3
import pandas as pd
import pandera.pandas as pa
import yaml
from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator
from shapely.geometry import shape

from common import PUBLIC, ROOT, now, read_json, sha256, write_json

DATA = ROOT / "data"
SNAPSHOTS = DATA / "snapshots"
CATALOG = DATA / "catalog"
PUBLIC_CATALOG = PUBLIC / "catalog"
CURRENT = PUBLIC / "current"
HISTORY = PUBLIC / "history"
ANALYTICS = PUBLIC / "analytics"

QUALITY_STATES = {"current", "stale", "partial", "manual-required", "unavailable"}


class SourceDefinition(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(pattern=r"^[a-z0-9][a-z0-9-]+$")
    entity: str = Field(min_length=2)
    url: HttpUrl
    access: str
    frequency: str
    data_date: str | None = None
    published_at: str | None = None
    downloaded_at: str | None = None
    coverage: str
    granularity: str
    key: str
    license: str
    fields: list[str]
    transformations: list[str]
    limitations: list[str]
    update_policy: str
    status: str
    quality_status: str
    hash: str | None = None
    snapshot: str | None = None
    published_version: str | None = None
    last_valid_version: str | None = None

    @field_validator("status", "quality_status")
    @classmethod
    def valid_status(cls, value: str) -> str:
        if value not in QUALITY_STATES:
            raise ValueError(f"estado no permitido: {value}")
        return value

    @field_validator("hash")
    @classmethod
    def valid_hash(cls, value: str | None) -> str | None:
        if value is not None and (len(value) != 64 or any(c not in "0123456789abcdef" for c in value)):
            raise ValueError("hash debe ser SHA-256 hexadecimal")
        return value


class SourceCatalog(BaseModel):
    model_config = ConfigDict(extra="forbid")
    version: str
    updated: date
    sources: list[SourceDefinition]

    @field_validator("sources")
    @classmethod
    def unique_ids(cls, sources: list[SourceDefinition]) -> list[SourceDefinition]:
        ids = [source.id for source in sources]
        if len(ids) != len(set(ids)):
            raise ValueError("IDs de fuente duplicados")
        return sources


CATALOG_FRAME_SCHEMA = pa.DataFrameSchema(
    {
        "id": pa.Column(str, unique=True, nullable=False),
        "entity": pa.Column(str, pa.Check.str_length(min_value=2), nullable=False),
        "url": pa.Column(str, pa.Check.str_startswith("https://"), nullable=False),
        "status": pa.Column(str, pa.Check.isin(sorted(QUALITY_STATES)), nullable=False),
        "quality_status": pa.Column(str, pa.Check.isin(sorted(QUALITY_STATES)), nullable=False),
        "granularity": pa.Column(str, pa.Check.str_length(min_value=2), nullable=False),
        "license": pa.Column(str, pa.Check.str_length(min_value=2), nullable=False),
    },
    strict=False,
    coerce=True,
)

TERRITORIAL_TYPES_SCHEMA = pa.DataFrameSchema(
    {
        "code": pa.Column(str, pa.Check.str_matches(r"^\d{5}$"), unique=True, nullable=False),
        "departmentCode": pa.Column(str, pa.Check.str_matches(r"^\d{2}$"), nullable=False),
        "name": pa.Column(str, pa.Check.str_length(min_value=1), nullable=False),
        "type": pa.Column(str, pa.Check.str_length(min_value=1), nullable=False),
        "areaName": pa.Column(object, nullable=True),
        "creationYear": pa.Column(object, nullable=True),
        "creationResolution": pa.Column(object, nullable=True),
    },
    strict=False,
    coerce=True,
)

AGGREGATE_SCHEMA = pa.DataFrameSchema(
    {
        "source": pa.Column(str, nullable=False),
        "records": pa.Column(int, pa.Check.greater_than_or_equal_to(0), nullable=False),
        "value": pa.Column(float, pa.Check.greater_than_or_equal_to(0), nullable=True),
        "resultType": pa.Column(str, pa.Check.isin(["observed", "calculated"]), nullable=False),
    },
    strict=False,
    coerce=True,
)


def load_catalog(path: Path = DATA / "sources.yml") -> SourceCatalog:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    catalog = SourceCatalog.model_validate(value)
    frame = pd.DataFrame(
        [
            {
                "id": source.id,
                "entity": source.entity,
                "url": str(source.url),
                "status": source.status,
                "quality_status": source.quality_status,
                "granularity": source.granularity,
                "license": source.license,
            }
            for source in catalog.sources
        ]
    )
    CATALOG_FRAME_SCHEMA.validate(frame, lazy=True)
    return catalog


def write_public_catalog(catalog: SourceCatalog) -> Path:
    PUBLIC_CATALOG.mkdir(parents=True, exist_ok=True)
    output = PUBLIC_CATALOG / "sources.json"
    write_json(
        output,
        {
            **catalog.model_dump(mode="json"),
            "generatedAt": now(),
            "policy": {
                "pricing": "100 % gratuito; sin tarjeta, suscripción ni pago por consumo",
                "defaultProviders": {"llm": "none", "embeddings": "none"},
            },
        },
    )
    return output


def stable_snapshot_id(source_id: str, raw_hash: str, normalized_hash: str = "") -> str:
    fingerprint = hashlib.sha256(f"{raw_hash}:{normalized_hash}".encode()).hexdigest()
    return f"{source_id}-{fingerprint[:16]}"


@dataclass(frozen=True)
class SnapshotResult:
    source_id: str
    snapshot_id: str
    raw_hash: str
    path: Path
    promoted: bool


def create_snapshot(
    source_id: str,
    raw_files: Iterable[Path],
    normalized_files: Iterable[Path],
    quality: dict[str, Any],
    *,
    promote: bool,
) -> SnapshotResult:
    raw_files = list(raw_files)
    normalized_files = list(normalized_files)
    if not raw_files:
        raise ValueError("Un snapshot requiere al menos un original")
    combined = hashlib.sha256()
    for path in sorted(raw_files):
        combined.update(path.name.encode("utf-8"))
        combined.update(bytes.fromhex(sha256(path)))
    raw_hash = combined.hexdigest()
    normalized_digest = hashlib.sha256()
    for path in sorted(normalized_files):
        normalized_digest.update(path.name.encode("utf-8"))
        normalized_digest.update(bytes.fromhex(sha256(path)))
    normalized_hash = normalized_digest.hexdigest()
    snapshot_id = stable_snapshot_id(source_id, raw_hash, normalized_hash)
    target = SNAPSHOTS / source_id / snapshot_id
    raw_dir = target / "raw"
    normalized_dir = target / "normalized"
    quality_dir = target / "quality"

    if target.exists():
        manifest = read_json(target / "manifest.json")
        if manifest["rawHash"] != raw_hash:
            raise RuntimeError("Colisión de snapshot: mismo ID con contenido diferente")
    else:
        raw_dir.mkdir(parents=True, exist_ok=False)
        normalized_dir.mkdir(parents=True)
        quality_dir.mkdir(parents=True)
        for path in raw_files:
            _link_or_copy(path, raw_dir / path.name)
        for path in normalized_files:
            _link_or_copy(path, normalized_dir / path.name)
        write_json(quality_dir / "results.json", quality)
        write_json(
            target / "manifest.json",
            {
                "schemaVersion": 1,
                "sourceId": source_id,
                "snapshotId": snapshot_id,
                "rawHash": raw_hash,
                "normalizedHash": normalized_hash,
                "createdAt": now(),
                "immutable": True,
                "raw": _file_manifest(raw_dir),
                "normalized": _file_manifest(normalized_dir),
                "quality": quality,
            },
        )

    promoted = bool(promote and quality.get("valid") is True)
    if promoted:
        pointer = CURRENT / f"{source_id}.json"
        previous = read_json(pointer) if pointer.exists() else None
        if previous:
            write_json(HISTORY / source_id / f"{previous['snapshotId']}.json", previous)
        try:
            manifest_path = target.relative_to(ROOT).as_posix() + "/manifest.json"
        except ValueError:
            manifest_path = str(target / "manifest.json")
        write_json(
            pointer,
            {
                "sourceId": source_id,
                "snapshotId": snapshot_id,
                "rawHash": raw_hash,
                "manifest": manifest_path,
                "promotedAt": now(),
            },
        )
    return SnapshotResult(source_id, snapshot_id, raw_hash, target, promoted)


def _file_manifest(folder: Path) -> list[dict[str, Any]]:
    return [
        {"path": path.name, "bytes": path.stat().st_size, "sha256": sha256(path)}
        for path in sorted(folder.iterdir())
        if path.is_file()
    ]


def _link_or_copy(source: Path, target: Path) -> None:
    try:
        os.link(source, target)
    except OSError:
        shutil.copy2(source, target)


def validate_territorial_types(records: list[dict[str, Any]]) -> pd.DataFrame:
    frame = pd.DataFrame(records)
    return TERRITORIAL_TYPES_SCHEMA.validate(frame, lazy=True)


def validate_aggregates(records: list[dict[str, Any]]) -> pd.DataFrame:
    frame = pd.DataFrame(records)
    return AGGREGATE_SCHEMA.validate(frame, lazy=True)


def representative_point(geometry: dict[str, Any]) -> list[float]:
    point = shape(geometry).representative_point()
    return [round(point.x, 7), round(point.y, 7)]


def write_analytics() -> list[Path]:
    ANALYTICS.mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []

    catalog = load_catalog()
    catalog_frame = pd.json_normalize(catalog.model_dump(mode="json")["sources"])
    catalog_path = ANALYTICS / "catalog.parquet"
    catalog_frame.to_parquet(catalog_path, index=False)
    outputs.append(catalog_path)

    indicator_rows: list[dict[str, Any]] = []
    for source_path in sorted((PUBLIC / "indicators").glob("*.json")):
        if source_path.name == "index.json":
            continue
        document = read_json(source_path)
        for record in document.get("records", []):
            indicator_rows.append(
                {
                    "dataset": source_path.stem,
                    "source": document.get("source"),
                    "status": document.get("status"),
                    "code": record.get("code") or record.get("territoryCode"),
                    "year": str(record.get("year") or document.get("dataPeriod") or ""),
                    "value": _numeric_value(record),
                    "record": json.dumps(record, ensure_ascii=False, sort_keys=True),
                }
            )
    indicator_frame = pd.DataFrame(
        indicator_rows,
        columns=["dataset", "source", "status", "code", "year", "value", "record"],
    )
    indicators_path = ANALYTICS / "indicators.parquet"
    indicator_frame.to_parquet(indicators_path, index=False)
    outputs.append(indicators_path)

    series_path = ANALYTICS / "series.parquet"
    indicator_frame[indicator_frame["year"].astype(str).str.len() > 0].to_parquet(
        series_path, index=False
    )
    outputs.append(series_path)

    entities = read_json(PUBLIC / "government" / "entities-by-territory.json")
    entities_path = ANALYTICS / "entities.parquet"
    pd.DataFrame(entities.get("records", [])).to_parquet(entities_path, index=False)
    outputs.append(entities_path)

    sgr = read_json(PUBLIC / "indicators" / "sgr-aggregates.json")
    sgr_path = ANALYTICS / "sgr-aggregates.parquet"
    pd.DataFrame(sgr.get("records", [])).to_parquet(sgr_path, index=False)
    outputs.append(sgr_path)

    secop_path = ANALYTICS / "secop-aggregates.parquet"
    if not secop_path.exists():
        raise FileNotFoundError("Falta el agregado SECOP Parquet completo")
    outputs.append(secop_path)

    departments = gpd.read_file(PUBLIC / "geography" / "departments.geojson")
    departments.set_crs("EPSG:4326", allow_override=True, inplace=True)
    geometry_path = ANALYTICS / "departments.geoparquet"
    departments.to_parquet(geometry_path, index=False)
    outputs.append(geometry_path)

    h3_records = build_h3_index()
    h3_path = ANALYTICS / "h3-divipola.parquet"
    pd.DataFrame(h3_records).to_parquet(h3_path, index=False)
    outputs.append(h3_path)
    write_json(ANALYTICS / "h3-divipola.json", {
        "resolution": 5,
        "legalBoundary": False,
        "warning": "H3 es una malla analítica y no reemplaza límites administrativos o legales.",
        "records": h3_records,
    })
    write_json(
        ANALYTICS / "manifest.json",
        {
            "version": "4.0.0",
            "generatedAt": now(),
            "files": [
                {"path": path.name, "bytes": path.stat().st_size, "sha256": sha256(path)}
                for path in outputs
            ],
            "fallback": "../geography/municipalities-index.json",
            "h3Warning": "H3 es una malla analítica y no reemplaza límites administrativos o legales.",
        },
    )
    return outputs


def _numeric_value(record: dict[str, Any]) -> float | None:
    for key in ("value", "totalValue", "projectValue", "population", "score"):
        value = record.get(key)
        if isinstance(value, (int, float)):
            return float(value)
    return None


def build_h3_index(resolution: int = 5) -> list[dict[str, Any]]:
    centroids = read_json(PUBLIC / "geography" / "municipality-centroids.json")
    records = []
    for item in centroids:
        lon, lat = item["coordinates"]
        records.append(
            {
                "code": item["code"],
                "resolution": resolution,
                "h3": h3.latlng_to_cell(lat, lon, resolution),
                "association": "punto representativo dentro de la geometría oficial",
                "legalBoundary": False,
            }
        )
    return records


def environment_policy() -> dict[str, str]:
    return {
        "LLM_PROVIDER": os.getenv("LLM_PROVIDER", "none"),
        "EMBEDDING_PROVIDER": os.getenv("EMBEDDING_PROVIDER", "none"),
    }
