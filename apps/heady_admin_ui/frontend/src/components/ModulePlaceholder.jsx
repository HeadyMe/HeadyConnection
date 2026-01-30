import React from "react";

const ModulePlaceholder = ({ title, description, items = [] }) => (
  <section className="panel">
    <h2>{title}</h2>
    <p>{description}</p>
    {items.length > 0 && (
      <ul>
        {items.map((item) => (
          <li key={item}>{item}</li>
        ))}
      </ul>
    )}
  </section>
);

export default ModulePlaceholder;
