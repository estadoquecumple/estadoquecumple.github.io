import hashlib
import json
import os
import socket
import time
from pathlib import Path
from sqlalchemy import text
from services.shared.db import engine
from services.shared.optimization import optimize

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
        if payload.get("optimization_type"):
            result = optimize(payload["optimization_type"], payload.get("inputs", {}))
            optimization_id = db.execute(text("""INSERT INTO optimization_runs(
              optimization_type,state,input,formulation,solver,solver_version,seed,duration_ms,
              solution,alternatives,infeasibility,sensitivity,result_kind)
              VALUES(:type,:state,CAST(:input AS jsonb),CAST(:formulation AS jsonb),:solver,:version,
              :seed,:duration,CAST(:solution AS jsonb),CAST(:alternatives AS jsonb),
              CAST(:infeasibility AS jsonb),CAST(:sensitivity AS jsonb),:kind) RETURNING id"""),
              {"type": payload["optimization_type"], "state": result["status"],
               "input": json.dumps(payload.get("inputs", {})),
               "formulation": json.dumps(result.get("formulation", {})),
               "solver": result.get("solver", "OR-Tools CP-SAT"),
               "version": result.get("solver_version", "unknown"), "seed": result.get("seed", 42),
               "duration": result.get("duration_ms"), "solution": json.dumps(result.get("solution")),
               "alternatives": json.dumps(result.get("alternatives", [])),
               "infeasibility": json.dumps(result.get("infeasibility")),
               "sensitivity": json.dumps(result.get("sensitivity", {})),
               "kind": result["result_kind"]}).scalar_one()
            db.execute(text("""UPDATE jobs SET state='succeeded',progress=100,
              result=jsonb_build_object('optimization_run_id',CAST(:run AS text),'status',CAST(:status AS text)),
              updated_at=now() WHERE id=:id"""),
              {"id": job["id"], "run": optimization_id, "status": result["status"]})
            db.execute(text("""INSERT INTO job_events(job_id,event_type,payload,quality_status)
              VALUES(:id,'optimization_succeeded',jsonb_build_object('worker',CAST(:worker AS text)),'valid')"""),
              {"id": job["id"], "worker": WORKER})
            return
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
