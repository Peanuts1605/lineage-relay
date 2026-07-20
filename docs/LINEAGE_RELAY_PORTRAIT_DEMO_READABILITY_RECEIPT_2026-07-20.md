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

- Drive: pending initial verified mirror.
- Notion pointer: pending.

## Next Action

Keep Lineage Relay stable and use the readable portrait proof when publishing
the public demo video.
