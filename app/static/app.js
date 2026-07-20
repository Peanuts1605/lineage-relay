const state = { review: null, activeArtifact: null };

const $ = (selector) => document.querySelector(selector);

function setBusy(button, busy) {
  button.disabled = busy;
  button.textContent = busy ? "Reading DataHub..." : button.dataset.label;
}

async function request(path, options = {}) {
  const response = await fetch(path, options);
  const payload = await response.json();
  if (!response.ok) throw new Error(payload.detail || "Unable to complete review.");
  return payload;
}

function render(review) {
  state.review = review;
  const decision = review.decision;
  document.body.dataset.verdict = decision;
  $("#proof-status").innerHTML = '<span class="pulse"></span>Live DataHub + MCP evidence';
  $("#verdict").textContent = decision.replaceAll("_", " ");
  $("#reason").textContent = review.reason;
  $("#receipt").textContent = review.receipt_id;
  $("#hash").textContent = `Evidence ${review.evidence_hash}`;
  const owners = review.evidence.owners.ml_customer_features;
  $("#ml-owner").textContent = owners.length ? `Owned by ${owners.join(", ")}` : "Owner missing";
  $("#lineage-proof").textContent = review.evidence.exact_lineage_present
    ? "Exact source-to-consumer field lineage traced through the official DataHub MCP server."
    : "Field-level lineage is incomplete.";
  renderArtifacts(review.artifacts);
}

function renderArtifacts(artifacts) {
  const entries = Object.entries(artifacts);
  state.activeArtifact = entries[0]?.[0] || null;
  const tabs = $("#artifact-tabs");
  tabs.innerHTML = "";
  for (const [name] of entries) {
    const tab = document.createElement("button");
    tab.textContent = name;
    tab.className = name === state.activeArtifact ? "active" : "";
    tab.addEventListener("click", () => {
      state.activeArtifact = name;
      document.querySelectorAll("#artifact-tabs button").forEach((button) => button.classList.toggle("active", button.textContent === name));
      $("#artifact").textContent = artifacts[name];
    });
    tabs.appendChild(tab);
  }
  $("#artifact").textContent = state.activeArtifact ? artifacts[state.activeArtifact] : "No package generated.";
}

function renderUnavailable(message) {
  state.review = null;
  state.activeArtifact = null;
  document.body.dataset.verdict = "UNAVAILABLE";
  $("#proof-status").innerHTML = '<span class="pulse"></span>Metadata proof unavailable';
  $("#verdict").textContent = "DataHub unavailable";
  $("#reason").textContent = message;
  $("#receipt").textContent = "-";
  $("#hash").textContent = "Evidence unavailable";
  $("#ml-owner").textContent = "Proof unavailable";
  $("#lineage-proof").textContent = "The metadata proof path could not be verified.";
  $("#artifact-tabs").innerHTML = "";
  $("#artifact").textContent = "No review package was generated.";
}

async function run(button, path, options) {
  setBusy(button, true);
  try {
    render(await request(path, options));
  } catch (error) {
    renderUnavailable(error.message);
  } finally {
    setBusy(button, false);
  }
}

for (const button of document.querySelectorAll(".actions button")) button.dataset.label = button.textContent;
$("#assess").addEventListener("click", () => run($("#assess"), "/api/review"));
$("#assign-owner").addEventListener("click", () => run($("#assign-owner"), "/api/assign-owner", { method: "POST" }));
$("#governance").addEventListener("click", () => run($("#governance"), "/api/review?governance=true"));
run($("#assess"), "/api/review");
