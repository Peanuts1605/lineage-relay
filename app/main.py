from __future__ import annotations

import logging
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .datahub_service import DataHubReviewService

APP_ROOT = Path(__file__).parent
app = FastAPI(title="Lineage Relay")
app.mount("/static", StaticFiles(directory=APP_ROOT / "static"), name="static")
logger = logging.getLogger(__name__)


def service() -> DataHubReviewService:
    return DataHubReviewService()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "product": "lineage-relay"}


@app.get("/api/review")
def review(governance: bool = False) -> dict:
    try:
        return service().evaluate(governance_block=governance)
    except Exception:
        logger.exception("Lineage Relay could not complete its metadata proof")
        raise HTTPException(
            status_code=503,
            detail="The metadata proof path is unavailable. No release package was generated.",
        ) from None


@app.post("/api/assign-owner")
def assign_owner() -> dict:
    try:
        review_service = service()
        review_service.assign_ml_owner()
        return review_service.evaluate()
    except Exception:
        logger.exception("Lineage Relay could not assign the synthetic owner")
        raise HTTPException(
            status_code=503,
            detail="The ownership update could not be verified. No release package was generated.",
        ) from None


@app.get("/")
def index() -> FileResponse:
    return FileResponse(APP_ROOT / "static" / "index.html")
