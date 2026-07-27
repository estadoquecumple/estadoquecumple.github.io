"""Crea snapshots sólo cuando existe un original o respuesta oficial conservada."""
from __future__ import annotations

from pathlib import Path

from common import CACHE, PUBLIC, ROOT, now, read_json, write_json
from platform_v4 import create_snapshot


def _existing(paths: list[Path]) -> list[Path]:
    return [path for path in paths if path.exists()]


def run() -> None:
    candidates = {
        "dane-divipola-mgn-2025": {
            "raw": sorted((CACHE / "dane-geography-official").glob("*.geojson")),
            "normalized": [
                PUBLIC / "geography" / "departments.geojson",
                PUBLIC / "geography" / "municipalities-index.json",
                PUBLIC / "geography" / "territorial-unit-types.json",
                PUBLIC / "geography" / "municipality-centroids.json",
            ],
        },
        "dnp-sgr-mzgh-shtp": {
            "raw": [CACHE / "sgr-mzgh-shtp-raw.json"],
            "normalized": [PUBLIC / "indicators" / "sgr-aggregates.json"],
        },
        "secop-ii": {
            "raw": sorted(CACHE.glob("secop-jbjy-vk9h-*-raw-aggregate.json")) + [CACHE / "secop-jbjy-vk9h-metadata.json"],
            "normalized": [PUBLIC / "indicators" / "secop-aggregates.json"],
        },
        "dnp-typologies-2026": {
            "raw": [ROOT / "data" / "manual" / "dnp_typologies_2026.xlsx"],
            "normalized": [PUBLIC / "indicators" / "typologies.json"],
        },
        "dnp-idf-2024": {
            "raw": [ROOT / "data" / "manual" / "dnp_idf_2024.xlsx"],
            "normalized": [PUBLIC / "indicators" / "fiscal.json"],
        },
        "dnp-mdm": {
            "raw": [ROOT / "data" / "manual" / "dnp_mdm.xlsx"],
            "normalized": [PUBLIC / "indicators" / "municipal-performance.json"],
        },
    }
    report = []
    for source_id, files in candidates.items():
        raw = _existing(files["raw"])
        normalized = _existing(files["normalized"])
        if not raw:
            report.append(
                {
                    "sourceId": source_id,
                    "status": "manual-required",
                    "promoted": False,
                    "message": "No existe original conservado; no se fabrica un snapshot.",
                }
            )
            continue
        valid = bool(normalized)
        published_status = "current"
        if normalized[0].suffix == ".json":
            published_status = read_json(normalized[0]).get("status", "current")
        result = create_snapshot(
            source_id,
            raw,
            normalized,
            {
                "valid": valid,
                "checkedAt": now(),
                "publishedStatus": published_status,
                "checks": ["original-presente", "sha256", "producto-normalizado-presente"],
            },
            promote=valid,
        )
        report.append(
            {
                "sourceId": source_id,
                "status": published_status if result.promoted else "partial",
                "snapshotId": result.snapshot_id,
                "rawHash": result.raw_hash,
                "promoted": result.promoted,
            }
        )
    write_json(PUBLIC / "catalog" / "snapshot-status.json", {"version": "4.0.0", "generatedAt": now(), "sources": report})
    print(f"Snapshots V4: {sum(item['promoted'] for item in report)} promovidos; {len(report)} fuentes evaluadas")


if __name__ == "__main__":
    run()
