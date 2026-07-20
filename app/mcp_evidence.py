from __future__ import annotations

import asyncio
import json
import os
import sys
from dataclasses import dataclass
from typing import Any

from fastmcp import Client
from fastmcp.client.transports import StdioTransport


class MCPLineageError(RuntimeError):
    """Raised when a review cannot obtain its required MCP lineage evidence."""


@dataclass(frozen=True)
class MCPLineageTrace:
    source_urn: str
    source_column: str
    target_urn: str
    target_column: str
    path_count: int
    first_path: tuple[str, ...]

    def as_dict(self) -> dict[str, Any]:
        return {
            "source": {"urn": self.source_urn, "column": self.source_column},
            "target": {"urn": self.target_urn, "column": self.target_column},
            "path_count": self.path_count,
            "first_path": list(self.first_path),
        }


def parse_lineage_path_response(
    text: str,
    *,
    source_urn: str,
    source_column: str,
    target_urn: str,
    target_column: str,
) -> MCPLineageTrace:
    """Validate the compact JSON emitted by DataHub's MCP path-trace tool."""

    try:
        payload = json.loads(text)
    except json.JSONDecodeError as error:
        raise MCPLineageError("DataHub MCP returned non-JSON lineage evidence.") from error

    paths = payload.get("paths") or []
    path_count = payload.get("pathCount", 0)
    if not isinstance(path_count, int) or path_count < 1 or not paths:
        raise MCPLineageError("DataHub MCP found no exact column-level lineage path.")

    first_path = paths[0].get("path") or []
    urns = tuple(node.get("urn", "") for node in first_path if node.get("urn"))
    expected_source = f"urn:li:schemaField:({source_urn},{source_column})"
    expected_target = f"urn:li:schemaField:({target_urn},{target_column})"
    if expected_source not in urns or expected_target not in urns:
        raise MCPLineageError("DataHub MCP returned a path that does not match the requested fields.")

    return MCPLineageTrace(
        source_urn=source_urn,
        source_column=source_column,
        target_urn=target_urn,
        target_column=target_column,
        path_count=path_count,
        first_path=urns,
    )


class DataHubMCPLineageClient:
    """A narrow stdio client for the official DataHub MCP server.

    The demo intentionally keeps mutation tools disabled. MCP supplies the evidence
    trace; the application writes its bounded receipt through the DataHub SDK.
    """

    def __init__(self, gms_url: str) -> None:
        self.gms_url = gms_url
        self.python = os.environ.get("LINEAGE_RELAY_MCP_PYTHON", sys.executable)
        self.source_root = os.environ.get("LINEAGE_RELAY_MCP_SOURCE_ROOT")

    def trace(
        self,
        *,
        source_urn: str,
        source_column: str,
        target_urn: str,
        target_column: str,
    ) -> MCPLineageTrace:
        return asyncio.run(
            self._trace(
                source_urn=source_urn,
                source_column=source_column,
                target_urn=target_urn,
                target_column=target_column,
            )
        )

    async def _trace(
        self,
        *,
        source_urn: str,
        source_column: str,
        target_urn: str,
        target_column: str,
    ) -> MCPLineageTrace:
        environment = {
            "DATAHUB_GMS_URL": self.gms_url,
            "DATAHUB_MCP_DOCUMENT_TOOLS_DISABLED": "true",
            "LOGURU_LEVEL": "WARNING",
        }
        if self.source_root:
            environment["PYTHONPATH"] = self.source_root

        transport = StdioTransport(
            command=self.python,
            args=["-m", "mcp_server_datahub"],
            env=environment,
        )
        try:
            async with Client(transport) as client:
                result = await client.call_tool(
                    "get_lineage_paths_between",
                    {
                        "source_urn": source_urn,
                        "source_column": source_column,
                        "target_urn": target_urn,
                        "target_column": target_column,
                        "direction": "downstream",
                    },
                )
        except Exception as error:
            raise MCPLineageError(f"DataHub MCP path trace unavailable: {error}") from error

        if result.is_error:
            raise MCPLineageError("DataHub MCP declined the requested path trace.")

        texts = [item.text for item in result.content if hasattr(item, "text")]
        if not texts:
            raise MCPLineageError("DataHub MCP returned no lineage evidence.")
        return parse_lineage_path_response(
            texts[0],
            source_urn=source_urn,
            source_column=source_column,
            target_urn=target_urn,
            target_column=target_column,
        )
