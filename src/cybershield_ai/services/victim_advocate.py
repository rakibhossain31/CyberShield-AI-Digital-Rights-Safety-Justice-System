from __future__ import annotations

import uuid
from typing import Optional

from cybershield_ai.core import database
from cybershield_ai.core.models import IncidentReport, TriageResult
from cybershield_ai.core.security import redact_text
from cybershield_ai.services.case_classifier import classify_case
from cybershield_ai.services.risk_scorer import score_risk
from cybershield_ai.services.legal_rag import LegalRAGEngine
from cybershield_ai.services.fir_generator import generate_complaint_draft
from cybershield_ai.services.awareness import AwarenessEngine
from cybershield_ai.services.offender_graph import register_pattern

DISCLAIMER = (
    "CyberShield AI is a safe demo and decision-support prototype. Outputs are not legal advice, "
    "do not determine guilt, and must be reviewed by a qualified human before any action."
)


class VictimAdvocate:
    def __init__(
        self,
        db_path: str = database.DEFAULT_DB_PATH,
        knowledge_path: str = "data/demo/legal_knowledge.md",
        awareness_path: str = "data/demo/awareness_guidance.json",
    ):
        self.db_path = db_path
        database.init_db(db_path)
        self.rag = LegalRAGEngine(knowledge_path)
        self.awareness = AwarenessEngine(awareness_path)

    def triage(self, report: IncidentReport, case_id: Optional[str] = None) -> TriageResult:
        case_id = case_id or f"CS-{uuid.uuid4().hex[:10].upper()}"
        redacted = redact_text(report.statement)
        classification = classify_case(redacted)
        suspect_key, repeat_count = register_pattern(self.db_path, report.suspect_identifier, classification.category)
        risk = score_risk(report, classification, repeat_count=repeat_count)
        guidance = self.rag.retrieve(redacted + " " + classification.category, k=3)
        complaint = generate_complaint_draft(report, redacted, classification, risk, guidance)
        tips = self.awareness.tips_for(classification.category)

        result = TriageResult(
            case_id=case_id,
            category=classification.category,
            confidence=classification.confidence,
            risk_score=risk.risk_score,
            priority=risk.priority,
            redacted_statement=redacted,
            matched_terms=classification.matched_terms,
            guidance=guidance,
            complaint_draft=complaint,
            awareness_tips=tips,
            repeat_pattern_count=repeat_count,
            anonymized_suspect_key=suspect_key,
            human_review_required=True,
            disclaimer=DISCLAIMER,
        )

        database.insert_case(
            self.db_path,
            {
                "case_id": result.case_id,
                "created_at": database.utc_now(),
                "reporter_alias": report.reporter_alias,
                "category": result.category,
                "confidence": result.confidence,
                "risk_score": result.risk_score,
                "priority": result.priority,
                "redacted_statement": result.redacted_statement,
                "platform": report.platform,
                "location": report.location,
                "anonymized_suspect_key": result.anonymized_suspect_key,
                "repeat_pattern_count": result.repeat_pattern_count,
                "complaint_draft": result.complaint_draft,
                "payload": result.model_dump(),
            },
        )
        database.audit(self.db_path, "case_triaged", result.case_id, {"category": result.category, "priority": result.priority})
        return result
