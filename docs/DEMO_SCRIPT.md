# Lineage Relay Demo Script

**Length:** about 50 seconds.
**Starting state:** restored synthetic `NEEDS_OWNER` fixture on Forge.

## 0:00-0:17 - The release problem

Show the Lineage Relay review desk.

> A field rename can look small, but it can disconnect a dashboard, a model,
> or the person responsible. Lineage Relay reads a live DataHub graph before
> that change becomes an incident.

## 0:17-0:34 - A useful non-green outcome

Point to `orders.customer_id`, the PII tag, three downstream paths, and the
green **Live DataHub + MCP evidence** badge.

> The official DataHub MCP server proves the exact field paths from orders to
> analytics, the revenue dashboard, and ML features. This review finds PII
> flowing to an ML feature with no accountable owner, so it returns
> `NEEDS_OWNER`, not a false green light, and writes a receipt back to DataHub.

## 0:34-0:50 - Bounded action and governance stop

Select **Assign ML owner**. Wait for `READY`, then show the package tabs.

> When an accountable owner is assigned, the same live context becomes `READY`
> with a migration, compatibility view, contract test, and change summary for
> review. A governance rule then becomes `BLOCKED_BY_GOVERNANCE` and no
> migration package is generated. Nothing deploys automatically.

## Closing card

> Context changes the decision before a small rename becomes a large incident.
