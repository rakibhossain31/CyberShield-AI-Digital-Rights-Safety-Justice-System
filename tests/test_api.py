import os
from fastapi.testclient import TestClient

os.environ["CYBERSHIELD_DB_PATH"] = "artifacts/test_api.db"

from cybershield_ai.api.main import app  # noqa: E402


def test_health_endpoint():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_triage_endpoint():
    client = TestClient(app)
    payload = {
        "reporter_alias": "demo",
        "statement": "A fake profile is using my photo and pretending to be me.",
        "platform": "facebook",
        "suspect_identifier": "@fake_profile"
    }
    response = client.post("/triage", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["category"] == "impersonation"
    assert data["case_id"]
