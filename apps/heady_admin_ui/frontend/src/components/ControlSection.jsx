import React from "react";

const ControlSection = ({ title, children }) => (
  <div className="panel">
    <h3>{title}</h3>
    {children}
  </div>
);

export default ControlSection;
