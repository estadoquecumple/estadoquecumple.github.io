import re
import unicodedata
from rapidfuzz.fuzz import ratio
from sqlalchemy import text


def normalize_name(value: str) -> str:
    value = unicodedata.normalize("NFKD", value.casefold())
    value = "".join(char for char in value if not unicodedata.combining(char))
    return " ".join(re.sub(r"[^a-z0-9]+", " ", value).split())


def resolve_candidates(db, raw_name, official_identifier=None, identifier_type=None, limit=5):
    normalized = normalize_name(raw_name)
    rows = db.execute(text("""
      SELECT id,name,canonical_key,properties FROM graph_nodes
      WHERE node_type IN ('entity','organization','body','territory')
      ORDER BY name
    """)).mappings()
    ranked = []
    for row in rows:
        identifiers = row["properties"].get("identifiers", {}) if row["properties"] else {}
        exact_identifier = bool(official_identifier and identifiers.get(identifier_type) == official_identifier)
        exact_name = normalize_name(row["name"]) == normalized
        score = 1.0 if exact_identifier else 0.98 if exact_name else ratio(normalized, normalize_name(row["name"])) / 100
        method = "official_identifier" if exact_identifier else "normalized_exact" if exact_name else "rapidfuzz"
        if score >= 0.60:
            ranked.append({**dict(row), "score": score, "method": method,
                           "band": "high" if score >= .90 else "medium" if score >= .75 else "low"})
    return sorted(ranked, key=lambda item: (-item["score"], item["name"]))[:limit]
