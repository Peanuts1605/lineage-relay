# Lineage Relay Live DataHub Replay Receipt

- Receipt ID: `LINEAGE-RELAY-LIVE-DATAHUB-REPLAY-2026-07-20`
- Date: 2026-07-20
- Agent: Orion_L / Codex Desktop
- Status: `submission_evidence_ready`
- Task: Re-run Lineage Relay against a fresh synthetic local DataHub graph,
  verify the visual decision path, and reconcile the judge-access route with
  the current official contest rules.

## Artifact

- Decision note:
  `docs/LINEAGE_RELAY_LIVE_DATAHUB_REPLAY_2026-07-20.md`
- Rendered proof:
  `demo/frames/05-live-local-needs-owner-2026-07-20.png`
  `demo/frames/06-live-local-ready-2026-07-20.png`
  `demo/frames/07-live-local-governance-2026-07-20.png`
  `demo/frames/08-live-local-mobile-2026-07-20.png`

## Verified Work

- Started Docker and a fresh synthetic DataHub Quickstart locally.
- Installed the public official `acryldata/mcp-server-datahub` package into the
  existing local virtual environment.
- Seeded the synthetic `orders`, analytics, dashboard, and ML-feature fixture.
- Requested a live review and received `NEEDS_OWNER` with three exact
  field-level MCP traces and an evidence-backed receipt.
- Exercised `NEEDS_OWNER`, `READY`, and `BLOCKED_BY_GOVERNANCE` in the visible
  review desk.
- Confirmed six project tests, compilation, no browser errors, and no 390 px
  horizontal overflow.
- Re-read the current official rules. They allow a live demo, hosted app, or
  public repository with clear setup instructions. The published repository is
  the accurate test route; no misleading hosted imitation was deployed.

## Submission Evidence Update

- Public video: <https://www.youtube.com/shorts/0HokRdSv5D4>
- YouTube Studio reported `Video published` and `No issues found` before
  publication.
- Independent HTTP verification returned 200 after redirect handling.

## Shared Proof Reconciliation

- Drive mirror: `TMN_NAUMIO_HQ/06_DELIVERY/LINEAGE-RELAY-LIVE-DATAHUB-REPLAY-2026-07-20/`
  (six files hash-verified by `mirror_shared_proof.mjs`).
- Notion pointer:
  `https://app.notion.com/p/3a3b143d291781c3803ffe527ff4c295`
  (created and fetched back from the TMN Receipts Ledger).
- Reconciled receipt mirror: pending final re-mirror after the public-video
  evidence is included.

## Transfer Rule

When a contest accepts a reproducible public repository as its test route,
do not create an unreliable hosted imitation just to satisfy a visual instinct.
Prove the genuine stack, make the setup easy, and spend the final surface work
on the public video and submission clarity.
