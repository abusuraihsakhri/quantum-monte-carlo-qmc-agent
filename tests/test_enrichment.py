"""
Automated Pytest for quantum-monte-carlo-qmc-agent Enrichment Modules.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from enrichment import (
    QuantumAmplitudeEstimationForFinancialOptionPricingEngine,
    ImplementationEngine,
    FilesToCreatemodifyEngine,
    TestingEngine,
    QuantumMonteCarloForPortfolioRiskAnalysisEngine,
    QuantummontecarloqmcagentEnrichmentSuite,
    enrichment_suite,
)

def test_enrichment_suite_execution():
    suite = QuantummontecarloqmcagentEnrichmentSuite()
    res = suite.execute_all(primary_val=0.5, secondary_val=0.2)
    assert len(res) == 5  # Verify all 5 unique engines are present
    expected_keys = {
        "QuantumAmplitudeEstimationForFinancialOptionPricingEngine",
        "ImplementationEngine",
        "FilesToCreatemodifyEngine",
        "TestingEngine",
        "QuantumMonteCarloForPortfolioRiskAnalysisEngine",
    }
    assert set(res.keys()) == expected_keys
    for k, v in res.items():
        assert v.status in ["OPTIMAL", "WARNING", "CRITICAL_ALERT"]
        assert isinstance(v.recommendations, list)

def test_enrichment_threshold_escalation():
    suite = QuantummontecarloqmcagentEnrichmentSuite()
    res = suite.execute_all(primary_val=10.0, secondary_val=5.0)
    for k, v in res.items():
        assert v.status in ["WARNING", "CRITICAL_ALERT"]
        assert len(v.alerts) > 0

def test_enrichment_suite_no_duplicate_results():
    """Verify that the enrichment suite produces exactly 5 unique results (no duplicates)."""
    suite = QuantummontecarloqmcagentEnrichmentSuite()
    res = suite.execute_all(primary_val=1.5, secondary_val=0.5)
    assert len(res) == 5
    # Verify all keys are unique (no duplicates from repeated assignments)
    assert len(set(res.keys())) == len(res)
