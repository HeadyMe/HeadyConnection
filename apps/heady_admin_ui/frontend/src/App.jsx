import React, { useState } from "react";
import Dashboard from "./components/Dashboard.jsx";
import ControlPanel from "./components/ControlPanel.jsx";
import ModuleSidebar from "./components/ModuleSidebar.jsx";
import ModulePlaceholder from "./components/ModulePlaceholder.jsx";

const App = () => {
  const [activeModule, setActiveModule] = useState("dashboard");

  return (
    <div className="app-shell">
      <header className="app-header">
        <div>
          <h1>Heady Admin UI</h1>
          <p>End-to-end personal operations dashboard</p>
        </div>
        <div className="status-pill">Secure · Audited · Local-first</div>
      </header>
      <div className="app-body">
        <ModuleSidebar activeModule={activeModule} onSelect={setActiveModule} />
        <main className="app-main">
          {activeModule === "dashboard" && <Dashboard />}
          {activeModule === "control" && <ControlPanel />}
          {activeModule === "tasks" && (
            <ModulePlaceholder
              title="Tasks & Projects"
              description="Track deadlines, priority, and progress across projects."
              items={["Review roadmap", "Draft investor memo", "Schedule sprint retro"]}
            />
          )}
          {activeModule === "calendar" && (
            <ModulePlaceholder
              title="Calendar & Scheduling"
              description="Sync external calendars and manage reminders."
              items={["Design review — 2pm", "Investor call — 4pm"]}
            />
          )}
          {activeModule === "documents" && (
            <ModulePlaceholder
              title="Documents & Content"
              description="Versioned document library with templates and approvals."
              items={["Ops runbook v3", "Pricing sheet", "Compliance checklist"]}
            />
          )}
          {activeModule === "messages" && (
            <ModulePlaceholder
              title="Communications"
              description="Unified inbox for email, chat, and notifications."
              items={["Finance updates", "Security alert", "Customer request"]}
            />
          )}
          {activeModule === "finance" && (
            <ModulePlaceholder
              title="Finance & Subscriptions"
              description="Track budgets, invoices, and recurring services."
              items={["Monthly burn: $82k", "Upcoming invoice: $4.5k"]}
            />
          )}
          {activeModule === "settings" && (
            <ModulePlaceholder
              title="Settings & Customization"
              description="Configure modules, layouts, themes, and integrations."
              items={["Theme: Dark", "Integrations: 6 active"]}
            />
          )}
        </main>
      </div>
    </div>
  );
};

export default App;
