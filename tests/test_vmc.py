"""Numerical and audit-integrity regression tests."""
import math

import pytest

from qmc_simulator.vmc import run_vmc
from agents.base import AuditTrail


def test_harmonic_ground_state_zero_variance():
    output = run_vmc(alpha=1.0, samples=500, burn_in=100, seed=123)
    assert output.energy == pytest.approx(0.5, abs=1e-14)
    assert output.standard_error == pytest.approx(0, abs=1e-14)
    assert output.analytic_energy == pytest.approx(0.5)
    assert 0 < output.acceptance_rate < 1


def test_seeded_vmc_reproducible_and_near_analytic():
    a = run_vmc(alpha=0.8, samples=20_000, burn_in=2_000, seed=42)
    b = run_vmc(alpha=0.8, samples=20_000, burn_in=2_000, seed=42)
    assert a == b
    assert abs(a.energy - a.analytic_energy) < max(0.03, 6 * a.standard_error)
    assert a.energy >= 0.49


@pytest.mark.parametrize("kwargs", [
    {"alpha": 0}, {"alpha": math.nan}, {"proposal": math.inf},
    {"samples": 2}, {"samples": 1_000_001}, {"seed": -1},
    {"burn_in": -1},
])
def test_reject_bad_vmc_inputs(kwargs):
    with pytest.raises(ValueError):
        run_vmc(**kwargs)


def test_audit_signature_detects_hash_or_payload_changes():
    trail = AuditTrail(secret_key="test-key")
    trail.log("tester", "operator", "RUN", {"count": 1})
    trail.log("tester", "operator", "RUN", {"count": 2})
    assert trail.verify_integrity()

    external = trail.get_trail()
    external[0]["event_type"] = "CHANGED"
    assert trail.verify_integrity()  # callers cannot modify the ledger

    trail.logs[1]["payload_hash"] = "0" * 64
    assert not trail.verify_integrity()
    trail.logs[1]["payload_hash"] = "f" * 64
    assert not trail.verify_integrity()
