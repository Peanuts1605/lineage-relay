from pathlib import Path


def test_unavailable_metadata_path_clears_stale_release_package() -> None:
    client = (Path(__file__).parents[1] / "app" / "static" / "app.js").read_text()

    assert "function renderUnavailable(message)" in client
    assert '$("#proof-status").innerHTML = \'<span class="pulse"></span>Metadata proof unavailable\';' in client
    assert '$("#receipt").textContent = "-";' in client
    assert '$("#writeback").textContent = "No decision record was written.";' in client
    assert '$("#artifact-tabs").innerHTML = "";' in client
    assert '$("#artifact").textContent = "No review package was generated.";' in client
    assert "renderUnavailable(error.message);" in client
