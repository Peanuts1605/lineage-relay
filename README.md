# Lineage Relay

Lineage Relay turns a schema-change request into a reviewable release package
grounded in a live DataHub metadata graph and verified by the official DataHub
MCP server.

Data teams usually discover that a harmless-looking column rename had a human
owner, an ML feature, or a dashboard attached only after something breaks.
Lineage Relay makes the consequence visible before release: exact field paths,
accountable owners, a deterministic release posture, and a review package. It
is not a generic coding assistant and it never deploys a migration.

The first proof asks to rename `orders.customer_id` to `buyer_id`. The app reads
the source schema, ownership, and sensitivity metadata from a synthetic local
DataHub instance. It then asks DataHub MCP to trace three exact column paths:
source to analytics, analytics to dashboard, and source to ML features. It
returns one deterministic posture:

- `NEEDS_OWNER` when sensitive downstream use has no accountable owner.
- `READY` when owners and compatibility actions are present.
- `BLOCKED_BY_GOVERNANCE` when a removal rule blocks the request.

It generates a migration, compatibility view, contract test, and change summary
for review. It never runs the migration. Each review writes a receipt back to
the source asset as DataHub custom properties.

## Sample review package

Judges can inspect the generated `NEEDS_OWNER` package without starting the
lab in [`examples/needs-owner/`](examples/needs-owner/). The package keeps the
legacy column in place and makes the ownership gap explicit; it is review
material, not an automatically applied migration.

## Local proof

1. Run the Forge fixture from `contest-portfolio/lineage-relay-forge/`.
2. Install `requirements.txt` into one Python 3.11 environment.
3. Install the official `acryldata/mcp-server-datahub` source in editable mode
   and set `LINEAGE_RELAY_MCP_SOURCE_ROOT` to its `src` directory. Editable
   mode keeps the MCP server's bundled GraphQL assets alongside the process.
4. Set `DATAHUB_GMS_URL=http://localhost:8080` and
   `LINEAGE_RELAY_MCP_PYTHON` to that Python environment.
5. Start `uvicorn app.main:app --host 127.0.0.1 --port 4176` from this directory.
6. Open `http://127.0.0.1:4176`.

The MCP server runs with its mutation tools disabled. It provides the field-level
proof; the app writes only its receipt properties through the DataHub SDK.

## Judge check in one minute

1. Open the seeded `NEEDS_OWNER` review: the ML feature uses PII and has no
   owner, while the DataHub MCP trace confirms all three column paths.
2. Select **Assign ML owner**: the synthetic owner is written to DataHub and the
   same evidence produces `READY` plus a migration package.
3. Select **Check governance block**: the active removal rule yields
   `BLOCKED_BY_GOVERNANCE` and no migration artifact.
4. Every decision leaves a receipt and evidence hash on `orders` in DataHub.

## Test

```bash
python -m pytest tests -q
```
