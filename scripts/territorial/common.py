"""Utilidades reproducibles del pipeline territorial CAMS (solo fuentes públicas)."""
from __future__ import annotations
import hashlib, json, time, urllib.parse, urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PUBLIC = ROOT / "public" / "data" / "territorial"
CACHE = ROOT / "data" / "cache"
USER_AGENT = "CAMS-Laboratorio-Territorial/1.0 (+https://estadoquecumple.github.io)"

def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def get_json(url: str, params: dict | None = None, retries: int = 4):
    if params:
        url += ("&" if "?" in url else "?") + urllib.parse.urlencode(params)
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(request, timeout=90) as response:
                return json.load(response)
        except Exception:
            if attempt == retries - 1:
                raise
            time.sleep(2 ** attempt)

def normalize_divipola(value, level="municipality") -> str | None:
    if value is None:
        return None
    digits = "".join(c for c in str(value).strip().split(".")[0] if c.isdigit())
    width = 2 if level == "department" else 5
    normalized = digits.zfill(width)
    return normalized if len(normalized) == width else None

def feature_collection(features, **metadata):
    return {"type": "FeatureCollection", "metadata": metadata, "features": features}
