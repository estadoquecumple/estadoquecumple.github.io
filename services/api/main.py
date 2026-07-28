import json
import time
import uuid
import zipfile
from collections import defaultdict, deque
from contextlib import asynccontextmanager
from fastapi import Body, Depends, FastAPI, File, HTTPException, Query, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from sqlalchemy import text
from sqlalchemy.orm import Session
from services.shared.config import settings
from services.shared.db import session_scope
from services.shared.anomalies import review_cases
from services.shared.documents import UnsafeDocument, inspect_and_extract
from services.shared.graph import ALLOWED_RELATIONS, neighborhood
from services.shared.optimization import optimize
from services.shared.resolution import normalize_name, resolve_candidates

cfg = settings()
started = time.monotonic()
requests_by_client: dict[str, deque[float]] = defaultdict(deque)

class ScenarioInput(BaseModel):
    name: str = Field(min_length=1, max_length=160)
    units: list[str] = Field(min_length=1, max_length=200)
    assumptions: dict = Field(default_factory=dict)

class EdgeInput(BaseModel):
    source_node_id: uuid.UUID
    target_node_id: uuid.UUID
    relation_type: str
    valid_from: str
    valid_to: str | None = None
    source_id: uuid.UUID
    evidence: dict
    confidence: float = Field(ge=0, le=1)
    method: str = Field(min_length=2, max_length=100)

class ResolutionInput(BaseModel):
    raw_name: str = Field(min_length=2, max_length=300)
    official_identifier: str | None = Field(None, max_length=100)
    identifier_type: str | None = Field(None, max_length=50)

class ResolutionDecision(BaseModel):
    decision: str = Field(pattern="^(approved|rejected)$")
    rationale: str = Field(min_length=3, max_length=1000)
    decided_by: str = Field(min_length=2, max_length=100)

class OptimizationInput(BaseModel):
    optimization_type: str = Field(pattern="^(contiguous_regions|service_location|capacity_distribution|competence_assignment|institutional_transition)$")
    inputs: dict
    queued: bool = False

class CitationInput(BaseModel):
    fragment_id: uuid.UUID
    cited_by_type: str = Field(min_length=2, max_length=80)
    cited_by_id: uuid.UUID | None = None
    quote: str = Field(min_length=1, max_length=2000)

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

@app.get("/v1/graph/nodes")
def graph_nodes(node_type: str | None = None, q: str | None = Query(None, max_length=100),
                paging=Depends(page), db: Session = Depends(db_session)):
    limit, offset = paging
    clauses, params = [], {"limit": limit, "offset": offset}
    if node_type:
        clauses.append("node_type=:node_type"); params["node_type"] = node_type
    if q:
        clauses.append("lower(name) LIKE lower(:q)"); params["q"] = f"%{q}%"
    where = f" WHERE {' AND '.join(clauses)}" if clauses else ""
    rows = db.execute(text(f"""SELECT id,node_type,canonical_key,name,properties,valid_from,valid_to,
      source_id,quality_status FROM graph_nodes{where} ORDER BY node_type,name LIMIT :limit OFFSET :offset"""), params).mappings()
    return {"items": [dict(row) for row in rows], "limit": limit, "offset": offset}

@app.get("/v1/graph/nodes/{node_id}/neighborhood")
def graph_neighborhood(node_id: uuid.UUID, at: str | None = None, depth: int = Query(2, ge=1, le=5),
                       db: Session = Depends(db_session)):
    if not db.execute(text("SELECT 1 FROM graph_nodes WHERE id=:id"), {"id": node_id}).scalar():
        raise HTTPException(404, detail={"code": "not_found", "message": "Nodo no encontrado"})
    return neighborhood(db, node_id, at, depth)

@app.post("/v1/graph/relations", status_code=201)
def create_relation(payload: EdgeInput, db: Session = Depends(db_session)):
    if payload.relation_type not in ALLOWED_RELATIONS:
        raise HTTPException(422, detail={"code": "invalid_relation"})
    edge_id = db.execute(text("""INSERT INTO graph_edges(
      source_node_id,target_node_id,relation_type,valid_from,valid_to,source_id,evidence,
      confidence,method,review_status)
      VALUES(:source,:target,:relation,CAST(:start AS timestamptz),CAST(:end AS timestamptz),
      :source_id,CAST(:evidence AS jsonb),:confidence,:method,'pending') RETURNING id"""),
      {"source": payload.source_node_id, "target": payload.target_node_id,
       "relation": payload.relation_type, "start": payload.valid_from, "end": payload.valid_to,
       "source_id": payload.source_id, "evidence": json.dumps(payload.evidence, ensure_ascii=False),
       "confidence": payload.confidence, "method": payload.method}).scalar_one()
    db.commit()
    return {"id": edge_id, "review_status": "pending"}

@app.post("/v1/graph/relations/{edge_id}/review")
def review_relation(edge_id: uuid.UUID, decision: str = Body(embed=True, pattern="^(approved|rejected)$"),
                    db: Session = Depends(db_session)):
    state = db.execute(text("""UPDATE graph_edges SET review_status=:decision,updated_at=now()
      WHERE id=:id RETURNING review_status"""), {"id": edge_id, "decision": decision}).scalar()
    if state is None:
        raise HTTPException(404, detail={"code": "not_found"})
    db.commit()
    return {"id": edge_id, "review_status": state}

@app.post("/v1/entities/resolve")
def resolve_entity(payload: ResolutionInput, db: Session = Depends(db_session)):
    candidates = resolve_candidates(db, payload.raw_name, payload.official_identifier, payload.identifier_type)
    stored = []
    for candidate in candidates:
        candidate_id = db.execute(text("""INSERT INTO entity_resolution_candidates(
          raw_name,normalized_name,official_identifier,identifier_type,candidate_node_id,
          score,method,status,evidence)
          VALUES(:raw,:normalized,:official,:identifier,:node,:score,:method,'pending',
          jsonb_build_object('band',CAST(:band AS text))) RETURNING id"""),
          {"raw": payload.raw_name, "normalized": normalize_name(payload.raw_name),
           "official": payload.official_identifier, "identifier": payload.identifier_type,
           "node": candidate["id"], "score": candidate["score"], "method": candidate["method"],
           "band": candidate["band"]}).scalar_one()
        stored.append({**candidate, "candidate_id": candidate_id})
    db.commit()
    return {"normalized_name": normalize_name(payload.raw_name), "candidates": stored,
            "automatic_merge": False}

@app.post("/v1/entities/resolution/{candidate_id}/decision")
def decide_entity(candidate_id: uuid.UUID, payload: ResolutionDecision, db: Session = Depends(db_session)):
    if not db.execute(text("SELECT 1 FROM entity_resolution_candidates WHERE id=:id"), {"id": candidate_id}).scalar():
        raise HTTPException(404, detail={"code": "not_found"})
    previous = db.execute(text("""SELECT id FROM entity_resolution_decisions WHERE candidate_id=:id
      ORDER BY decided_at DESC LIMIT 1"""), {"id": candidate_id}).scalar()
    decision_id = db.execute(text("""INSERT INTO entity_resolution_decisions(
      candidate_id,decision,rationale,decided_by,previous_decision_id)
      VALUES(:candidate,:decision,:rationale,:actor,:previous) RETURNING id"""),
      {"candidate": candidate_id, "decision": payload.decision, "rationale": payload.rationale,
       "actor": payload.decided_by, "previous": previous}).scalar_one()
    db.execute(text("UPDATE entity_resolution_candidates SET status=:decision WHERE id=:id"),
               {"id": candidate_id, "decision": payload.decision})
    db.commit()
    return {"id": decision_id, "decision": payload.decision, "versioned": True}

@app.post("/v1/optimization/runs")
def run_optimization(payload: OptimizationInput, db: Session = Depends(db_session)):
    if payload.queued:
        key = str(uuid.uuid5(uuid.NAMESPACE_URL, json.dumps(payload.model_dump(), sort_keys=True)))
        job = db.execute(text("""INSERT INTO jobs(kind,payload,idempotency_key,max_attempts,timeout_seconds)
          VALUES('optimization',CAST(:payload AS jsonb),:key,:attempts,:timeout)
          ON CONFLICT(idempotency_key) DO UPDATE SET updated_at=now() RETURNING id,state"""),
          {"payload": payload.model_dump_json(), "key": key, "attempts": cfg.lab_job_max_attempts,
           "timeout": cfg.lab_job_timeout_seconds}).mappings().one()
        db.commit()
        return {"job_id": job["id"], "state": str(job["state"])}
    result = optimize(payload.optimization_type, payload.inputs)
    run_id = db.execute(text("""INSERT INTO optimization_runs(
      optimization_type,state,input,formulation,solver,solver_version,seed,duration_ms,
      solution,alternatives,infeasibility,sensitivity,result_kind)
      VALUES(:type,:state,CAST(:input AS jsonb),CAST(:formulation AS jsonb),:solver,:version,
      :seed,:duration,CAST(:solution AS jsonb),CAST(:alternatives AS jsonb),
      CAST(:infeasibility AS jsonb),CAST(:sensitivity AS jsonb),:kind) RETURNING id"""),
      {"type": payload.optimization_type, "state": result["status"],
       "input": json.dumps(payload.inputs), "formulation": json.dumps(result.get("formulation", {})),
       "solver": result.get("solver", "OR-Tools CP-SAT"), "version": result.get("solver_version", "unknown"),
       "seed": result.get("seed", payload.inputs.get("seed", 42)), "duration": result.get("duration_ms"),
       "solution": json.dumps(result.get("solution")), "alternatives": json.dumps(result.get("alternatives", [])),
       "infeasibility": json.dumps(result.get("infeasibility")),
       "sensitivity": json.dumps(result.get("sensitivity", {})), "kind": result["result_kind"]}).scalar_one()
    db.commit()
    return {"id": run_id, **result}

@app.post("/v1/review-cases/analyze")
def analyze_cases(records: list[dict], db: Session = Depends(db_session)):
    cases = review_cases(records)
    for case in cases:
        db.execute(text("""INSERT INTO review_cases(method,subject_type,subject_key,metric,
          observed_value,score,explanation,evidence)
          VALUES(:method,'record',:subject,'value',:value,:score,:explanation,'{}')"""),
          {"method": case["method"], "subject": case["subject_key"], "value": case["observed_value"],
           "score": case["score"], "explanation": case["explanation"]})
    db.commit()
    return {"items": cases, "label": "caso para revisar"}

@app.post("/v1/documents", status_code=201)
async def upload_document(file: UploadFile = File(...), source_url: str | None = None,
                          db: Session = Depends(db_session)):
    data = await file.read(cfg.lab_max_upload_bytes + 1)
    try:
        extracted = inspect_and_extract(file.filename or "document", file.content_type or "", data)
    except (UnsafeDocument, UnicodeDecodeError, ValueError, zipfile.BadZipFile) as exc:
        raise HTTPException(422, detail={"code": "unsafe_document", "message": str(exc)}) from exc
    document_id = db.execute(text("""INSERT INTO documents(
      original_name,safe_name,media_type,size_bytes,sha256,source_url,extraction_status,security_findings,metadata)
      VALUES(:original,:safe,:media,:size,:sha,:url,'extracted',CAST(:findings AS jsonb),
      jsonb_build_object('instruction_policy','documents_are_data')) ON CONFLICT(sha256)
      DO UPDATE SET original_name=excluded.original_name RETURNING id"""),
      {"original": file.filename, "safe": extracted["safe_name"], "media": extracted["media_type"],
       "size": extracted["size_bytes"], "sha": extracted["sha256"], "url": source_url,
       "findings": json.dumps(extracted["security_findings"], ensure_ascii=False)}).scalar_one()
    for fragment in extracted["fragments"]:
        db.execute(text("""INSERT INTO document_fragments(
          document_id,ordinal,page,line_start,line_end,text,sha256)
          VALUES(:document,:ordinal,:page,:start,:end,:text,:sha)
          ON CONFLICT(document_id,ordinal) DO NOTHING"""),
          {"document": document_id, "ordinal": fragment["ordinal"], "page": fragment["page"],
           "start": fragment["line_start"], "end": fragment["line_end"], "text": fragment["text"],
           "sha": fragment["sha256"]})
    db.commit()
    return {"id": document_id, **extracted}

@app.get("/v1/documents/{document_id}/fragments")
def document_fragments(document_id: uuid.UUID, db: Session = Depends(db_session)):
    rows = db.execute(text("""SELECT id,ordinal,page,line_start,line_end,text,sha256,result_kind
      FROM document_fragments WHERE document_id=:id ORDER BY ordinal"""), {"id": document_id}).mappings()
    return {"items": [dict(row) for row in rows]}

@app.post("/v1/citations", status_code=201)
def create_citation(payload: CitationInput, db: Session = Depends(db_session)):
    fragment = db.execute(text("""SELECT text,sha256,page,line_start,line_end,document_id
      FROM document_fragments WHERE id=:id"""), {"id": payload.fragment_id}).mappings().first()
    if not fragment:
        raise HTTPException(404, detail={"code": "fragment_not_found"})
    if payload.quote not in fragment["text"]:
        raise HTTPException(422, detail={"code": "quote_not_in_fragment"})
    citation_id = db.execute(text("""INSERT INTO citations(fragment_id,cited_by_type,cited_by_id,quote)
      VALUES(:fragment,:type,:target,:quote) RETURNING id"""),
      {"fragment": payload.fragment_id, "type": payload.cited_by_type,
       "target": payload.cited_by_id, "quote": payload.quote}).scalar_one()
    db.commit()
    return {"id": citation_id, "fragment_id": payload.fragment_id, "document_id": fragment["document_id"],
            "page": fragment["page"], "line_start": fragment["line_start"],
            "line_end": fragment["line_end"], "fragment_sha256": fragment["sha256"],
            "quote": payload.quote}
