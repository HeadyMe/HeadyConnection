import React from "react";
import ControlSection from "./ControlSection.jsx";

const ControlPanel = () => (
  <section className="control-panel">
    <h2>Control Panel</h2>
    <p>Manage modules, integrations, and security policies from a unified view.</p>
    <div className="control-grid">
      <ControlSection title="Authentication">
        <ul>
          <li>Active sessions: 2</li>
          <li>2FA: Enabled</li>
          <li>Token rotation: Weekly</li>
        </ul>
      </ControlSection>
      <ControlSection title="Integrations">
        <ul>
          <li>Google Workspace: Connected</li>
          <li>Slack: Pending token refresh</li>
          <li>Cloud Storage: Connected</li>
        </ul>
      </ControlSection>
      <ControlSection title="Audit & Recovery">
        <ul>
          <li>Audit log retention: 365 days</li>
          <li>Soft-delete enabled</li>
          <li>Last export: 2 hours ago</li>
        </ul>
      </ControlSection>
    </div>
  </section>
);

export default ControlPanel;
