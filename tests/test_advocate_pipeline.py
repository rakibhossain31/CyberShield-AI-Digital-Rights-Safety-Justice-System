from cybershield_ai.core.models import IncidentReport
from cybershield_ai.services.victim_advocate import VictimAdvocate


def test_advocate_pipeline(tmp_path):
    service = VictimAdvocate(db_path=str(tmp_path / "test.db"))
    report = IncidentReport(
        reporter_alias="demo",
        statement="Someone is sending repeated abusive messages and threats on social media.",
        platform="facebook",
        suspect_identifier="@demo_suspect",
        evidence_items=["screenshot.png"],
    )
    result = service.triage(report)
    assert result.case_id
    assert result.category in {"harassment", "blackmail", "hacking", "impersonation", "doxxing", "financial_fraud", "other"}
    assert result.human_review_required is True
    assert "human" in result.disclaimer.lower()
