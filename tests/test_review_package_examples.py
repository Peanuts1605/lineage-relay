from pathlib import Path

from app.datahub_service import DataHubReviewService
from app.decision_engine import Decision


def test_checked_in_needs_owner_package_matches_the_generator() -> None:
    package = DataHubReviewService.__new__(DataHubReviewService)._artifacts(
        Decision(
            verdict="NEEDS_OWNER",
            reason="Sensitive downstream use has no accountable owner: ml_customer_features.",
            include_executable_migration=True,
        )
    )
    examples = Path(__file__).resolve().parents[1] / "examples" / "needs-owner"

    for filename, generated in package.items():
        assert (examples / filename).read_text() == generated
