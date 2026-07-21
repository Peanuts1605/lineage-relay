# Lineage Relay Public Video Reconciliation Receipt

- Receipt ID: `LINEAGE-RELAY-PUBLIC-VIDEO-RECONCILIATION-2026-07-20`
- Agent: `ORION_L`
- Date: `2026-07-20 America/New_York`
- Status: `VALID`

## Artifact and decision

- Artifact: `docs/LINEAGE_RELAY_PUBLIC_VIDEO_RECONCILIATION_2026-07-20.md`
- Decision: public demo evidence is complete; advance only the remaining
  entrant-controlled Devpost form and eligibility attestation.

## Checks

- `ffprobe` measured `demo/video/lineage-relay-forge-walkthrough-draft.mp4` at
  `49.896009` seconds.
- `curl -IL` confirmed public routes for the YouTube walkthrough and public
  GitHub repository on 2026-07-20.
- `.venv/bin/python -m pytest tests -q`: `7 passed in 0.76s` after the
  documentation update. (The repository virtual environment is required;
  system Python does not carry the app's test dependencies.)

## Historical-record handling

`LINEAGE_RELAY_FORGE_MCP_VERTICAL_SLICE_RECEIPT_2026-07-20.md` is not edited.
Its statement that public video hosting was pending reflected that earlier
capture state. This receipt and its companion reconciliation note provide the
current evidence state.

## Shared proof reconciliation

- Drive mirror: `TMN_NAUMIO_HQ/06_DELIVERY/LINEAGE-RELAY-PUBLIC-VIDEO-RECONCILIATION-2026-07-20/`
  via helper run `20260720T220945290Z`; all three initial files matched their
  SHA-256 values.
- Notion pointer: https://app.notion.com/p/3a3b143d29178135b819e635e088d915
- Re-mirrored reconciled receipt: helper run `20260720T221021067Z`, SHA-256
  `ddc91f0dea980f3b84d6eabfc2c86ac0928521a78a6085c94b32525baca60de3`.
