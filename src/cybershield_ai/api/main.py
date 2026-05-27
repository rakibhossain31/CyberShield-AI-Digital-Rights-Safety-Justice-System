from __future__ import annotations

import os
import uuid
from typing import Optional

from contextlib import asynccontextmanager
from fastapi import FastAPI, Header, HTTPException

from cybershield_ai.core import database
from cybershield_ai.core.models import IncidentReport, EvidenceTextRequest, FeedbackRequest
from cybershield_ai.services.victim_advocate import VictimAdvocate
from cybershield_ai.services.evidence_vault import EvidenceVault
from cybershield_ai.monitoring.pattern_monitor import build_pattern_report

DB_PATH = os.getenv("CYBERSHIELD_DB_PATH", database.DEFAULT_DB_PATH)
API_KEY = os.getenv("CYBERSHIELD_API_KEY")

@asynccontextmanager
async def lifespan(app: FastAPI):
    database.init_db(DB_PATH)
    yield


app = FastAPI(
    title="CyberShield AI API",
    description="Safe demo API for cyber incident triage, evidence hashing, and monitoring.",
    version="1.0.0",
    lifespan=lifespan,
)


def check_api_key(x_api_key: Optional[str]) -> None:
    if API_KEY and x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")


@app.get("/health")
def health():
    return {"status": "ok", "mode": "safe_demo", "db_path": DB_PATH}


@app.post("/triage")
def triage(report: IncidentReport, x_api_key: Optional[str] = Header(default=None)):
    check_api_key(x_api_key)
    service = VictimAdvocate(db_path=DB_PATH)
    return service.triage(report)


@app.post("/evidence/text")
def add_text_evidence(request: EvidenceTextRequest, x_api_key: Optional[str] = Header(default=None)):
    check_api_key(x_api_key)
    vault = EvidenceVault(db_path=DB_PATH)
    return vault.add_text_evidence(
        case_id=request.case_id,
        evidence_name=request.evidence_name,
        evidence_text=request.evidence_text,
        collector_alias=request.collector_alias,
    )


@app.get("/case/{case_id}")
def get_case(case_id: str, x_api_key: Optional[str] = Header(default=None)):
    check_api_key(x_api_key)
    case = database.get_case(DB_PATH, case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case


@app.get("/patterns")
def patterns(x_api_key: Optional[str] = Header(default=None)):
    check_api_key(x_api_key)
    return build_pattern_report(DB_PATH)


@app.post("/feedback")
def feedback(request: FeedbackRequest, x_api_key: Optional[str] = Header(default=None)):
    check_api_key(x_api_key)
    row = request.model_dump()
    row["feedback_id"] = str(uuid.uuid4())
    row["timestamp_utc"] = database.utc_now()
    database.insert_feedback(DB_PATH, row)
    database.audit(DB_PATH, "feedback_logged", request.case_id, {"rating": request.rating, "useful": request.useful})
    return row


@app.get("/dashboard/summary")
def dashboard_summary(x_api_key: Optional[str] = Header(default=None)):
    check_api_key(x_api_key)
    return database.summary(DB_PATH)
