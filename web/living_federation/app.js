const statusGrid = document.getElementById("statusGrid");
const patentGrid = document.getElementById("patentGrid");
const demoGrid = document.getElementById("demoGrid");
const securityList = document.getElementById("securityList");
const patentSearch = document.getElementById("patentSearch");
const activityLog = document.getElementById("activityLog");
const patentAlert = document.getElementById("patentAlert");
const snapshotMeta = document.getElementById("snapshotMeta");
const logSummary = document.getElementById("logSummary");
const offlineBanner = document.getElementById("offlineBanner");
const logStorageKey = "livingFederationActivityLog";

const statusItems = [
  { label: "Governance Sync", value: "Active", detail: "Policy pack 1.3.2" },
  { label: "MCP Gateway", value: "Healthy", detail: "Allowlist enforced" },
  { label: "Intel Edge", value: "Ready", detail: "3 queues online" },
  { label: "DocsGuardian", value: "Passing", detail: "0 drift alerts" },
  { label: "HeadyMake", value: "Layer-Verified", detail: "Structure proof queued" },
  { label: "HeadyField", value: "Regenerating", detail: "Soil score +4.6%" },
  { label: "HeadyLegacy", value: "Monitoring", detail: "Biometric check-ins active" },
];

const securityItems = [
  "Localhost binding enforced for internal services.",
  "No cross-vertical data exchange; metadata routing only.",
  "JWT validation + origin allowlists for tool calls.",
  "Audit logs redact sensitive payload fields.",
  "Deterministic build artifacts tracked via DocsGuardian.",
  "HeadyMake layer hashes signed with rotating keys.",
  "HeadyField oracle validates sensor signatures before payouts.",
  "HeadyLegacy succession triggers require multi-party approval.",
];

const demoActions = [
  {
    title: "Policy Drift Check",
    description: "Simulate policy bundle verification and rollback gating.",
    action: "Run drift scan",
  },
  {
    title: "HeadyReflect Cycle",
    description: "Review a reflective decision gate before execution.",
    action: "Open reflection",
  },
  {
    title: "HeadyConductor",
    description: "Orchestrate a spoke registration handshake.",
    action: "Register spoke",
  },
  {
    title: "HeadyMake Proof",
    description: "Verify a layer-by-layer structure certificate for a printed part.",
    action: "Verify build",
  },
  {
    title: "HeadyField Oracle",
    description: "Simulate soil telemetry crossing a payout threshold.",
    action: "Trigger payout",
  },
  {
    title: "HeadyLegacy Succession",
    description: "Preview biometric inactivity and shard recovery workflow.",
    action: "Review succession",
  },
];

const moduleGrid = document.getElementById("moduleGrid");
const moduleCards = [
  {
    title: "HeadyMake · Proof-of-Structure",
    detail: "Layer scan fidelity: 99.98%",
    description: "In-situ scanners hash each layer and sign attestations to produce a tamper-proof build certificate.",
  },
  {
    title: "HeadyField · Regenerative Oracle",
    detail: "Soil score: 82 · payout ready",
    description: "Telemetry from soil sensors unlocks rewards when regeneration metrics improve.",
  },
  {
    title: "HeadyLegacy · Sovereign Succession",
    detail: "Check-in SLA: 7 days",
    description: "Biometric monitoring and shard-based recovery protect identity and assets.",
  },
];

let patents = [];
const actionButtons = document.querySelectorAll("[data-action]");
const maxLogEntries = 25;
let snapshotState = null;
const sessionStart = new Date().toISOString();

const renderStatus = () => {
  statusGrid.innerHTML = "";
  statusItems.forEach((item) => {
    const div = document.createElement("div");
    div.className = "status-pill";
    div.innerHTML = `<strong>${item.label}</strong><p>${item.value}</p><small>${item.detail}</small>`;
    statusGrid.appendChild(div);
  });
};

const loadLogEntries = () => {
  try {
    const stored = JSON.parse(localStorage.getItem(logStorageKey));
    return Array.isArray(stored) ? stored : [];
  } catch (error) {
    return [];
  }
};

const saveLogEntries = (entries) => {
  localStorage.setItem(logStorageKey, JSON.stringify(entries));
};

const addLogEntry = (message) => {
  const entries = loadLogEntries();
  const timestamp = new Date().toISOString();
  entries.unshift({ message, timestamp });
  const trimmed = entries.slice(0, maxLogEntries);
  saveLogEntries(trimmed);
  renderLog(trimmed);
};

const clearLogEntries = () => {
  saveLogEntries([]);
  renderLog([]);
};

const exportLogEntries = () => {
  const entries = loadLogEntries();
  const payload = {
    exported_at: new Date().toISOString(),
    session_started_at: sessionStart,
    search_filter: patentSearch?.value ?? "",
    snapshot: snapshotState,
    entries,
  };
  const blob = new Blob([JSON.stringify(payload, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = `living-federation-log-${payload.exported_at}.json`;
  document.body.appendChild(anchor);
  anchor.click();
  anchor.remove();
  URL.revokeObjectURL(url);
  addLogEntry("Exported activity log.");
};

const renderLog = (entries = loadLogEntries()) => {
  if (!activityLog) {
    return;
  }

  activityLog.innerHTML = "";
  if (logSummary) {
    const durationMs = Date.now() - Date.parse(sessionStart);
    const minutes = Math.max(1, Math.round(durationMs / 60000));
    logSummary.textContent = `${entries.length} actions recorded · ${minutes} min session.`;
  }
  if (!entries.length) {
    activityLog.textContent = "No recent activity yet.";
    return;
  }

  entries.forEach((entry) => {
    const row = document.createElement("div");
    row.textContent = `${entry.timestamp} — ${entry.message}`;
    activityLog.appendChild(row);
  });
};

const renderSecurity = () => {
  securityList.innerHTML = "";
  securityItems.forEach((item) => {
    const li = document.createElement("li");
    li.textContent = item;
    securityList.appendChild(li);
  });
};

const renderDemos = () => {
  demoGrid.innerHTML = "";
  demoActions.forEach((demo) => {
    const card = document.createElement("div");
    card.className = "demo-card";
    card.innerHTML = `
      <h3>${demo.title}</h3>
      <p>${demo.description}</p>
      <button class="ghost-button" type="button" data-demo-action="${demo.title}">${demo.action}</button>
    `;
    demoGrid.appendChild(card);
  });
};

const renderModules = () => {
  if (!moduleGrid) {
    return;
  }
  moduleGrid.innerHTML = "";
  moduleCards.forEach((module) => {
    const card = document.createElement("div");
    card.className = "card";
    card.innerHTML = `
      <h3>${module.title}</h3>
      <p class="meta">${module.detail}</p>
      <p>${module.description}</p>
    `;
    moduleGrid.appendChild(card);
  });
};

const renderPatents = (filter = "") => {
  const query = filter.trim().toLowerCase();
  const filtered = patents.filter((patent) => {
    return [patent.number, patent.title, patent.status, ...patent.tags]
      .join(" ")
      .toLowerCase()
      .includes(query);
  });

  patentGrid.innerHTML = "";

  if (!filtered.length) {
    patentGrid.innerHTML = '<div class="card"><h3>No matches</h3><p>Try a different filter term.</p></div>';
    return;
  }

  filtered.forEach((patent) => {
    const card = document.createElement("div");
    card.className = "card";
    card.innerHTML = `
      <h3>${patent.title}</h3>
      <p class="meta">Patent ${patent.number} · ${patent.status}</p>
      <p class="meta">${patent.assignment ?? "Assignment pending"}</p>
      <p>${patent.summary}</p>
      <p class="meta">Integration: ${patent.integration}</p>
      <p class="meta">Tags: ${patent.tags.join(", ")}</p>
    `;
    patentGrid.appendChild(card);
  });
};

const showPatentAlert = (message) => {
  if (!patentAlert) {
    return;
  }

  if (!message) {
    patentAlert.classList.remove("is-visible");
    patentAlert.textContent = "";
    return;
  }

  patentAlert.textContent = message;
  patentAlert.classList.add("is-visible");
};

const validatePatents = (data) => {
  if (!Array.isArray(data)) {
    return { ok: false, message: "Patent manifest is not a list." };
  }

  for (const entry of data) {
    if (!entry || typeof entry !== "object") {
      return { ok: false, message: "Patent entry missing required fields." };
    }
    const required = ["number", "title", "status", "summary", "integration", "tags", "assignment"];
    const missing = required.filter((key) => !(key in entry));
    if (missing.length) {
      return { ok: false, message: `Patent entry missing fields: ${missing.join(", ")}.` };
    }
    if (!Array.isArray(entry.tags)) {
      return { ok: false, message: "Patent tags must be an array." };
    }
  }

  return { ok: true };
};

const validateManifest = (data) => {
  if (!data || typeof data !== "object") {
    return { ok: false, message: "Manifest is not an object." };
  }
  if (!data.snapshot || typeof data.snapshot !== "object") {
    return { ok: false, message: "Manifest snapshot missing." };
  }
  const requiredSnapshot = ["version", "generated_at", "source", "schema_version", "manifest_id"];
  const missingSnapshot = requiredSnapshot.filter((key) => !(key in data.snapshot));
  if (missingSnapshot.length) {
    return { ok: false, message: `Snapshot missing fields: ${missingSnapshot.join(", ")}.` };
  }
  if (!Array.isArray(data.patents)) {
    return { ok: false, message: "Manifest patents list missing." };
  }
  return validatePatents(data.patents);
};

const updateSnapshotMeta = (snapshot) => {
  if (!snapshotMeta) {
    return;
  }
  snapshotState = snapshot;
  if (!snapshot) {
    snapshotMeta.textContent = "No snapshot loaded.";
    return;
  }
  snapshotMeta.textContent = `${snapshot.version} · ${snapshot.generated_at} · ${snapshot.source} · schema ${snapshot.schema_version}`;
};

const attachDemoHandlers = () => {
  actionButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const action = button.getAttribute("data-action") || "Action";
      if (action === "export") {
        exportLogEntries();
        return;
      }
      if (action === "clear-log") {
        const confirmed = window.confirm("Clear the local activity log?");
        if (confirmed) {
          clearLogEntries();
          addLogEntry("Cleared activity log.");
        }
        return;
      }
      addLogEntry(`Primary action triggered: ${action}.`);
    });
  });

  demoGrid.addEventListener("click", (event) => {
    const target = event.target;
    if (target instanceof HTMLElement && target.dataset.demoAction) {
      addLogEntry(`Demo executed: ${target.dataset.demoAction}.`);
    }
  });
};

const init = async () => {
renderStatus();
renderSecurity();
renderDemos();
renderModules();
  renderLog();
  attachDemoHandlers();

  try {
    const response = await fetch("data/manifest.json");
    const data = await response.json();
    const validation = validateManifest(data);
    if (!validation.ok) {
      showPatentAlert(`Patent manifest validation failed: ${validation.message}`);
      patents = [];
      if (offlineBanner) {
        offlineBanner.classList.remove("is-visible");
      }
    } else {
      showPatentAlert("");
      patents = data.patents;
      updateSnapshotMeta(data.snapshot);
      if (offlineBanner) {
        offlineBanner.classList.remove("is-visible");
      }
    }
  } catch (error) {
    showPatentAlert("Patent manifest unavailable. Displaying fallback metadata.");
    updateSnapshotMeta(null);
    if (offlineBanner) {
      offlineBanner.classList.add("is-visible");
    }
    patents = [
      {
        number: "00",
        title: "Fallback Snapshot",
        status: "Offline",
        summary: "Local fallback metadata used because the manifest could not be loaded.",
        integration: "Local-only mode",
        tags: ["offline", "fallback"],
      },
    ];
  }
  renderPatents();
};

patentSearch.addEventListener("input", (event) => {
  renderPatents(event.target.value);
});

init();
