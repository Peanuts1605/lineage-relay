# Lineage Relay Portrait Demo Readability Receipt

- Receipt ID: `LINEAGE-RELAY-PORTRAIT-DEMO-READABILITY-2026-07-20`
- Agent: `ORION_L`
- Date: `2026-07-20`
- Status: `PASS_WITH_PATCH`
- Decision: `KEEP_PRODUCT_BEHAVIOR_FROZEN`

## Artifact

- [Portrait demo readability patch](LINEAGE_RELAY_PORTRAIT_DEMO_READABILITY_PATCH_2026-07-20.md)
- [Live Forge portrait proof](../demo/frames/04-portrait-needs-owner-readable.png)

## Proof

- The original issue was reproduced from the 1008 x 1208 submitted portrait
  walkthrough: a long receipt ID extended the decision panel beyond the frame.
- `app/static/styles.css` now allows receipt content to shrink and wraps the
  identifier safely.
- `app/static/index.html` serves `styles.css?v=20260720n`.
- The patch is committed and pushed as `2763be5`.
- Forge served the new root markup and CSS after the atomic static-file update.
- Pytest passed: `6 passed in 0.60s`.

## Product Learning

- Decision: presentation defects that crop the proof state are product defects,
  even when the underlying engine is correct.
- Strongest evidence: a rendered capture at the target video viewport, not a
  source-code assumption.
- Transfer rule: validate the exact demo viewport after dynamic identifiers
  render; flex layouts can look correct until real evidence strings arrive.

## Shared Proof Reconciliation

- Drive: `TMN_NAUMIO_HQ/06_DELIVERY/LINEAGE-RELAY-PORTRAIT-DEMO-READABILITY-2026-07-20/`
  - Initial verified mirror: `20260720T170353568Z`
  - Patch-note SHA-256:
    `dcb8517bda473d46308a904777f0b53c9279c2d961b10ed86111d3cbcad5f00c`
  - Portrait proof SHA-256:
    `84a43e713255b399559c21711dc042d94382ce856924c67e35b876d768e02cd1`
- Notion pointer: [Lineage Relay Portrait Demo Readability](https://app.notion.com/p/3a3b143d29178161a9c6e9a981b04950)

This receipt was patched after the initial Drive verification and Notion
readback. The reconciled receipt is mirrored again with its append-only
portfolio checkpoint.

## Next Action

Keep Lineage Relay stable and use the readable portrait proof when publishing
the public demo video.
