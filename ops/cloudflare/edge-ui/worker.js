const STATUS_MAP = {
  ok: { label: "Operational", color: "#16a34a" },
  degraded: { label: "Degraded", color: "#f59e0b" },
  outage: { label: "Outage", color: "#dc2626" },
  unknown: { label: "Unknown", color: "#64748b" },
};

const renderPage = ({ status, summary, updatedAt }) => {
  const statusEntry = STATUS_MAP[status] ?? STATUS_MAP.unknown;
  const indicator = statusEntry.color;
  const label = statusEntry.label;
  return `<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Trust Center Status</title>
    <style>
      body { font-family: system-ui, sans-serif; padding: 24px; background: #0f172a; color: #e2e8f0; }
      .status { display: flex; align-items: center; gap: 12px; }
      .dot { width: 12px; height: 12px; border-radius: 999px; background: ${indicator}; box-shadow: 0 0 8px ${indicator}; }
      .panel { background: #111827; padding: 16px 20px; border-radius: 12px; border: 1px solid #1f2937; }
    </style>
  </head>
  <body>
    <div class="panel">
      <h1>System Status</h1>
      <div class="status">
        <span class="dot"></span>
        <strong>${label}</strong>
      </div>
      <p>${summary}</p>
      ${updatedAt ? `<small>Updated ${updatedAt}</small>` : ""}
    </div>
  </body>
</html>`;
};

const readStatus = async (env) => {
  if (!env.STATUS_FEED_URL) {
    return { status: "unknown", summary: "Status feed unavailable", updatedAt: null };
  }
  try {
    const response = await fetch(env.STATUS_FEED_URL, { cf: { cacheTtl: 30, cacheEverything: true } });
    if (!response.ok) {
      return { status: "degraded", summary: "Status feed unavailable", updatedAt: null };
    }
    const data = await response.json();
    return {
      status: data.status ?? "unknown",
      summary: data.summary ?? "Status feed unavailable",
      updatedAt: data.updated_at ?? null,
    };
  } catch {
    return { status: "degraded", summary: "Status feed unavailable", updatedAt: null };
  }
};

export default {
  async fetch(request, env) {
    const status = await readStatus(env);
    return new Response(renderPage(status), {
      headers: {
        "content-type": "text/html; charset=utf-8",
        "cache-control": "public, max-age=30",
      },
    });
  },
};
