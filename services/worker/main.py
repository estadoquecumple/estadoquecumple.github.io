import hashlib
import json
import os
import socket
import time
from pathlib import Path
from sqlalchemy import text
from services.shared.db import engine

WORKER = f"{socket.gethostname()}-{os.getpid()}"

def recover():
    with engine.begin() as db:
        db.execute(text("""UPDATE jobs SET state='queued',locked_by=NULL,locked_at=NULL,
          available_at=now(),updated_at=now() WHERE state='running'
          AND locked_at < now() - make_interval(secs => timeout_seconds)"""))

def claim():
    with engine.begin() as db:
        return db.execute(text("""WITH candidate AS (
          SELECT id FROM jobs WHERE state='queued' AND available_at<=now()
          ORDER BY created_at FOR UPDATE SKIP LOCKED LIMIT 1)
          UPDATE jobs j SET state='running',locked_by=:worker,locked_at=now(),
          attempts=attempts+1,progress=1,updated_at=now() FROM candidate
          WHERE j.id=candidate.id RETURNING j.id,j.payload,j.attempts,j.max_attempts"""), {"worker": WORKER}).mappings().first()

def execute(job):
    run_id = None
    with engine.begin() as db:
        run_id = db.execute(text("SELECT id FROM scenario_runs WHERE job_id=:id"), {"id": job["id"]}).scalar()
        cancelled = db.execute(text("SELECT state='cancel_requested' FROM jobs WHERE id=:id"), {"id": job["id"]}).scalar()
        if cancelled:
            db.execute(text("UPDATE jobs SET state='cancelled',progress=0,updated_at=now() WHERE id=:id"), {"id": job["id"]})
            return
        payload = dict(job["payload"])
        if payload.get("force_failure"):
            raise RuntimeError("fallo controlado para comprobar reintentos")
        artifact = json.dumps({"status": "succeeded", "scenario": payload}, ensure_ascii=False).encode()
        vault = Path(os.getenv("LAB_VAULT_PATH", "/vault")) / "scenarios" / str(run_id)
        vault.mkdir(parents=True, exist_ok=True)
        target = vault / "result.json"
        target.write_bytes(artifact)
        digest = hashlib.sha256(artifact).hexdigest()
        db.execute(text("""INSERT INTO scenario_artifacts(run_id,path,sha256,size_bytes,quality_status)
          VALUES(:run,:path,:sha,:size,'valid')"""), {"run": run_id, "path": str(target), "sha": digest, "size": len(artifact)})
        db.execute(text("UPDATE jobs SET state='succeeded',progress=100,result=:result,updated_at=now() WHERE id=:id"),
                   {"id": job["id"], "result": json.dumps({"artifact_sha256": digest})})
        db.execute(text("UPDATE scenario_runs SET state='succeeded',updated_at=now() WHERE id=:run"), {"run": run_id})
        db.execute(text("""INSERT INTO job_events(job_id,event_type,payload,quality_status)
          VALUES(:id,'succeeded',jsonb_build_object('worker',CAST(:worker AS text)),'valid')"""),
          {"id": job["id"], "worker": WORKER})

def fail(job, exc):
    with engine.begin() as db:
        retry = job["attempts"] < job["max_attempts"]
        db.execute(text("""UPDATE jobs SET state=CAST(:state AS job_state),error=:error,
          available_at=now()+make_interval(secs => LEAST(60,power(2,attempts)::int)),
          locked_by=NULL,locked_at=NULL,updated_at=now() WHERE id=:id"""),
          {"id": job["id"], "state": "queued" if retry else "failed", "error": str(exc)[:1000]})

def main():
    while True:
        recover()
        job = claim()
        if not job:
            time.sleep(1)
            continue
        try: execute(job)
        except Exception as exc: fail(job, exc)

if __name__ == "__main__":
    main()
