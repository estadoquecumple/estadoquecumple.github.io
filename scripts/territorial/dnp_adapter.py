"""Adaptador conservador DNP: descubre descargas oficiales sin automatizar Power BI."""
from __future__ import annotations

import re
import urllib.parse
import urllib.request
from pathlib import Path

from common import ROOT, USER_AGENT, now, sha256, write_json

DOWNLOAD_EXTENSIONS = (".csv", ".xlsx", ".xls", ".zip", ".json", ".parquet")


def discover_downloads(page_url: str, html: str) -> list[str]:
    urls = []
    for value in re.findall(r"""(?:href|src)=["']([^"'#]+)["']""", html, flags=re.IGNORECASE):
        absolute = urllib.parse.urljoin(page_url, value)
        path = urllib.parse.urlparse(absolute).path.lower()
        if absolute.startswith("https://") and path.endswith(DOWNLOAD_EXTENSIONS):
            urls.append(absolute)
    return sorted(set(urls))


def fetch_page(page_url: str) -> tuple[str, list[str]]:
    request = urllib.request.Request(page_url, headers={"User-Agent": USER_AGENT, "Accept": "text/html"})
    with urllib.request.urlopen(request, timeout=60) as response:
        html = response.read().decode(response.headers.get_content_charset() or "utf-8", errors="replace")
    return html, discover_downloads(page_url, html)


def archive_download(source_id: str, url: str) -> Path:
    filename = Path(urllib.parse.urlparse(url).path).name
    if not filename or not filename.lower().endswith(DOWNLOAD_EXTENSIONS):
        raise ValueError("La URL no apunta a un formato de datos permitido")
    target = ROOT / "data" / "cache" / "dnp" / source_id / filename
    target.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=120) as response:
        target.write_bytes(response.read())
    write_json(
        target.with_suffix(target.suffix + ".manifest.json"),
        {"sourceId": source_id, "url": url, "downloadedAt": now(), "sha256": sha256(target), "bytes": target.stat().st_size},
    )
    return target
