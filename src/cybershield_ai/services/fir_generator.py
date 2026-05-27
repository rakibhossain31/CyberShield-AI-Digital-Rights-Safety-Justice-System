from __future__ import annotations

from cybershield_ai.core.models import IncidentReport, ClassificationResult, RiskResult, RetrievedGuidance
from typing import List


def generate_complaint_draft(
    report: IncidentReport,
    redacted_statement: str,
    classification: ClassificationResult,
    risk: RiskResult,
    guidance: List[RetrievedGuidance],
) -> str:
    evidence = ", ".join(report.evidence_items) if report.evidence_items else "Evidence items to be attached or uploaded for review."
    guidance_titles = "; ".join([g.title for g in guidance]) if guidance else "General cyber safety guidance"
    location = report.location or "[Location to be confirmed]"
    platform = report.platform or "[Platform/channel to be confirmed]"
    incident_date = report.incident_date or "[Date/time to be confirmed]"

    return f"""
DRAFT CYBER INCIDENT COMPLAINT FOR HUMAN REVIEW

Important: This is an automatically generated draft for review by a qualified human support worker, lawyer, or authorized officer. It is not legal advice and is not automatically submitted anywhere.

1. Reporter Alias
{report.reporter_alias}

2. Incident Category Suggested by System
{classification.category} (confidence: {classification.confidence})

3. Priority Suggested by System
{risk.priority.upper()} (risk score: {risk.risk_score}/100)

4. Incident Location / Jurisdiction Context
{location}

5. Platform or Communication Channel
{platform}

6. Incident Date or Discovery Date
{incident_date}

7. Statement of Facts
{redacted_statement}

8. Evidence Mentioned
{evidence}

9. Suggested Review Checklist
- Confirm victim identity and consent for next steps.
- Verify incident timeline and preserve original evidence.
- Review screenshots, URLs, chat exports, logs, and account identifiers.
- Confirm whether urgent protection, legal aid, or platform takedown support is needed.
- Validate the legal category and complaint language before submission.

10. Retrieved Guidance Used for Drafting Context
{guidance_titles}

11. Human Review Required
This draft must be reviewed before being used as a complaint, FIR-style statement, legal notice, or support document.
""".strip()
