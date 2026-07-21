# Lineage Relay: DataHub Hackathon Alignment

- Contest: [Build with DataHub: The Agent Hackathon](https://datahub.devpost.com/)
- Deadline: 2026-08-10 5:00 PM EDT
- Primary category: **Metadata-Aware Code Generation & Development**
- Supporting evidence: agentic owner assignment and DataHub decision write-back

## Why this route

Lineage Relay is not a generic metadata viewer or blind SQL writer. For a
proposed field rename, it gathers schema, PII, ownership, and lineage context
from DataHub; proves three exact field paths through the official MCP server;
selects a deterministic release posture; and generates a migration,
compatibility view, contract test, and PR-ready change summary that reflect
that evidence.

That directly supports the contest's metadata-aware code-generation category:
the release package is grounded in real schemas, lineage, and rules before any
artifact is produced. The bounded synthetic owner assignment and DataHub
write-back remain important supporting proof that the agent leaves durable
context for the next reviewer.

## Rubric evidence

| Criterion | Evidence in this repository |
| --- | --- |
| Use of DataHub | Live local DataHub graph; schema, PII, ownership, field lineage, and receipt write-back. |
| Technical execution | Seven focused tests plus Forge validation of all three release postures. |
| Originality | A release decision can be `NEEDS_OWNER`, preventing a false green light when metadata shows an unowned sensitive dependency. |
| Real-world usefulness | Data teams receive a reviewable migration, compatibility view, contract test, and change summary before a field is removed. |
| Submission quality | One-minute judge path, public source, Apache 2.0 license, visual proof, reproducible setup, and a short demo script. |

## Submission checklist

- [x] Public repository with Apache 2.0 license.
- [x] Clear local setup and test instructions.
- [x] Sample generated review artifacts in `examples/needs-owner/`.
- [x] Demo script grounded in the live Forge scenario.
- [x] Public 49.896-second video showing the working review desk: [YouTube walkthrough](https://www.youtube.com/shorts/0HokRdSv5D4) (public HTTP route checked 2026-07-20).
- [ ] Devpost project form, final eligibility attestation, and submission.

## Decision

Advance without adding broad features. The score move is a crisp working demo
that makes the MCP field paths, owner action, generated package, and DataHub
receipt obvious in under three minutes.
