import React from "react";

const metrics = [
  { label: "Open Tasks", value: 12 },
  { label: "Events Today", value: 3 },
  { label: "Unread Messages", value: 8 },
  { label: "Budget Remaining", value: "$4,200" },
];

const Dashboard = () => (
  <section className="dashboard">
    <h2>Overview</h2>
    <div className="metric-grid">
      {metrics.map((metric) => (
        <div key={metric.label} className="metric-card">
          <p className="metric-label">{metric.label}</p>
          <p className="metric-value">{metric.value}</p>
        </div>
      ))}
    </div>
    <div className="dashboard-grid">
      <div className="panel">
        <h3>Priority Tasks</h3>
        <ul>
          <li>Finalize quarterly plan</li>
          <li>Review calendar sync conflicts</li>
          <li>Approve vendor invoice</li>
        </ul>
      </div>
      <div className="panel">
        <h3>Recent Activity</h3>
        <ul>
          <li>Uploaded roadmap draft</li>
          <li>Sent message to finance</li>
          <li>Scheduled follow-up meeting</li>
        </ul>
      </div>
    </div>
  </section>
);

export default Dashboard;
