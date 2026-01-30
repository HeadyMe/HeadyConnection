const { useState } = React;

const initialEntries = [
  { id: 1, text: "Morning check-in complete", status: "approved" },
  { id: 2, text: "Homework reading session", status: "approved" },
  { id: 3, text: "Message pending review", status: "pending" },
];

function DotButton({ label, onClick, active = false }) {
  return (
    <button
      className={`six-dot-button${active ? " is-active" : ""}`}
      onClick={onClick}
      aria-pressed={active}
    >
      <span>{label}</span>
      <span className="dot-grid" aria-hidden="true">
        <span className="dot"></span>
        <span className="dot"></span>
        <span className="dot"></span>
        <span className="dot"></span>
        <span className="dot"></span>
        <span className="dot"></span>
      </span>
    </button>
  );
}

function App() {
  const [entries, setEntries] = useState(initialEntries);
  const [filter, setFilter] = useState("all");

  const filtered = entries.filter((entry) =>
    filter === "all" ? true : entry.status === filter
  );

  return (
    <div className="portal">
      <header>
        <h1>Parent Portal</h1>
        <p>Review activity, manage permissions, and keep Junior safe.</p>
      </header>
      <section className="controls">
        <DotButton
          label="All"
          onClick={() => setFilter("all")}
          active={filter === "all"}
        />
        <DotButton
          label="Approved"
          onClick={() => setFilter("approved")}
          active={filter === "approved"}
        />
        <DotButton
          label="Pending"
          onClick={() => setFilter("pending")}
          active={filter === "pending"}
        />
      </section>
      <section className="entries" aria-live="polite">
        {filtered.length === 0 ? (
          <div className="entry empty">
            <span className="status">all clear</span>
            <p>No entries match this filter.</p>
          </div>
        ) : (
          filtered.map((entry) => (
            <article key={entry.id} className={`entry ${entry.status}`}>
              <span className="status">{entry.status}</span>
              <p>{entry.text}</p>
            </article>
          ))
        )}
      </section>
      <section className="permissions">
        <h2>Permissions</h2>
        <div className="permission-grid">
          <div>
            <h3>Messaging</h3>
            <p>Allow trusted contacts only.</p>
            <DotButton label="Manage Contacts" />
          </div>
          <div>
            <h3>Activity Windows</h3>
            <p>Set daily usage windows.</p>
            <DotButton label="Configure Schedule" />
          </div>
          <div>
            <h3>Content Filters</h3>
            <p>Update prohibited topics list.</p>
            <DotButton label="Review Filters" />
          </div>
        </div>
      </section>
    </div>
  );
}

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<App />);
