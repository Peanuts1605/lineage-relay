# Lineage Relay Demo Script

**Length:** 80-100 seconds.  
**Starting state:** restored synthetic `NEEDS_OWNER` fixture on Forge.

## 0:00-0:12 - The release problem

Show the Lineage Relay review desk.

> A field rename can look harmless in a migration ticket, then quietly sever
> a dashboard, an ML feature, or the person responsible for it. Lineage Relay
> turns that into a release decision before the change ships.

## 0:12-0:34 - Live context, not a guess

Point to `orders.customer_id`, the PII tag, three downstream paths, and the
green **Live DataHub + MCP evidence** badge.

> This review reads a live synthetic DataHub graph. The official DataHub MCP
> server proves the exact field paths from orders to analytics, the revenue
> dashboard, and an ML feature. The ML feature has no owner, so the agent does
> not give us a false green light.

## 0:34-0:48 - A useful non-green outcome

Point to the `NEEDS OWNER` panel and receipt.

> The posture is `NEEDS_OWNER`. The receipt and evidence hash are written back
> to the source asset, so the next reviewer sees why this release stopped.

## 0:48-1:05 - Bounded action and code review package

Select **Assign ML owner**. Wait for `READY`, then show the package tabs.

> When an accountable owner is assigned, the same live evidence becomes
> `READY`. Lineage Relay produces a migration, compatibility view, contract
> test, and change summary for review. It does not deploy anything.

## 1:05-1:20 - Governance remains decisive

Select **Check governance block**. Show that the migration tab is absent.

> If a governance rule forbids the removal, the result becomes
> `BLOCKED_BY_GOVERNANCE` and no migration package is generated. Context changes
> the decision; it is not decorative metadata.

## Closing card

> Lineage Relay gives data teams a traceable answer before a small schema change
> becomes a large incident: field paths, owners, a release posture, reviewable
> code, and a receipt in one place.
