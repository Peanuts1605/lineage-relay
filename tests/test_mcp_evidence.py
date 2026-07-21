import json

import pytest

from app.mcp_evidence import MCPLineageError, parse_lineage_path_response


SOURCE = "urn:li:dataset:(urn:li:dataPlatform:demo,orders,PROD)"
TARGET = "urn:li:dataset:(urn:li:dataPlatform:demo,ml_customer_features,PROD)"


def path_payload() -> str:
    return json.dumps(
        {
            "pathCount": 1,
            "paths": [
                {
                    "path": [
                        {"urn": f"urn:li:schemaField:({SOURCE},customer_id)"},
                        {"urn": f"urn:li:schemaField:({TARGET},customer_id)"},
                    ]
                }
            ],
        }
    )


def test_parses_a_matching_field_path() -> None:
    trace = parse_lineage_path_response(
        path_payload(),
        source_urn=SOURCE,
        source_column="customer_id",
        target_urn=TARGET,
        target_column="customer_id",
    )

    assert trace.path_count == 1
    assert trace.first_path[0].endswith("orders,PROD),customer_id)")


def test_rejects_a_path_without_the_requested_target_field() -> None:
    payload = json.loads(path_payload())
    payload["paths"][0]["path"][-1]["urn"] = "urn:li:schemaField:(urn:li:dataset:(urn:li:dataPlatform:demo,other,PROD),customer_id)"

    with pytest.raises(MCPLineageError, match="does not match"):
        parse_lineage_path_response(
            json.dumps(payload),
            source_urn=SOURCE,
            source_column="customer_id",
            target_urn=TARGET,
            target_column="customer_id",
        )


def test_rejects_a_reversed_field_path() -> None:
    payload = json.loads(path_payload())
    payload["paths"][0]["path"].reverse()

    with pytest.raises(MCPLineageError, match="direction"):
        parse_lineage_path_response(
            json.dumps(payload),
            source_urn=SOURCE,
            source_column="customer_id",
            target_urn=TARGET,
            target_column="customer_id",
        )
