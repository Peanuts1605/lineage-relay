# Lineage Relay: DataHub Hackathon Alignment

- Contest: [Build with DataHub: The Agent Hackathon](https://datahub.devpost.com/)
- Deadline: 2026-08-10 5:00 PM EDT
- Primary category: **Agents That Do Real Work**
- Secondary evidence: metadata-aware migration review package

## Why this route

Lineage Relay is not a generic metadata viewer. For a proposed field rename,
it gathers schema, PII, ownership, and lineage context from DataHub; proves
three exact field paths through the official MCP server; selects a deterministic
release posture; performs only a bounded owner assignment when asked; and
writes a decision receipt and evidence hash back to the source asset.

That directly supports the contest's emphasis on agents that read the context
graph, take a useful action, and leave durable context for the next person or
agent. The review package also demonstrates DataHub-grounded migration code,
but it is supporting proof rather than the primary category claim.

## Rubric evidence

| Criterion | Evidence in this repository |
| --- | --- |
| Use of DataHub | Live local DataHub graph; schema, PII, ownership, field lineage, and receipt write-back. |
| Technical execution | Five focused tests plus Forge validation of all three release postures. |
| Originality | A release decision can be `NEEDS_OWNER`, preventing a false green light when metadata shows an unowned sensitive dependency. |
| Real-world usefulness | Data teams receive a reviewable migration, compatibility view, contract test, and change summary before a field is removed. |
| Submission quality | One-minute judge path, public source, Apache 2.0 license, visual proof, reproducible setup, and a short demo script. |

## Submission checklist

- [x] Public repository with Apache 2.0 license.
- [x] Clear local setup and test instructions.
- [x] Sample generated review artifacts in `examples/needs-owner/`.
- [x] Demo script grounded in the live Forge scenario.
- [ ] Public sub-three-minute video showing the working review desk.
- [ ] Devpost project form, final eligibility attestation, and submission.

## Decision

Advance without adding broad features. The score move is a crisp working demo
that makes the MCP field paths, owner action, generated package, and DataHub
receipt obvious in under three minutes.
