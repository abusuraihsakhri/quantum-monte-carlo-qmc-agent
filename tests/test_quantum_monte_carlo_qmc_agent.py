"""
Automated Pytest Test Suite for Quantum Monte Carlo Qmc Agent.
Domain: Post-Quantum Cryptography & Hardware Security
Standard: NIST FIPS 203/204/205 / ISO/IEC 17825 Standards
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import math
import os
import tempfile
import pytest
from agents.base import PHIGuard, AuditLogger, SecurityException
from agents.models import SystemTaskPayload, UrgencyLevel, SystemIntegrityStatus
from agents.workers import InvariantQCWorker, SafetyEscalationWorker, ProtocolConformanceWorker
from agents.supervisor import SystemSupervisor
from cli import main


def test_phi_guard_enforcement():
    with pytest.raises(SecurityException):
        PHIGuard.assert_no_phi("Patient MRN-994827 blood culture positive for Staphylococcus")

    # Clean text passes
    PHIGuard.assert_no_phi("Analytical assay specimen KEY-001 optimal")


def test_specialized_workers():
    # Worker 1: QC Invariant
    p1 = SystemTaskPayload(task_id="T1", target_identifier="KEY-01", primary_metric=35.0)
    alerts1 = InvariantQCWorker.evaluate(p1)
    assert len(alerts1) == 1
    assert alerts1[0].urgency == UrgencyLevel.ELEVATED

    # Worker 2: Safety
    p2 = SystemTaskPayload(task_id="T2", target_identifier="KEY-02", primary_metric=10.0, is_critical_flag=True)
    alerts2 = SafetyEscalationWorker.evaluate(p2)
    assert len(alerts2) == 1
    assert alerts2[0].urgency == UrgencyLevel.CRITICAL_STAT

    # Worker 3: Protocol Conformance
    p3 = SystemTaskPayload(task_id="T3", target_identifier="KEY-03", primary_metric=10.0, status_descriptor="DISCORDANT_ANOMALY")
    alerts3 = ProtocolConformanceWorker.evaluate(p3)
    assert len(alerts3) == 1


def test_supervisor_consensus_and_audit():
    supervisor = SystemSupervisor(model_provider="mock")
    payload = SystemTaskPayload(
        task_id="TASK-PROD-01",
        target_identifier="KEY-PROD-01",
        primary_metric=12.0,
        secondary_metric=4.0,
        status_descriptor="NOMINAL"
    )
    dossier = supervisor.process_task(payload)
    assert dossier.overall_urgency == UrgencyLevel.ROUTINE
    assert dossier.integrity_status == SystemIntegrityStatus.VALIDATED
    assert dossier.audit_hash != ""

    # Verify cryptographic audit trail
    assert AuditLogger.verify_integrity() is True

    # CLI tests
    assert main(["audit", "--task-id", "CLI-TEST-01"]) == 0
    assert main(["chat", "Explain", "specifications"]) == 0
    assert main(["verify-audit"]) == 0


def test_input_validation_nan_infinity():
    """Test that NaN and infinity values are rejected."""
    with pytest.raises(ValueError, match="finite"):
        SystemTaskPayload(task_id="T1", target_identifier="KEY-01", primary_metric=float("nan"))

    with pytest.raises(ValueError, match="finite"):
        SystemTaskPayload(task_id="T1", target_identifier="KEY-01", primary_metric=float("inf"))

    with pytest.raises(ValueError, match="finite"):
        SystemTaskPayload(task_id="T1", target_identifier="KEY-01", primary_metric=10.0, secondary_metric=float("-inf"))


def test_input_validation_empty_identifiers():
    """Test that empty identifiers are rejected."""
    with pytest.raises(ValueError, match="empty"):
        SystemTaskPayload(task_id="", target_identifier="KEY-01", primary_metric=10.0)

    with pytest.raises(ValueError, match="empty"):
        SystemTaskPayload(task_id="T1", target_identifier="", primary_metric=10.0)

    with pytest.raises(ValueError, match="empty"):
        SystemTaskPayload(task_id="   ", target_identifier="KEY-01", primary_metric=10.0)


def test_batch_processing_file_not_found():
    """Test that batch processing handles missing files gracefully."""
    result = main(["batch", "-i", "nonexistent_file.csv"])
    assert result == 1


def test_batch_processing_with_malformed_csv():
    """Test that batch processing handles malformed CSV gracefully."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write("task_id,target_identifier,primary_metric\n")
        f.write("T1,KEY-01,invalid_number\n")  # Invalid float
        f.write("T2,KEY-02,15.0\n")  # Valid row
        temp_path = f.name

    try:
        result = main(["batch", "-i", temp_path, "-o", "test_output.csv"])
        assert result == 0
        # Clean up output file
        if os.path.exists("test_output.csv"):
            os.remove("test_output.csv")
    finally:
        os.remove(temp_path)


def test_phi_redaction():
    """Test that PHI is properly redacted."""
    text_with_phi = "Patient MRN-123456 has phone 555-123-4567"
    redacted = PHIGuard.redact_phi(text_with_phi)
    assert "MRN-123456" not in redacted
    assert "555-123-4567" not in redacted
    assert "[REDACTED_IDENTIFIER]" in redacted
