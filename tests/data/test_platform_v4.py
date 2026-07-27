from __future__ import annotations

import json

import pytest

from scripts.territorial import platform_v4
from scripts.territorial.build_v4_foundation import publication_commit
from scripts.territorial.fetch_secop import aggregate_query, metadata_fields, normalize_aggregate, resolve_fields
from scripts.territorial.fetch_sgr import aggregate_rows
from scripts.territorial.platform_v4 import (
    SourceCatalog,
    create_snapshot,
    representative_point,
    validate_aggregates,
    validate_territorial_types,
)


def test_catalog_rejects_duplicate_ids():
    source = {
        "id": "official-source",
        "entity": "Entidad",
        "url": "https://example.gov.co/data",
        "access": "público",
        "frequency": "anual",
        "data_date": None,
        "published_at": None,
        "downloaded_at": None,
        "coverage": "nacional",
        "granularity": "municipio",
        "key": "DIVIPOLA",
        "license": "datos abiertos",
        "fields": ["code"],
        "transformations": ["normalización"],
        "limitations": ["ninguna"],
        "update_policy": "validar",
        "status": "current",
        "quality_status": "current",
        "hash": None,
        "snapshot": None,
        "published_version": "1",
        "last_valid_version": "1",
    }
    with pytest.raises(ValueError, match="duplicados"):
        SourceCatalog.model_validate({"version": "4", "updated": "2026-07-26", "sources": [source, source]})


def test_foundation_prefers_github_publication_sha(monkeypatch):
    commit = "1234567890abcdef1234567890abcdef12345678"
    monkeypatch.setenv("GITHUB_SHA", commit)
    assert publication_commit() == commit


def test_pandera_validates_equivalent_catalog_aggregates_and_types():
    validate_territorial_types(
        [{"code": "05001", "departmentCode": "05", "name": "Medellín", "type": "Municipio", "areaName": None, "creationYear": None, "creationResolution": None}]
    )
    frame = validate_aggregates([{"source": "secop-ii", "records": 2, "value": 100.0, "resultType": "calculated"}])
    assert frame.iloc[0]["records"] == 2
    with pytest.raises(Exception):
        validate_aggregates([{"source": "secop-ii", "records": -1, "value": 100.0, "resultType": "calculated"}])


def test_snapshot_is_immutable_and_only_promotes_valid_quality(tmp_path, monkeypatch):
    monkeypatch.setattr(platform_v4, "SNAPSHOTS", tmp_path / "snapshots")
    monkeypatch.setattr(platform_v4, "CURRENT", tmp_path / "current")
    monkeypatch.setattr(platform_v4, "HISTORY", tmp_path / "history")
    raw = tmp_path / "raw.json"
    normalized = tmp_path / "normalized.json"
    raw.write_text('{"official":true}', encoding="utf-8")
    normalized.write_text('{"records":[]}', encoding="utf-8")
    rejected = create_snapshot("source", [raw], [normalized], {"valid": False}, promote=True)
    assert rejected.promoted is False
    assert not (tmp_path / "current" / "source.json").exists()
    accepted = create_snapshot("source", [raw], [normalized], {"valid": True}, promote=True)
    pointer = json.loads((tmp_path / "current" / "source.json").read_text(encoding="utf-8"))
    assert accepted.promoted is True
    assert pointer["rawHash"] == accepted.raw_hash
    assert create_snapshot("source", [raw], [normalized], {"valid": True}, promote=True).snapshot_id == accepted.snapshot_id


def test_representative_point_is_inside_concave_polygon():
    geometry = {"type": "Polygon", "coordinates": [[[0, 0], [4, 0], [4, 1], [1, 1], [1, 4], [0, 4], [0, 0]]]}
    x, y = representative_point(geometry)
    assert (x <= 1 and y <= 4) or (x <= 4 and y <= 1)


def test_sgr_deduplicates_bpin_and_reports_value_coverage():
    rows = [
        {"bpin": "1", "departamento": "Antioquia", "municipio": "Medellín", "sector": "Salud", "estado": "Aprobado", "ejecutor": "E1", "valor_total": "100"},
        {"bpin": "1", "departamento": "Antioquia", "municipio": "Medellín", "sector": "Salud", "estado": "Aprobado", "ejecutor": "E1", "valor_total": "100"},
        {"bpin": "2", "departamento": "Antioquia", "municipio": "Medellín", "sector": "Salud", "estado": "Aprobado", "ejecutor": "E1"},
    ]
    records, quality = aggregate_rows(rows)
    assert quality == {
        "inputRows": 3,
        "uniqueProjects": 2,
        "duplicateBpinRows": 1,
        "rowsWithoutBpin": 0,
        "aggregatedProjectCount": 2,
        "valid": True,
    }
    assert records[0]["records"] == 2
    assert records[0]["valueCoverage"] == 1


def test_secop_resolves_metadata_and_paginates_aggregates():
    metadata = {"columns": [{"fieldName": "nombre_entidad"}, {"fieldName": "departamento"}, {"fieldName": "valor_del_contrato"}]}
    fields = resolve_fields(metadata_fields(metadata))
    assert fields["entity"] == "nombre_entidad"
    assert fields["value"] == "valor_del_contrato"
    calls = []

    def fetch(_url, params):
        calls.append(params)
        return [{"entity": "Alcaldía", "records": "2", "value": "30"}]

    rows = aggregate_query([("entity", "nombre_entidad")], "valor_del_contrato", fetch=fetch)
    normalized = normalize_aggregate(rows, "contracting-entity")
    assert normalized[0]["records"] == 2
    assert normalized[0]["value"] == 30
    assert calls[0]["$group"] == "`nombre_entidad`"
