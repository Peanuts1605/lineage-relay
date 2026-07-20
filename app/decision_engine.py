from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ReviewEvidence:
    source_is_sensitive: bool
    missing_owner_assets: tuple[str, ...]
    compatibility_actions_present: bool
    active_governance_block: bool


@dataclass(frozen=True)
class Decision:
    verdict: str
    reason: str
    include_executable_migration: bool


def decide(evidence: ReviewEvidence) -> Decision:
    if evidence.active_governance_block:
        return Decision(
            verdict="BLOCKED_BY_GOVERNANCE",
            reason="The active governance rule forbids removal while a downstream dependency remains.",
            include_executable_migration=False,
        )
    if evidence.source_is_sensitive and evidence.missing_owner_assets:
        return Decision(
            verdict="NEEDS_OWNER",
            reason=f"Sensitive downstream use has no accountable owner: {', '.join(evidence.missing_owner_assets)}.",
            include_executable_migration=True,
        )
    if evidence.compatibility_actions_present:
        return Decision(
            verdict="READY",
            reason="Every affected dependency has an owner and the compatibility path is present.",
            include_executable_migration=True,
        )
    return Decision(
        verdict="BLOCKED_BY_GOVERNANCE",
        reason="The compatibility path is incomplete, so removing the original field is not reviewable.",
        include_executable_migration=False,
    )
