import fs from "node:fs";
import path from "node:path";

const root = path.resolve(process.cwd(), "apps/heady_admin_ui");
const targets = [
  path.join(root, "backend/server.js"),
  path.join(root, "frontend/src/App.jsx"),
];

const missing = targets.filter((file) => !fs.existsSync(file));
if (missing.length) {
  console.error("Missing files:", missing.join(", "));
  process.exit(1);
}

console.log("Placeholder lint passed");
