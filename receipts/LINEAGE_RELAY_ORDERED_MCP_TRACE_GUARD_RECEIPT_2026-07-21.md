# Lineage Relay Ordered MCP Trace Guard Receipt

- Receipt ID: `LINEAGE-RELAY-ORDERED-MCP-TRACE-GUARD-2026-07-21`
- Date: 2026-07-21
- Agent: ORION_L / Codex Desktop
- Status: `RECONCILED`
- Decision: `FIXED_AND_PUBLIC`

## Artifact

- Decision note:
  `docs/LINEAGE_RELAY_ORDERED_MCP_TRACE_GUARD_2026-07-21.md`
- Public source changes:
  `README.md`, `app/mcp_evidence.py`, and `tests/test_mcp_evidence.py`
- Public commit:
  <https://github.com/Peanuts1605/lineage-relay/commit/8dbaa45bfd3e4293b88d81eb6551477e61e9dc1a>

## Evidence

- An adversarial test reversed a valid field path. Before the parser change, it
  failed because Lineage Relay accepted the reversed path.
- The parser now rejects a source index that is not earlier than the target
  index with an explicit downstream-direction error.
- `.venv/bin/python -m pytest tests -q`: `8 passed`.
- `.venv/bin/python -m compileall -q app scripts`: passed.
- `git diff --check`: passed.
- `git ls-remote origin refs/heads/main` returned
  `8dbaa45bfd3e4293b88d81eb6551477e61e9dc1a`.

## Scope and Truth

- The correction keeps a reversed or incomplete DataHub MCP path from becoming
  downstream evidence.
- It does not alter the synthetic fixture, decision rules, public video, MCP
  server configuration, contest eligibility, or entrant declarations.
- Current-tool capability review: `reviewed; no route change`. This was a
  deterministic evidence-contract correction, not a feature or tooling change.

## Shared Proof Reconciliation

- Drive folder:
  `TMN_NAUMIO_HQ/06_DELIVERY/LINEAGE-RELAY-ORDERED-MCP-TRACE-GUARD-2026-07-21/`
  (initial mirror hash-verified the decision note, local receipt, source parser,
  test, README, and contest tracker).
- Notion pointer:
  <https://app.notion.com/p/3a4b143d291781d6a9bdc8ffeb1faa2c>
  (created in and fetched back from the TMN Receipts Ledger).
- Reconciled receipt mirror:
  `LINEAGE_RELAY_ORDERED_MCP_TRACE_GUARD_RECEIPT_2026-07-21.reconciled-20260721T182153195Z.md`
  in the named Drive folder. Its SHA-256 is
  `2cc47fde4616b7b7689f614dd2f6b18b83b99bd113c9f022e1359648547556f0`.

## Transfer Rule

Validate traversal direction as well as matching endpoints before presenting a
graph path as causal or downstream evidence.
