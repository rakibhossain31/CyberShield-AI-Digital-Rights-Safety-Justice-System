from __future__ import annotations

from typing import List
from cybershield_ai.core.models import IncidentReport, ClassificationResult, RiskResult

URGENT_TERMS = ["tonight", "kill", "suicide", "physical harm", "leak", "deadline", "pay now", "come to my house"]
HIGH_RISK_CATEGORIES = {"blackmail", "doxxing", "hacking"}


def score_risk(report: IncidentReport, classification: ClassificationResult, repeat_count: int = 0) -> RiskResult:
    text = report.statement.lower()
    score = 20
    reasons: List[str] = []

    if classification.category in HIGH_RISK_CATEGORIES:
        score += 25
        reasons.append(f"Category '{classification.category}' is treated as higher risk in the demo policy.")

    urgent_hits = [t for t in URGENT_TERMS if t in text]
    if urgent_hits:
        score += 25
        reasons.append("Urgent terms detected: " + ", ".join(urgent_hits))

    if report.immediate_danger:
        score += 30
        reasons.append("Reporter indicated immediate danger.")

    if len(report.evidence_items) >= 2:
        score += 10
        reasons.append("Multiple evidence items were reported.")

    if report.wants_legal_aid:
        score += 5
        reasons.append("Reporter requested legal aid support.")

    if repeat_count > 1:
        score += min(20, repeat_count * 5)
        reasons.append(f"Anonymized suspect key appears in {repeat_count} cases.")

    score = max(0, min(score, 100))
    if score >= 75:
        priority = "urgent"
    elif score >= 45:
        priority = "medium"
    else:
        priority = "standard"

    if not reasons:
        reasons.append("No urgent escalation indicator was detected, but human review is still required.")

    return RiskResult(risk_score=score, priority=priority, escalation_reasons=reasons)
