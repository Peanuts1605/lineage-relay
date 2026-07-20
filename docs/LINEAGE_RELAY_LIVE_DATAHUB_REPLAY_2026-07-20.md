# Lineage Relay Live DataHub Replay

Date: 2026-07-20
Contest: Build with DataHub: The Agent Hackathon
Category: Metadata-Aware Code Generation & Development

## Decision

`LIVE_PROOF_GREEN; PUBLIC_REPOSITORY_AND_VIDEO_ARE_THE_JUDGE_TEST_ROUTE`

Lineage Relay does not need a pretend hosted dashboard. The official rules
accept a live demo, hosted app, **or a public repository with clear setup
instructions** as the judge test route. The public repository has the required
Apache 2.0 license, a complete local Quickstart path, fixture seed, test
instructions, and inspectable generated package.

## Live Replay

On Leo, a fresh synthetic DataHub Quickstart was started locally, the official
DataHub MCP server was installed from its public repository, and the Lineage
Relay fixture was seeded. The review desk then ran against that metadata graph.

The initial review produced:

- `NEEDS_OWNER`
- three exact field-level MCP paths: source to analytics, analytics to
  dashboard, and source to ML feature
- an unowned PII-dependent ML feature
- generated compatibility-first review artifacts
- a write-back receipt on the synthetic `orders` asset

The visible app path was then exercised in sequence:

1. `NEEDS_OWNER` with the missing ML owner.
2. `READY` after **Assign ML owner** writes the synthetic owner to DataHub.
3. `BLOCKED_BY_GOVERNANCE` after the governance action, with no false release.

Desktop and 390 px mobile replays completed with no browser errors and no
horizontal overflow.

## Evidence

| Check | Result |
| --- | --- |
| `pytest tests -q` | `6 passed` |
| `python -m compileall -q app scripts` | passed |
| DataHub Quickstart | running locally |
| Official MCP traces | 3 exact field paths returned |
| `NEEDS_OWNER` | passed |
| `READY` after owner assignment | passed |
| `BLOCKED_BY_GOVERNANCE` | passed |
| Browser errors | none |
| 390 px overflow | false |

Fresh rendered evidence:

- `demo/frames/05-live-local-needs-owner-2026-07-20.png`
- `demo/frames/06-live-local-ready-2026-07-20.png`
- `demo/frames/07-live-local-governance-2026-07-20.png`
- `demo/frames/08-live-local-mobile-2026-07-20.png`

## Current Tool Check

The official DataHub quickstart documentation remains the intended local route.
The installed DataHub CLI resolved its default Quickstart plan to
`v1.5.0.6`; the project uses `acryl-datahub 1.6.0.15`. The actual live replay
passed across that pairing, including the official MCP field-trace path. This
is stronger evidence than assuming the version alignment from package metadata.

Cloudflare Containers are now a possible hosting surface, but they require a
Workers Paid plan and are a poor fit for a multi-service DataHub Quickstart.
The official contest rules already accept this repository's reproducible judge
route, so no fragile or misleading hosted substitute was introduced.

## Submission Evidence Update

The prepared 49.896-second walkthrough was published on 2026-07-20 at
<https://www.youtube.com/shorts/0HokRdSv5D4>. YouTube Studio reported no
copyright issues, and an independent HTTP request returned 200 at the public
URL. No app or fixture change was needed.
