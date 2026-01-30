export const createOverlay = () => {
  const panel = document.querySelector("#overlay-panel");
  const title = panel.querySelector("[data-overlay-title]");
  const description = panel.querySelector("[data-overlay-description]");
  const logic = panel.querySelector("[data-overlay-logic]");
  const ip = panel.querySelector("[data-overlay-ip]");

  const setVisible = (visible) => {
    panel.setAttribute("data-visible", visible ? "true" : "false");
  };

  const update = (info) => {
    if (!info) {
      title.textContent = "Select a body part";
      description.textContent = "Hover or click on a highlighted region to learn more.";
      logic.textContent = "";
      ip.textContent = "";
      return;
    }
    title.textContent = info.name;
    description.textContent = info.description;
    logic.textContent = info.logic;
    ip.textContent = info.ip;
  };

  return {
    setVisible,
    update,
  };
};
