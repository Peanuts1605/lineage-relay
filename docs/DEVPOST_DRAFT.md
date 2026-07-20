# Lineage Relay

## Tagline

Turn a risky schema rename into a clear release decision before people and
systems get disconnected.

## Submission assets

- **Project URL:** <https://github.com/Peanuts1605/lineage-relay>
- **Source repository:** <https://github.com/Peanuts1605/lineage-relay>
- **Cover image:** [`demo/submission/lineage-relay-devpost-cover.png`](../demo/submission/lineage-relay-devpost-cover.png)
  (2400 x 1260, composed from the live `NEEDS_OWNER` review state).
- **Demo video:** [`demo/video/lineage-relay-forge-walkthrough-draft.mp4`](../demo/video/lineage-relay-forge-walkthrough-draft.mp4)
  (49.896 seconds, H.264/AAC). Upload it with the title and description below.

## Challenge category

**Metadata-Aware Code Generation & Development.** Lineage Relay uses the
official DataHub MCP server to read the real field-level schema, lineage,
ownership, and governance context before it generates a reviewable migration,
compatibility view, contract test, and PR-ready change summary. It also writes
the release decision receipt back to the source asset so the next reviewer
inherits the evidence.

## Inspiration

A column rename looks tiny in a migration ticket. In a real data stack it can
quietly break a dashboard, an ML feature, or the relationship between a team
and the data they own. The information exists in the catalog, but it is rarely
assembled into one decision a release owner can trust.

## What it does

Lineage Relay reviews a proposed rename of `orders.customer_id` to `buyer_id`.
It reads the source schema, ownership, and sensitivity metadata from DataHub,
then uses the official DataHub MCP server to trace three exact field-level
paths: source to analytics, analytics to dashboard, and source to ML features.

The outcome is one of three explicit release postures:

- `NEEDS_OWNER` when sensitive downstream use has no accountable owner.
- `READY` when ownership and compatibility actions are present.
- `BLOCKED_BY_GOVERNANCE` when a removal rule forbids the release.

For reviewable outcomes it generates a migration, compatibility view, contract
test, and change summary. It never deploys those artifacts. Every decision
writes a receipt and evidence hash back to the DataHub source asset.

## Why it is different

Lineage Relay is not a chat answer that says a change seems safe. It makes a
release posture depend on observable metadata, exact MCP lineage paths, and
accountability. The missing owner case is the default demo because it is the
failure that optimistic automation tends to miss.

## How we built it

- A synthetic DataHub instance on a Forge lab machine holds the source,
  analytics model, dashboard, ML feature, field lineage, ownership, and PII
  metadata.
- The app uses the DataHub Python SDK for schema and owner reads plus receipt
  write-back.
- The official DataHub MCP server supplies the `get_lineage_paths_between`
  traces that prove each source-to-consumer path at column level.
- A deterministic decision engine selects the posture and artifacts.
- FastAPI serves the review desk; the UI makes the field path, owner gap,
  release decision, receipt, and generated package visible together.

## Demo flow

1. Start on `NEEDS_OWNER`: the ML feature consumes PII and nobody owns it.
2. Show that the evidence ledger remains connected from source through
   analytics and dashboard while the ML path is visibly unowned.
3. Assign the synthetic ML owner and show `READY` plus the review package.
4. Turn on the governance constraint and show `BLOCKED_BY_GOVERNANCE` with no
   migration artifact.
5. Point out the receipt and evidence hash written to `orders`.

## Public demo metadata

**YouTube title**

`Lineage Relay: DataHub MCP Evidence for Safer Schema Changes`

**YouTube description**

Lineage Relay turns a risky field rename into a clear release decision before
people and systems get disconnected. In this 50-second walkthrough, a live
synthetic DataHub graph and the official DataHub MCP server expose three
field-level lineage paths, find an unowned PII-dependent ML feature, and return
`NEEDS_OWNER` instead of a false green light. Assigning an owner produces a
review package; a governance rule blocks it again. Every decision leaves a
receipt and evidence hash on the source asset.

Repository: https://github.com/Peanuts1605/lineage-relay

## Challenges

The substantive challenge was keeping the claim honest. Field lineage,
ownership, and release posture had to be live evidence, not hard-coded
storytelling. We also kept the MCP server's mutation tools disabled: it proves
the relationship paths, while the app's bounded DataHub SDK write records only
the review receipt.

## Accomplishments

- Proved all three release postures against a live synthetic DataHub graph.
- Verified three MCP field-level traces per review.
- Recovered the visual state after real interactions, including reset of the
  missing-owner demo state.
- Published source, tests, a reproducible Forge configuration, and the exact
  one-minute judge path.

## What is next

The next useful expansion is not autonomous migration. It is a review queue
for multiple proposed changes, with the same evidence-first contract and an
explicit human approval boundary.

## Built with

DataHub, DataHub MCP, FastAPI, Python, FastMCP, Docker, and a synthetic local
metadata graph.
