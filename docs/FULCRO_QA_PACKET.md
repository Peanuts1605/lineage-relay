# Lineage Relay: Fulcro QA Packet

## One-sentence claim to attack

Lineage Relay does not mark a rename safe unless DataHub ownership,
compatibility metadata, and three exact MCP field paths support the decision.

## Live lab target

- App: `http://127.0.0.1:4176` on Forge through an SSH tunnel.
- DataHub frontend: `http://127.0.0.1:9002` on Forge.
- Source: `urn:li:dataset:(urn:li:dataPlatform:demo,orders,PROD)`.
- Fixture: `contest-portfolio/lineage-relay-forge/seed_lineage_relay_fixture.py`.

## Expected reproducible results

| Action | Expected posture | Migration artifact | MCP traces |
| --- | --- | --- | --- |
| Fresh fixture | `NEEDS_OWNER` | present for review only | 3 |
| Assign ML owner | `READY` | present for review only | 3 |
| Governance block | `BLOCKED_BY_GOVERNANCE` | absent | 3 |

## Strongest claims worth falsifying

1. The decision uses MCP path evidence, rather than a hard-coded boolean.
2. An ML downstream dependency without an owner cannot produce `READY`.
3. A governance block cannot return an executable migration artifact.
4. The receipt written to `orders` matches the visible decision and evidence
   hash.
5. The three visible controls work in a real browser, not only through HTTP.
6. An unavailable metadata proof path produces a human-readable error and no
   generated release package.

## Existing proof

- Five unit tests: decision logic and MCP response validation.
- Live run: all three outcomes exercised after MCP integration.
- Browser run: owner mutation and governance control exercised against Forge.
- Screenshot: `docs/evidence/forge-needs-owner.png`.

## Desired QA return

Return one decision (`GO`, `GO_WITH_PATCH`, or `NO_GO`) plus reproducible
findings. Prioritize contradictions between the submission claim and actual
runtime behavior over cosmetic suggestions.
