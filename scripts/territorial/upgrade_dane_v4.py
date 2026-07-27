"""Actualiza productos DANE ya descargados al contrato V4 sin repetir la descarga."""
from __future__ import annotations

from collections import Counter

from common import PUBLIC, read_json, write_json


def upgrade(properties):
    literal = properties.get("MPIO_TIPO") or properties.get("type") or "Sin dato disponible"
    properties.update(
        {
            "MPIO_TIPO": literal,
            "type": literal,
            "unitType": str(literal).strip().lower(),
            "MPIO_NAREA": properties.get("MPIO_NAREA", properties.get("areaName")),
            "MPIO_NANO": properties.get("MPIO_NANO", properties.get("creationYear")),
            "MPIO_CRSLCION": properties.get("MPIO_CRSLCION", properties.get("creationResolution")),
        }
    )
    return properties


def run() -> None:
    index_path = PUBLIC / "geography" / "municipalities-index.json"
    index = [upgrade(item) for item in read_json(index_path)]
    write_json(index_path, index)
    for path in sorted((PUBLIC / "geography" / "municipalities").glob("*.geojson")):
        collection = read_json(path)
        for feature in collection["features"]:
            feature["properties"] = upgrade(feature["properties"])
        write_json(path, collection)
    counts = Counter(str(item["MPIO_TIPO"]) for item in index)
    manifest_path = PUBLIC / "geography" / "geography-manifest.json"
    manifest = read_json(manifest_path)
    manifest.update(
        {
            "territorialUnitCount": len(index),
            "municipalityCount": counts.get("MUNICIPIO", 0),
            "nonMunicipalizedAreaCount": counts.get("ÁREA NO MUNICIPALIZADA", 0),
            "typeCounts": dict(counts),
        }
    )
    write_json(manifest_path, manifest)
    print(f"DANE V4: {len(index)} unidades; tipos literales preservados")


if __name__ == "__main__":
    run()
