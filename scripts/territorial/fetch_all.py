from __future__ import annotations
import argparse, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def run(script,*args):
    subprocess.run([sys.executable,str(ROOT/"scripts"/"territorial"/script),*args],check=True,cwd=ROOT)
if __name__=="__main__":
    parser=argparse.ArgumentParser(); parser.add_argument("--offline",action="store_true"); opts=parser.parse_args()
    geography=ROOT/"public"/"data"/"territorial"/"geography"/"geography-manifest.json"
    if not opts.offline or not geography.exists(): run("fetch_dane_geography.py")
    for name in ("fetch_dane_population.py","fetch_dnp_typologies.py","fetch_dnp_fiscal.py","fetch_dnp_mdm.py"): run(name)
    if opts.offline:
        run("fetch_sgr.py","--offline"); run("fetch_secop.py","--offline"); run("fetch_government_entities.py","--offline")
    else:
        run("fetch_sgr.py"); run("fetch_secop.py"); run("fetch_government_entities.py")
    for name in ("normalize_divipola.py","build_geography.py","build_scenarios.py","build_indicators.py","build_manifest.py","build_v4_foundation.py","snapshot_v4.py","validate_sources.py"): run(name)
