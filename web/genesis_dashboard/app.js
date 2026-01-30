const statusGrid = document.getElementById("statusGrid");
const kaizenGrid = document.getElementById("kaizenGrid");
const signalGrid = document.getElementById("signalGrid");
const snapshotMeta = document.getElementById("snapshotMeta");

const actions = document.querySelectorAll("[data-action]");

const renderStatus = (items) => {
  statusGrid.innerHTML = "";
  items.forEach((item) => {
    const div = document.createElement("div");
    div.className = "status-pill";
    div.innerHTML = `<strong>${item.label}</strong><p>${item.value}</p><small>${item.detail}</small>`;
    statusGrid.appendChild(div);
  });
};

const renderCards = (target, items, className) => {
  target.innerHTML = "";
  items.forEach((item) => {
    const card = document.createElement("div");
    card.className = className;
    card.innerHTML = `
      <h3>${item.title}</h3>
      <p>${item.summary}</p>
      <p class="meta">Owner: ${item.owner}</p>
      <p class="meta">Status: ${item.status}</p>
    `;
    target.appendChild(card);
  });
};

const init = async () => {
  const response = await fetch("data/manifest.json");
  const payload = await response.json();

  snapshotMeta.textContent = `${payload.snapshot.version} · ${payload.snapshot.generated_at} · ${payload.snapshot.source}`;
  renderStatus(payload.status);
  renderCards(kaizenGrid, payload.kaizen, "card");
  renderCards(signalGrid, payload.signals, "signal-card");
};

actions.forEach((button) => {
  button.addEventListener("click", () => {
    const action = button.dataset.action;
    console.log(`Genesis action: ${action}`);
  });
});

init();
