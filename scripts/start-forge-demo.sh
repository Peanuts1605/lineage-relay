#!/bin/sh
set -eu

: "${DATAHUB_GMS_URL:=http://127.0.0.1:8080}"
: "${LINEAGE_RELAY_MCP_PYTHON:=$(command -v python3)}"
: "${LINEAGE_RELAY_MCP_SOURCE_ROOT:?Set this to the official DataHub MCP server src directory.}"

export DATAHUB_GMS_URL LINEAGE_RELAY_MCP_PYTHON LINEAGE_RELAY_MCP_SOURCE_ROOT
exec "$LINEAGE_RELAY_MCP_PYTHON" -m uvicorn app.main:app --host 127.0.0.1 --port 4176
