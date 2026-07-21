# Lineage Relay Ordered MCP Trace Guard

- Date: 2026-07-21
- Owner: ORION_L
- Contest: DataHub Agent Hackathon
- Decision: `FIXED_AND_PUBLIC`

## Problem

Lineage Relay uses DataHub MCP field-level paths as evidence for downstream
impact. The parser previously required the requested source and target fields to
appear in a returned path, but it did not require them to appear in downstream
order. A path returned as `target -> source` could therefore be described as a
valid downstream trace.

## Correction

`parse_lineage_path_response` now rejects any first path where the requested
source is not earlier than the requested target. The failure is explicit:
`DataHub MCP returned a path in the wrong downstream direction.`

The public README now states the same contract: a trace counts only when it
contains the requested fields in downstream order; reversed or incomplete paths
are not evidence.

## Proof

- Regression test: `test_rejects_a_reversed_field_path`.
- Before the parser change, that test failed because no exception was raised.
- After the parser change: `8 passed` via `.venv/bin/python -m pytest tests -q`.
- Compilation: `.venv/bin/python -m compileall -q app scripts` passed.
- Whitespace check: `git diff --check` passed.
- Public source commit: [`8dbaa45`](https://github.com/Peanuts1605/lineage-relay/commit/8dbaa45bfd3e4293b88d81eb6551477e61e9dc1a).
- Remote `main` was read back at the same commit.

## Judge Impact

The result keeps the product claim honest: `NEEDS_OWNER`, `READY`, and
`BLOCKED_BY_GOVERNANCE` are driven by evidence that is directionally consistent
with the requested downstream change, not merely by matching field names.

## Scope

This is a parser and documentation correction only. It does not change the
synthetic fixture, DataHub MCP configuration, decision policy, public video, or
entrant-registration state.

## Transfer Rule

When a product treats graph traversal as evidence, validate direction as well
as node membership before turning the trace into a decision or public claim.
