"""Publica catálogo y banco analítico V4 a partir de productos ya validados."""
from __future__ import annotations

import subprocess
import os

from common import PUBLIC, ROOT, now, sha256, write_json
from platform_v4 import environment_policy, load_catalog, write_analytics, write_public_catalog


def publication_commit() -> str:
    return os.environ.get("GITHUB_SHA") or subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, capture_output=True, text=True
    ).stdout.strip()


def run() -> None:
    commit = publication_commit()
    compiler = ROOT / "src" / "data" / "territorial" / "scenario-v4.ts"
    catalog = load_catalog()
    catalog_path = write_public_catalog(catalog)
    analytics = write_analytics()
    write_json(
        PUBLIC / "current" / "foundation-v4.json",
        {
            "version": "4.0.0",
            "generatedAt": now(),
            "commit": commit,
            "catalog": {"path": catalog_path.relative_to(ROOT / "public").as_posix(), "sha256": sha256(catalog_path)},
            "analytics": [
                {"path": path.relative_to(ROOT / "public").as_posix(), "sha256": sha256(path), "bytes": path.stat().st_size}
                for path in analytics
            ],
            "rules": [{"id": "scenario-compiler-v4", "version": "4.0.0", "sha256": sha256(compiler)}],
            "providers": environment_policy(),
            "promotionPolicy": "La actualización defectuosa no sustituye la última versión válida.",
        },
    )
    print(f"V4 foundation: catálogo y {len(analytics)} productos analíticos")


if __name__ == "__main__":
    run()
