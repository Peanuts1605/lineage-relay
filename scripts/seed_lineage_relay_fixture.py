#!/usr/bin/env python3
"""Seed the public-safe Lineage Relay rename scenario into local DataHub."""

from __future__ import annotations

import hashlib
import json
import os

from datahub.emitter.mce_builder import make_dataset_urn, make_schema_field_urn, make_user_urn
from datahub.emitter.mcp import MetadataChangeProposalWrapper
from datahub.emitter.rest_emitter import DatahubRestEmitter
from datahub.metadata.schema_classes import (
    DatasetPropertiesClass,
    FineGrainedLineageClass,
    OtherSchemaClass,
    OwnerClass,
    OwnershipClass,
    SchemaFieldClass,
    SchemaFieldDataTypeClass,
    SchemaMetadataClass,
    StringTypeClass,
    UpstreamClass,
    UpstreamLineageClass,
)

PLATFORM = "demo"
ENVIRONMENT = "PROD"
GMS_SERVER = os.environ.get("DATAHUB_GMS_URL", "http://localhost:8080")


def dataset_urn(name: str) -> str:
    return make_dataset_urn(PLATFORM, name, ENVIRONMENT)


def schema_fields(values: list[tuple[str, str, str]]) -> list[SchemaFieldClass]:
    return [
        SchemaFieldClass(
            fieldPath=field_path,
            type=SchemaFieldDataTypeClass(type=StringTypeClass()),
            nativeDataType=native_type,
            nullable=True,
            description=description,
        )
        for field_path, native_type, description in values
    ]


def emit_dataset(
    emitter: DatahubRestEmitter,
    name: str,
    description: str,
    fields: list[tuple[str, str, str]],
    properties: dict[str, str],
    owners: list[str],
    upstreams: list[str] | None = None,
    fine_grained: list[FineGrainedLineageClass] | None = None,
) -> str:
    urn = dataset_urn(name)
    emitter.emit_mcp(
        MetadataChangeProposalWrapper(
            entityUrn=urn,
            aspect=DatasetPropertiesClass(
                name=name,
                description=description,
                customProperties=properties,
            ),
        )
    )
    field_models = schema_fields(fields)
    schema_hash = hashlib.sha1(json.dumps(fields, sort_keys=True).encode()).hexdigest()
    emitter.emit_mcp(
        MetadataChangeProposalWrapper(
            entityUrn=urn,
            aspect=SchemaMetadataClass(
                schemaName=name,
                platform=f"urn:li:dataPlatform:{PLATFORM}",
                version=0,
                hash=schema_hash,
                platformSchema=OtherSchemaClass(rawSchema=json.dumps({"fixture": "lineage-relay"})),
                fields=field_models,
            ),
        )
    )
    emitter.emit_mcp(
        MetadataChangeProposalWrapper(
            entityUrn=urn,
            aspect=OwnershipClass(
                owners=[
                    OwnerClass(owner=make_user_urn(owner), type="TECHNICAL_OWNER")
                    for owner in owners
                ]
            ),
        )
    )
    if upstreams:
        emitter.emit_mcp(
            MetadataChangeProposalWrapper(
                entityUrn=urn,
                aspect=UpstreamLineageClass(
                    upstreams=[
                        UpstreamClass(dataset=upstream, type="TRANSFORMED")
                        for upstream in upstreams
                    ],
                    fineGrainedLineages=fine_grained or [],
                ),
            )
        )
    return urn


def main() -> None:
    emitter = DatahubRestEmitter(gms_server=GMS_SERVER)
    orders = emit_dataset(
        emitter,
        "orders",
        "Synthetic public-safe order source for the Lineage Relay rename test.",
        [
            ("order_id", "VARCHAR", "Synthetic order identifier."),
            ("customer_id", "VARCHAR", "PII-classified customer reference under review."),
            ("created_at", "TIMESTAMP", "Synthetic order creation timestamp."),
        ],
        {
            "lineage_relay.sensitivity": "PII",
            "lineage_relay.change_request": "customer_id -> buyer_id",
            "lineage_relay.compatibility_required": "true",
        },
        ["events-ops"],
    )
    analytics_orders = emit_dataset(
        emitter,
        "analytics_orders_model",
        "Synthetic analytics model that renames customer_id to buyer_id.",
        [
            ("order_id", "VARCHAR", "Synthetic order identifier."),
            ("buyer_id", "VARCHAR", "Compatibility rename target for customer_id."),
        ],
        {
            "lineage_relay.owner_status": "assigned",
            "lineage_relay.compatibility_view": "required",
        },
        ["analytics-owner"],
        [orders],
        [
            FineGrainedLineageClass(
                upstreamType="FIELD_SET",
                downstreamType="FIELD_SET",
                upstreams=[make_schema_field_urn(orders, "customer_id")],
                downstreams=[make_schema_field_urn(dataset_urn("analytics_orders_model"), "buyer_id")],
                transformOperation="rename customer_id to buyer_id",
                confidenceScore=1.0,
            )
        ],
    )
    revenue_dashboard = emit_dataset(
        emitter,
        "revenue_dashboard",
        "Synthetic revenue dashboard fed by the renamed analytics model.",
        [
            ("buyer_id", "VARCHAR", "Consumer-facing compatibility field."),
            ("revenue", "DECIMAL", "Synthetic revenue metric."),
        ],
        {"lineage_relay.owner_status": "assigned", "lineage_relay.decision_impact": "reporting"},
        ["finance-bi"],
        [analytics_orders],
        [
            FineGrainedLineageClass(
                upstreamType="FIELD_SET",
                downstreamType="FIELD_SET",
                upstreams=[make_schema_field_urn(analytics_orders, "buyer_id")],
                downstreams=[make_schema_field_urn(dataset_urn("revenue_dashboard"), "buyer_id")],
                transformOperation="carry buyer_id into revenue dashboard",
                confidenceScore=1.0,
            )
        ],
    )
    ml_customer_features = emit_dataset(
        emitter,
        "ml_customer_features",
        "Synthetic downstream ML feature set intentionally missing an owner.",
        [
            ("customer_id", "VARCHAR", "PII source field used by the synthetic feature."),
            ("feature_score", "DECIMAL", "Synthetic model feature."),
        ],
        {
            "lineage_relay.owner_status": "missing",
            "lineage_relay.sensitivity": "PII",
            "lineage_relay.decision_impact": "ml_feature",
        },
        [],
        [orders],
        [
            FineGrainedLineageClass(
                upstreamType="FIELD_SET",
                downstreamType="FIELD_SET",
                upstreams=[make_schema_field_urn(orders, "customer_id")],
                downstreams=[make_schema_field_urn(dataset_urn("ml_customer_features"), "customer_id")],
                transformOperation="carry customer_id into ML features",
                confidenceScore=1.0,
            )
        ],
    )
    print(
        json.dumps(
            {
                "status": "seeded",
                "source": orders,
                "rename_target": analytics_orders,
                "dashboard": revenue_dashboard,
                "unowned_ml_feature": ml_customer_features,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
