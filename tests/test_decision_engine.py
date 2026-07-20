from app.decision_engine import ReviewEvidence, decide


def test_unowned_sensitive_dependency_needs_owner() -> None:
    decision = decide(ReviewEvidence(True, ("ml_customer_features",), True, False))
    assert decision.verdict == "NEEDS_OWNER"
    assert decision.include_executable_migration


def test_owner_assignment_makes_compatible_change_ready() -> None:
    decision = decide(ReviewEvidence(True, (), True, False))
    assert decision.verdict == "READY"
    assert decision.include_executable_migration


def test_active_governance_rule_beats_ready_state() -> None:
    decision = decide(ReviewEvidence(True, (), True, True))
    assert decision.verdict == "BLOCKED_BY_GOVERNANCE"
    assert not decision.include_executable_migration
