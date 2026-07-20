from __future__ import annotations

import hashlib
import json
import os
from datetime import UTC, datetime
from typing import Any

from datahub.emitter.mce_builder import make_dataset_urn, make_user_urn
from datahub.emitter.mcp import MetadataChangeProposalWrapper
from datahub.emitter.rest_emitter import DatahubRestEmitter
from datahub.ingestion.graph.client import DataHubGraph
from datahub.ingestion.graph.config import DatahubClientConfig
from datahub.metadata.schema_classes import (
    DatasetPropertiesClass,
    OwnerClass,
    OwnershipClass,
    SchemaMetadataClass,
    UpstreamLineageClass,
)

from .decision_engine import Decision, ReviewEvidence, decide
from .mcp_evidence import DataHubMCPLineageClient

PLATFORM = "demo"
ENVIRONMENT = "PROD"
SOURCE = "orders"
ANALYTICS = "analytics_orders_model"
DASHBOARD = "revenue_dashboard"
ML_FEATURES = "ml_customer_features"


def dataset_urn(name: str) -> str:
    return make_dataset_urn(PLATFORM, name, ENVIRONMENT)


class DataHubReviewService:
    def __init__(self, server: str | None = None) -> None:
        self.server = server or os.environ.get("DATAHUB_GMS_URL", "http://localhost:8080")
        self.graph = DataHubGraph(DatahubClientConfig(server=self.server))
        self.emitter = DatahubRestEmitter(gms_server=self.server)
        self.mcp = DataHubMCPLineageClient(self.server)

    def _aspects(self, urn: str) -> dict[str, Any]:
        return self.graph.get_aspects_for_entity(
            urn,
            ["datasetProperties", "schemaMetadata", "upstreamLineage", "ownership"],
            [
                DatasetPropertiesClass,
                SchemaMetadataClass,
                UpstreamLineageClass,
                OwnershipClass,
            ],
        )

    def _owners(self, ownership: OwnershipClass | None) -> list[str]:
        if ownership is None:
            return []
        return [owner.owner.removeprefix("urn:li:corpuser:") for owner in ownership.owners]

    def _lineage_evidence(self, lineage: UpstreamLineageClass | None) -> list[str]:
        if lineage is None:
            return []
        evidence: list[str] = []
        for relationship in lineage.fineGrainedLineages or []:
            evidence.extend((relationship.upstreams or []) + (relationship.downstreams or []))
        return evidence

    def evaluate(self, governance_block: bool = False) -> dict[str, Any]:
        source = self._aspects(dataset_urn(SOURCE))
        analytics = self._aspects(dataset_urn(ANALYTICS))
        dashboard = self._aspects(dataset_urn(DASHBOARD))
        ml_features = self._aspects(dataset_urn(ML_FEATURES))

        source_properties = source["datasetProperties"]
        source_schema = source["schemaMetadata"]
        source_fields = [field.fieldPath for field in source_schema.fields]
        sensitivity = source_properties.customProperties.get("lineage_relay.sensitivity")
        ml_owners = self._owners(ml_features["ownership"])
        analytics_evidence = self._lineage_evidence(analytics["upstreamLineage"])
        dashboard_evidence = self._lineage_evidence(dashboard["upstreamLineage"])
        ml_evidence = self._lineage_evidence(ml_features["upstreamLineage"])
        mcp_traces = {
            "orders_to_analytics": self.mcp.trace(
                source_urn=dataset_urn(SOURCE),
                source_column="customer_id",
                target_urn=dataset_urn(ANALYTICS),
                target_column="buyer_id",
            ),
            "analytics_to_dashboard": self.mcp.trace(
                source_urn=dataset_urn(ANALYTICS),
                source_column="buyer_id",
                target_urn=dataset_urn(DASHBOARD),
                target_column="buyer_id",
            ),
            "orders_to_ml_features": self.mcp.trace(
                source_urn=dataset_urn(SOURCE),
                source_column="customer_id",
                target_urn=dataset_urn(ML_FEATURES),
                target_column="customer_id",
            ),
        }
        exact_lineage_present = all(trace.path_count > 0 for trace in mcp_traces.values())
        missing_owner_assets = (ML_FEATURES,) if not ml_owners else ()
        compatibility_actions_present = (
            source_properties.customProperties.get("lineage_relay.compatibility_required") == "true"
            and exact_lineage_present
        )
        evidence = ReviewEvidence(
            source_is_sensitive=sensitivity == "PII",
            missing_owner_assets=missing_owner_assets,
            compatibility_actions_present=compatibility_actions_present,
            active_governance_block=governance_block,
        )
        decision = decide(evidence)
        payload = self._review_payload(
            decision=decision,
            source_fields=source_fields,
            analytics_evidence=analytics_evidence,
            dashboard_evidence=dashboard_evidence,
            ml_evidence=ml_evidence,
            ml_owners=ml_owners,
            exact_lineage_present=exact_lineage_present,
            mcp_traces=mcp_traces,
        )
        self._write_back(payload)
        return payload

    def assign_ml_owner(self, owner: str = "ml-platform-owner") -> None:
        self.emitter.emit_mcp(
            MetadataChangeProposalWrapper(
                entityUrn=dataset_urn(ML_FEATURES),
                aspect=OwnershipClass(
                    owners=[OwnerClass(owner=make_user_urn(owner), type="TECHNICAL_OWNER")]
                ),
            )
        )

    def _review_payload(
        self,
        *,
        decision: Decision,
        source_fields: list[str],
        analytics_evidence: list[str],
        dashboard_evidence: list[str],
        ml_evidence: list[str],
        ml_owners: list[str],
        exact_lineage_present: bool,
        mcp_traces: dict[str, Any],
    ) -> dict[str, Any]:
        evidence = {
            "source": dataset_urn(SOURCE),
            "source_field": "customer_id",
            "rename_target": "buyer_id",
            "source_fields": source_fields,
            "lineage": {
                "analytics_orders_model": analytics_evidence,
                "revenue_dashboard": dashboard_evidence,
                "ml_customer_features": ml_evidence,
            },
            "owners": {
                "orders": ["events-ops"],
                "analytics_orders_model": ["analytics-owner"],
                "revenue_dashboard": ["finance-bi"],
                "ml_customer_features": ml_owners,
            },
            "exact_lineage_present": exact_lineage_present,
            "mcp": {
                "server": "official DataHub MCP server",
                "traces": {name: trace.as_dict() for name, trace in mcp_traces.items()},
            },
            "sensitivity": "PII",
        }
        evidence_hash = hashlib.sha256(json.dumps(evidence, sort_keys=True).encode()).hexdigest()[:16]
        receipt_id = f"LR-{datetime.now(UTC).strftime('%Y%m%d%H%M%S')}-{evidence_hash[:6]}"
        artifacts = self._artifacts(decision)
        return {
            "request": "Rename orders.customer_id to buyer_id, then remove the old field after migration.",
            "decision": decision.verdict,
            "reason": decision.reason,
            "evidence": evidence,
            "evidence_hash": evidence_hash,
            "receipt_id": receipt_id,
            "artifacts": artifacts,
            "write_back": {
                "asset": dataset_urn(SOURCE),
                "properties": [
                    "lineage_relay.last_verdict",
                    "lineage_relay.receipt_id",
                    "lineage_relay.evidence_hash",
                ],
            },
        }

    def _artifacts(self, decision: Decision) -> dict[str, str]:
        if not decision.include_executable_migration:
            return {
                "CHANGE_SUMMARY.md": f"# Release blocked\n\n{decision.reason}\n\nNo migration was generated.\n",
                "datahub-decision.json": json.dumps({"verdict": decision.verdict}, indent=2) + "\n",
            }
        return {
            "migration.sql": "ALTER TABLE orders ADD COLUMN buyer_id VARCHAR;\nUPDATE orders SET buyer_id = customer_id WHERE buyer_id IS NULL;\n-- Do not drop customer_id in this release.\n",
            "compatibility_view.sql": "CREATE OR REPLACE VIEW orders_compat AS\nSELECT order_id, buyer_id, buyer_id AS customer_id, created_at\nFROM orders;\n",
            "test_customer_key_contract.sql": "SELECT COUNT(*) AS mismatches\nFROM orders_compat\nWHERE buyer_id IS DISTINCT FROM customer_id;\n",
            "CHANGE_SUMMARY.md": (
                "# Schema change review\n\n"
                f"Verdict: `{decision.verdict}`\n\n"
                f"{decision.reason.replace(ML_FEATURES, f'`{ML_FEATURES}`')}\n\n"
                "Rollback: keep `customer_id` through the compatibility window.\n"
            ),
        }

    def _write_back(self, payload: dict[str, Any]) -> None:
        urn = dataset_urn(SOURCE)
        current = self.graph.get_aspect(urn, DatasetPropertiesClass)
        properties = dict(current.customProperties if current and current.customProperties else {})
        properties.update(
            {
                "lineage_relay.last_verdict": payload["decision"],
                "lineage_relay.receipt_id": payload["receipt_id"],
                "lineage_relay.evidence_hash": payload["evidence_hash"],
            }
        )
        self.emitter.emit_mcp(
            MetadataChangeProposalWrapper(
                entityUrn=urn,
                aspect=DatasetPropertiesClass(
                    name=current.name if current else SOURCE,
                    description=current.description if current else "Lineage Relay source asset.",
                    customProperties=properties,
                ),
            )
        )
