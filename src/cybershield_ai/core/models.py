from __future__ import annotations

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class IncidentReport(BaseModel):
    reporter_alias: str = Field(default="anonymous")
    statement: str = Field(..., min_length=10)
    location: Optional[str] = None
    platform: Optional[str] = None
    incident_date: Optional[str] = None
    suspect_identifier: Optional[str] = None
    evidence_items: List[str] = Field(default_factory=list)
    wants_legal_aid: bool = False
    immediate_danger: bool = False


class ClassificationResult(BaseModel):
    category: str
    confidence: float
    matched_terms: List[str] = Field(default_factory=list)
    explanation: str


class RiskResult(BaseModel):
    risk_score: int
    priority: str
    escalation_reasons: List[str] = Field(default_factory=list)


class RetrievedGuidance(BaseModel):
    title: str
    content: str
    score: float


class TriageResult(BaseModel):
    case_id: str
    category: str
    confidence: float
    risk_score: int
    priority: str
    redacted_statement: str
    matched_terms: List[str]
    guidance: List[RetrievedGuidance]
    complaint_draft: str
    awareness_tips: List[str]
    repeat_pattern_count: int
    anonymized_suspect_key: Optional[str] = None
    human_review_required: bool = True
    disclaimer: str


class EvidenceTextRequest(BaseModel):
    case_id: str
    evidence_name: str
    evidence_text: str
    collector_alias: str = "demo_user"


class EvidenceRecord(BaseModel):
    evidence_id: str
    case_id: str
    evidence_name: str
    evidence_hash: str
    chain_hash: str
    timestamp_utc: str
    collector_alias: str


class FeedbackRequest(BaseModel):
    case_id: str
    reviewer_alias: str = "reviewer"
    rating: int = Field(ge=1, le=5)
    useful: bool = True
    notes: Optional[str] = None


class FeedbackRecord(BaseModel):
    feedback_id: str
    case_id: str
    reviewer_alias: str
    rating: int
    useful: bool
    notes: Optional[str] = None
    timestamp_utc: str
