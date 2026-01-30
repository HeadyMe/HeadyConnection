import React from "react";

const MODULES = [
  { id: "dashboard", label: "Dashboard" },
  { id: "control", label: "Control Panel" },
  { id: "tasks", label: "Tasks" },
  { id: "calendar", label: "Calendar" },
  { id: "documents", label: "Documents" },
  { id: "messages", label: "Messages" },
  { id: "finance", label: "Finance" },
  { id: "settings", label: "Settings" },
];

const ModuleSidebar = ({ activeModule, onSelect }) => (
  <nav className="module-sidebar" aria-label="Primary modules">
    {MODULES.map((module) => (
      <button
        key={module.id}
        className={activeModule === module.id ? "active" : ""}
        onClick={() => onSelect(module.id)}
      >
        {module.label}
      </button>
    ))}
  </nav>
);

export default ModuleSidebar;
