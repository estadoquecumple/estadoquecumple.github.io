import json
import time
import uuid
from collections import defaultdict, deque
from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from sqlalchemy import text
from sqlalchemy.orm import Session
from services.shared.config import settings
from services.shared.db import session_scope

cfg = settings()
started = time.monotonic()
requests_by_client: dict[str, deque[float]] = defaultdict(deque)

class ScenarioInput(BaseModel):
    name: str = Field(min_length=1, max_length=160)
    units: list[str] = Field(min_length=1, max_length=200)
    assumptions: dict = Field(default_factory=dict)

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(title="Laboratorio Territorial V4 API", version="2.0.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=cfg.origins, allow_credentials=False, allow_methods=["GET", "POST"], allow_headers=["Content-Type", "X-Request-ID"])

@app.middleware("http")
async def security(request: Request, call_next):
    request_id = request.headers.get("x-request-id", str(uuid.uuid4()))[:80]
    content_length = request.headers.get("content-length")
    if content_length and int(content_length) > cfg.lab_max_upload_bytes:
        return JSONResponse({"error": {"code": "payload_too_large", "request_id": request_id}}, status_code=413)
    client = request.client.host if request.client else "unknown"
    now = time.monotonic()
    recent = requests_by_client[client]
    while recent and recent[0] < now - 60:
        recent.popleft()
    if len(recent) >= 120:
        return JSONResponse({"error": {"code": "rate_limited", "request_id": request_id}}, status_code=429)
    recent.append(now)
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    print(json.dumps({"event": "request", "request_id": request_id, "method": request.method, "path": request.url.path, "status": response.status_code}))
    return response

def db_session():
    yield from session_scope()

def page(limit: int = Query(50, ge=1, le=200), offset: int = Query(0, ge=0)):
    return limit, offset

@app.get("/health")
def health():
    return {"status": "ok", "uptime_seconds": round(time.monotonic() - started, 3)}

@app.get("/ready")
def ready(db: Session = Depends(db_session)):
    db.execute(text("SELECT 1"))
    extensions = dict(db.execute(text("SELECT extname,extversion FROM pg_extension WHERE extname IN ('postgis','vector')")).all())
    return {"status": "ready", "database": "ok", "extensions": extensions}

def listing(db, table, columns, paging, q=None):
    limit, offset = paging
    allowed = {"sources", "datasets", "territorial_units", "entities", "indicators"}
    if table not in allowed:
        raise ValueError("tabla no permitida")
    where, params = "", {"limit": limit, "offset": offset}
    if q:
        where, params["q"] = " WHERE lower(coalesce(name,'')) LIKE lower(:q)", f"%{q}%"
    rows = db.execute(text(f"SELECT {columns} FROM {table}{where} ORDER BY created_at LIMIT :limit OFFSET :offset"), params).mappings().all()
    return {"items": [dict(row) for row in rows], "limit": limit, "offset": offset}

@app.get("/v1/catalog/sources")
def sources(paging=Depends(page), db: Session = Depends(db_session)): return listing(db, "sources", "id,source_key,name,quality_status,metadata", paging)
@app.get("/v1/catalog/datasets")
def datasets(paging=Depends(page), db: Session = Depends(db_session)): return listing(db, "datasets", "id,dataset_key,name,quality_status", paging)
@app.get("/v1/territories")
def territories(
    q: str | None = Query(None, max_length=100),
    name: str | None = Query(None, max_length=100),
    level: str | None = Query(None, pattern="^(department|local)$"),
    type: str | None = Query(None, max_length=80),
    department: str | None = Query(None, pattern=r"^\d{2}$"),
    divipola: str | None = Query(None, pattern=r"^\d{2,5}$"),
    paging=Depends(page),
    db: Session = Depends(db_session),
):
    limit, offset = paging
    clauses, params = [], {"limit": limit, "offset": offset}
    if q or name:
        clauses.append("lower(name) LIKE lower(:name)")
        params["name"] = f"%{name or q}%"
    if level:
        clauses.append("level=:level")
        params["level"] = level
    if type:
        clauses.append("(lower(normalized_type)=lower(:type) OR lower(literal_type)=lower(:type))")
        params["type"] = type
    if department:
        clauses.append("(canonical_code=:department OR (level='local' AND left(canonical_code,2)=:department))")
        params["department"] = department
    if divipola:
        clauses.append("canonical_code=:divipola")
        params["divipola"] = divipola
    where = f" WHERE {' AND '.join(clauses)}" if clauses else ""
    rows = db.execute(text(f"""SELECT id,canonical_code,name,unit_type,level,literal_type,
      normalized_type,department_id,quality_status
      FROM territorial_units{where} ORDER BY canonical_code LIMIT :limit OFFSET :offset"""), params).mappings()
    return {"items": [dict(row) for row in rows], "limit": limit, "offset": offset}
@app.get("/v1/entities")
def entities(q: str | None = Query(None, max_length=100), paging=Depends(page), db: Session = Depends(db_session)): return listing(db, "entities", "id,name,quality_status,metadata", paging, q)
@app.get("/v1/indicators")
def indicators(paging=Depends(page), db: Session = Depends(db_session)): return listing(db, "indicators", "id,indicator_key,name,quality_status", paging)

@app.get("/v1/territories/{territory_id}")
def territory(territory_id: uuid.UUID, db: Session = Depends(db_session)):
    row = db.execute(text("""SELECT id,canonical_code,name,unit_type,level,literal_type,
      normalized_type,department_id,quality_status FROM territorial_units WHERE id=:id"""), {"id": territory_id}).mappings().first()
    if not row: raise HTTPException(404, detail={"code": "not_found", "message": "Territorio no encontrado"})
    return dict(row)

@app.get("/v1/legal/search")
def legal(q: str = Query(..., min_length=2, max_length=100), paging=Depends(page), db: Session = Depends(db_session)):
    limit, offset = paging
    rows = db.execute(text("SELECT id,name,metadata FROM legal_instruments WHERE lower(name) LIKE lower(:q) LIMIT :limit OFFSET :offset"), {"q": f"%{q}%", "limit": limit, "offset": offset}).mappings()
    return {"items": [dict(x) for x in rows], "limit": limit, "offset": offset}

@app.post("/v1/scenarios/compile")
def compile_scenario(payload: ScenarioInput):
    missing = [unit for unit in payload.units if not unit.strip()]
    return {"valid": not missing, "errors": [{"code": "empty_unit"} for _ in missing], "capsule": {"input": payload.model_dump(), "compiled_at": time.time()}}

@app.post("/v1/scenarios/run", status_code=202)
def run_scenario(payload: ScenarioInput, db: Session = Depends(db_session)):
    key = str(uuid.uuid5(uuid.NAMESPACE_URL, json.dumps(payload.model_dump(), sort_keys=True)))
    job = db.execute(text("""INSERT INTO jobs(kind,payload,idempotency_key,max_attempts,timeout_seconds)
      VALUES('scenario',CAST(:payload AS jsonb),:key,:attempts,:timeout)
      ON CONFLICT(idempotency_key) DO UPDATE SET updated_at=now() RETURNING id,state"""),
      {"payload": payload.model_dump_json(), "key": key, "attempts": cfg.lab_job_max_attempts, "timeout": cfg.lab_job_timeout_seconds}).mappings().one()
    run = db.execute(text("""INSERT INTO scenario_runs(job_id,state,capsule)
      SELECT :job,'queued',CAST(:capsule AS jsonb) WHERE NOT EXISTS(SELECT 1 FROM scenario_runs WHERE job_id=:job)
      RETURNING id"""), {"job": job["id"], "capsule": payload.model_dump_json()}).scalar()
    if run is None: run = db.execute(text("SELECT id FROM scenario_runs WHERE job_id=:job"), {"job": job["id"]}).scalar_one()
    db.commit()
    return {"run_id": run, "job_id": job["id"], "state": str(job["state"])}

@app.get("/v1/scenarios/{run_id}")
def scenario(run_id: uuid.UUID, db: Session = Depends(db_session)):
    row = db.execute(text("""SELECT r.id,r.state,r.capsule,j.progress,j.error FROM scenario_runs r JOIN jobs j ON j.id=r.job_id WHERE r.id=:id"""), {"id": run_id}).mappings().first()
    if not row: raise HTTPException(404, detail={"code": "not_found", "message": "Ejecución no encontrada"})
    return dict(row)

@app.get("/v1/scenarios/{run_id}/artifacts")
def artifacts(run_id: uuid.UUID, db: Session = Depends(db_session)):
    rows = db.execute(text("SELECT id,path,sha256,size_bytes FROM scenario_artifacts WHERE run_id=:id"), {"id": run_id}).mappings()
    return {"items": [dict(row) for row in rows]}

@app.post("/v1/jobs/{job_id}/cancel", status_code=202)
def cancel(job_id: uuid.UUID, db: Session = Depends(db_session)):
    state = db.execute(text("""UPDATE jobs SET state=CASE WHEN state='queued' THEN 'cancelled'::job_state ELSE 'cancel_requested'::job_state END,updated_at=now()
      WHERE id=:id AND state IN ('queued','running') RETURNING state"""), {"id": job_id}).scalar()
    if state is None: raise HTTPException(409, detail={"code": "not_cancellable", "message": "Trabajo inexistente o terminado"})
    db.commit()
    return {"job_id": job_id, "state": str(state)}
