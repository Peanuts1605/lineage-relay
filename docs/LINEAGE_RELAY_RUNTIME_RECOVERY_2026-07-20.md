# Lineage Relay Runtime Recovery

**Decision:** `PASS_WITH_PATCH`

The Forge-hosted, synthetic DataHub proof path initially returned a `503`: its
local DataHub containers were not running, so Lineage Relay correctly produced
no review package. The sandbox stack was restored, the fixture was reseeded,
and all three decision states were replayed in a browser.

## Judge-Visible Patch

The browser client previously left an earlier package and receipt visible when
a later metadata-proof request failed. It now clears the active package,
receipt, evidence hash, owner claim, and header status before showing the
unavailable state.

This prevents a false impression that a release package remains valid after
the evidence path has disappeared.

## Verification

Local recovery simulation:

- begins with a `READY` package and two tabs;
- switches to `DataHub unavailable` on a simulated `503`;
- clears the receipt to `-`, tabs to `0`, and artifact to
  `No review package was generated.`;
- changes the header from `Live DataHub + MCP evidence` to
  `Metadata proof unavailable`.

Forge synthetic replay after DataHub recovery:

| State | Result | Receipt |
| --- | --- | --- |
| Missing owner | `NEEDS OWNER` | `LR-20260720195918-ca3ed1` |
| Owner assigned | `READY` | `LR-20260720195926-905c42` |
| Governance block | `BLOCKED BY GOVERNANCE` | `LR-20260720195931-905c42` |

The browser emitted no page errors. The fixture contains synthetic names and
metadata only.

## Evidence

- `demo/frames/09-local-proof-unavailable-clears-package-2026-07-20.png`
- `demo/frames/10-forge-needs-owner-2026-07-20.png`
- `demo/frames/11-forge-ready-2026-07-20.png`
- `demo/frames/12-forge-governance-2026-07-20.png`

## Transfer Rule

When a product claims its output is evidence-backed, an evidence failure must
remove every stale decision artifact, not merely change the headline.

