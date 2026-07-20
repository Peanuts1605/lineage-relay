# Lineage Relay Write-Back Recovery Patch

## Decision

`PASS_WITH_PATCH` - the unavailable-proof view must not retain a success claim
after the metadata request fails.

## Finding

The browser already cleared a stale receipt, evidence hash, tabs, and review
package when DataHub proof was unavailable. It still displayed `Decision record
written to orders`, which contradicted the state shown directly above it.

## Change

- Added the stable `#writeback` target to the decision panel.
- Restored `Decision record written to orders` only after a verified review
  response renders.
- Replaced it with `No decision record was written.` in the unavailable-proof
  renderer.
- Extended the existing recovery contract test to make that reset durable.

## Verification

- `python -m pytest tests -q`: 7 passed.
- Browser, local synthetic DataHub/MCP fixture: **Check governance block**
  produced `BLOCKED BY GOVERNANCE`, two non-executable review artifacts, and a
  new receipt.
- Browser, isolated unavailable-proof fixture: `DataHub unavailable`,
  `Metadata proof unavailable`, receipt `-`, zero artifact tabs, `No review
  package was generated.`, and `No decision record was written.`
- Browser, restored fixture: `NEEDS OWNER`, `Owner missing`, and the four
  review-package tabs returned.

This changes presentation truthfulness only. It does not change the DataHub
query, MCP trace, decision engine, generated migration content, or fixture.
