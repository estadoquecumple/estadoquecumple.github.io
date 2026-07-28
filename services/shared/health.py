import json
import os
import urllib.request

url = os.getenv("LAB_HEALTH_URL", "http://api:8000/ready")
with urllib.request.urlopen(url, timeout=10) as response:
    body = json.load(response)
    if response.status != 200 or body.get("status") != "ready":
        raise SystemExit(1)
    print(json.dumps(body))
