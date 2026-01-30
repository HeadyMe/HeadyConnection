import fs from "node:fs";
import path from "node:path";

const root = path.resolve(process.cwd(), "apps/heady_admin_ui/backend");
const specPath = path.join(root, "openapi.yaml");
if (!fs.existsSync(specPath)) {
  console.error("Missing openapi.yaml");
  process.exit(1);
}

const spec = fs.readFileSync(specPath, "utf-8");
const required = ["/api/profile", "/api/tasks", "/api/documents", "/api/events", "/api/messages", "/api/finance", "/api/audit"];
const missing = required.filter((route) => !spec.includes(route));
if (missing.length) {
  console.error(`OpenAPI missing routes: ${missing.join(", ")}`);
  process.exit(1);
}

console.log("API contract validation passed");
