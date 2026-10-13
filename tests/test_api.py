"""HTTP contract and unsupported model-provider regression checks."""
import pytest
from fastapi.testclient import TestClient

from agents.api import app
from agents.llm_factory import LLMFactory

client = TestClient(app)


def test_api_health_and_valid_audit():
    health = client.get("/health")
    assert health.status_code == 200
    assert health.json()["status"] == "HEALTHY"
    resp = client.post("/api/audit", json={
        "task_id": "HTTP-001",
        "target_identifier": "LAB-001",
        "primary_metric": 30,
        "secondary_metric": 13,
        "status_descriptor": "ANOMALY",
        "is_critical_flag": True,
    })
    assert resp.status_code == 200
    body = resp.json()
    assert body["total_alerts"] == 3
    assert body["overall_urgency"] == "CRITICAL_STAT_PANIC"
    assert len(body["audit_hash"]) == 64


def test_api_rejects_sensitive_identifiers_without_tracebacks():
    rejected = client.post("/api/audit", json={
        "task_id": "MRN-123456",
        "target_identifier": "LAB-001",
        "primary_metric": 1,
    })
    assert rejected.status_code == 400
    assert "MRN-123456" not in rejected.text


def test_only_mock_llm_provider_is_available():
    with pytest.raises(ValueError, match="not implemented"):
        LLMFactory.create("openai")
    reply = LLMFactory.create("mock").invoke("Status request")
    assert "No external model or scientific validation" in reply
