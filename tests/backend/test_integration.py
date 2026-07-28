import hashlib
import threading
import time
import uuid
from pathlib import Path
from sqlalchemy import text
from services.shared.vault import LocalFilesystemVault
from services.shared.db import engine

def test_extensions_are_real(db):
    extensions = dict(db.execute(text("SELECT extname,extversion FROM pg_extension WHERE extname IN ('postgis','vector')")).all())
    assert {"postgis", "vector"} <= extensions.keys()
    assert db.execute(text("SELECT ST_AsText(ST_Point(1,2))")).scalar() == "POINT(1 2)"
    assert db.execute(text("SELECT '[1,2,3]'::vector <-> '[1,2,4]'::vector")).scalar() == 1.0

def test_api_health_ready_and_cors(api):
    assert api.get("/health").status_code == 200
    assert api.get("/ready").json()["database"] == "ok"
    response = api.options("/v1/territories", headers={"Origin": "http://localhost:4321", "Access-Control-Request-Method": "GET"})
    assert response.headers["access-control-allow-origin"] == "http://localhost:4321"
    denied = api.options("/v1/territories", headers={"Origin": "https://evil.invalid", "Access-Control-Request-Method": "GET"})
    assert "access-control-allow-origin" not in denied.headers
    oversized = api.post("/v1/scenarios/compile", content=b"{}", headers={"content-length": "10485761"})
    assert oversized.status_code == 413
    assert oversized.json()["error"]["code"] == "payload_too_large"

def test_seed_is_idempotent(db):
    from services.shared.seed import main
    main()
    before = db.execute(text("SELECT count(*) FROM source_snapshots")).scalar()
    products_before = db.execute(text("SELECT count(*) FROM dataset_versions")).scalar()
    main()
    after = db.execute(text("SELECT count(*) FROM source_snapshots")).scalar()
    products_after = db.execute(text("SELECT count(*) FROM dataset_versions")).scalar()
    assert before == after and before > 0
    assert products_before == products_after and products_before > 0

def test_vault_immutable_integrity_and_traversal(tmp_path):
    vault = LocalFilesystemVault(str(tmp_path))
    item = vault.put("dane", "snapshot-1", "original.zip", b"official")
    assert vault.verify(item["path"])
    assert item["sha256"] == hashlib.sha256(b"official").hexdigest()
    try: vault.put("..", "snapshot-1", "x", b"bad")
    except ValueError: pass
    else: raise AssertionError("traversal aceptado")

def test_skip_locked_prevents_double_claim(db):
    key = str(uuid.uuid4())
    with engine.begin() as setup:
        job_id = setup.execute(text(
            "INSERT INTO jobs(idempotency_key,payload,state) VALUES(:key,'{}','cancelled') RETURNING id"
        ), {"key": key}).scalar_one()
    first = engine.connect()
    transaction = first.begin()
    assert first.execute(text("SELECT id FROM jobs WHERE id=:id FOR UPDATE"), {"id": job_id}).scalar_one() == job_id
    result = []
    def competing_claim():
        with engine.begin() as second:
            result.append(second.execute(text(
                "SELECT id FROM jobs WHERE id=:id FOR UPDATE SKIP LOCKED"
            ), {"id": job_id}).scalar())
    thread = threading.Thread(target=competing_claim)
    thread.start()
    thread.join()
    transaction.rollback()
    first.close()
    assert result == [None]

def test_cancellation_and_retry_state(db, api):
    with engine.begin() as setup:
        job_id = setup.execute(text("""INSERT INTO jobs(idempotency_key,payload,available_at)
          VALUES(:key,'{}',now()+interval '1 hour') RETURNING id"""),
          {"key": str(uuid.uuid4())}).scalar_one()
    cancelled = api.post(f"/v1/jobs/{job_id}/cancel")
    assert cancelled.json()["state"] == "cancelled"

def wait_for_state(job_id, expected, timeout=20):
    deadline = time.time() + timeout
    while time.time() < deadline:
        with engine.connect() as check:
            row = check.execute(text("SELECT state,attempts FROM jobs WHERE id=:id"), {"id": job_id}).one()
        if str(row.state) == expected:
            return row
        time.sleep(0.25)
    raise AssertionError(f"trabajo {job_id} no alcanzó {expected}")

def test_worker_retries_then_fails():
    with engine.begin() as setup:
        job_id = setup.execute(text("""INSERT INTO jobs(idempotency_key,payload,max_attempts)
          VALUES(:key,CAST(:payload AS jsonb),3) RETURNING id"""),
          {"key": str(uuid.uuid4()), "payload": '{"force_failure":true}'}).scalar_one()
    row = wait_for_state(job_id, "failed")
    assert row.attempts == 3

def test_worker_recovers_stale_running_job():
    with engine.begin() as setup:
        job_id = setup.execute(text("""INSERT INTO jobs(idempotency_key,payload,state,locked_at,locked_by,timeout_seconds)
          VALUES(:key,'{}','running',now()-interval '2 minutes','worker-caido',1) RETURNING id"""),
          {"key": str(uuid.uuid4())}).scalar_one()
    row = wait_for_state(job_id, "succeeded")
    assert row.attempts == 1
