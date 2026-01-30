import express, { Request, Response } from "express";
import { createRemoteJWKSet, jwtVerify } from "jose";
import fs from "node:fs";
import path from "node:path";

interface UpstreamConfig {
  name: string;
  baseUrl: string;
  allowedTools: string[];
}

interface McpConfig {
  upstreams: UpstreamConfig[];
  destructiveTools: string[];
}

const maxBodyBytes = Number(process.env.MAX_BODY_BYTES ?? 1048576);
const app = express();
app.use(express.json({ limit: maxBodyBytes }));

const configPath = process.env.MCP_CONFIG_PATH ?? path.join(process.cwd(), "mcp.config.json");
const mcpConfig: McpConfig = fs.existsSync(configPath)
  ? JSON.parse(fs.readFileSync(configPath, "utf-8"))
  : JSON.parse(fs.readFileSync(path.join(process.cwd(), "mcp.config.json.example"), "utf-8"));

const hostAllowlist = new Set((process.env.HOST_ALLOWLIST ?? "localhost,127.0.0.1").split(","));
const originAllowlist = new Set((process.env.ORIGIN_ALLOWLIST ?? "").split(",").filter(Boolean));
const destructiveTools = new Set(mcpConfig.destructiveTools ?? []);

const jwtSecret = process.env.JWT_HS256_SECRET;
const jwksUrl = process.env.JWT_JWKS_URL;
const reflectEnforce = process.env.HEADY_REFLECT_ENFORCE === "1";
const rateLimitRps = Number(process.env.RATE_LIMIT_RPS ?? 5);
const rateLimitWindowMs = Number(process.env.RATE_LIMIT_WINDOW_MS ?? 1000);
const rateLimitTtlMs = Number(process.env.RATE_LIMIT_TTL_MS ?? rateLimitWindowMs * 2);
const strictOrigin = process.env.STRICT_ORIGIN === "1";
const jwtAudience = process.env.JWT_AUDIENCE;
const optimisticRaa = process.env.OPTIMISTIC_RAA === "1";

const rateBuckets = new Map<string, { count: number; windowStart: number }>();

const jsonLog = (level: string, message: string, meta: Record<string, unknown> = {}) => {
  console.log(JSON.stringify({ level, message, ...meta, timestamp: new Date().toISOString() }));
};

const requestId = () => `req_${Math.random().toString(36).slice(2, 10)}`;

const validateConfig = (config: McpConfig) => {
  const names = new Set<string>();
  for (const upstream of config.upstreams ?? []) {
    if (!upstream.name || names.has(upstream.name)) {
      throw new Error(`Invalid upstream name: ${upstream.name}`);
    }
    names.add(upstream.name);
    if (!upstream.baseUrl) {
      throw new Error(`Missing baseUrl for upstream: ${upstream.name}`);
    }
    try {
      new URL(upstream.baseUrl);
    } catch {
      throw new Error(`Invalid baseUrl for upstream: ${upstream.name}`);
    }
    if (!upstream.allowedTools || upstream.allowedTools.length === 0) {
      throw new Error(`No allowedTools configured for upstream: ${upstream.name}`);
    }
  }
};

const verifyJwt = async (token?: string) => {
  if (!token) {
    throw new Error("Missing JWT");
  }
  const raw = token.replace(/^Bearer\s+/i, "");
  if (jwksUrl) {
    const jwks = createRemoteJWKSet(new URL(jwksUrl));
    return jwtVerify(raw, jwks, jwtAudience ? { audience: jwtAudience } : undefined);
  }
  if (!jwtSecret) {
    throw new Error("No JWT secret configured");
  }
  const secret = new TextEncoder().encode(jwtSecret);
  return jwtVerify(raw, secret, { algorithms: ["HS256"], ...(jwtAudience ? { audience: jwtAudience } : {}) });
};

const allowOrigin = (req: Request, res: Response, next: () => void) => {
  const origin = req.headers.origin;
  if (strictOrigin && originAllowlist.size > 0 && !origin) {
    return res.status(403).json({ error: "Origin required" });
  }
  if (origin && originAllowlist.size > 0 && !originAllowlist.has(origin)) {
    return res.status(403).json({ error: "Origin not allowed" });
  }
  if (origin && originAllowlist.has(origin)) {
    res.setHeader("Access-Control-Allow-Origin", origin);
    res.setHeader("Vary", "Origin");
    res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
    res.setHeader("Access-Control-Allow-Headers", "authorization, content-type, x-confirm-destructive");
  }
  return next();
};

const attachRequestId = (_req: Request, res: Response, next: () => void) => {
  const reqId = requestId();
  res.locals.reqId = reqId;
  res.setHeader("x-request-id", reqId);
  next();
};

app.use(attachRequestId);
app.use(allowOrigin);

app.options("/mcp/:upstream/tool", (req, res) => {
  if (strictOrigin && originAllowlist.size > 0 && !req.headers.origin) {
    return res.status(403).json({ error: "Origin required" });
  }
  return res.sendStatus(204);
});

app.post("/mcp/:upstream/tool", async (req, res) => {
  const reqId = res.locals.reqId ?? requestId();
  const clientKey = req.ip ?? req.socket.remoteAddress ?? "unknown";
  const now = Date.now();
  const bucket = rateBuckets.get(clientKey) ?? { count: 0, windowStart: now };
  if (now - bucket.windowStart > rateLimitWindowMs) {
    bucket.count = 0;
    bucket.windowStart = now;
  }
  bucket.count += 1;
  rateBuckets.set(clientKey, bucket);
  if (now - bucket.windowStart > rateLimitTtlMs) {
    rateBuckets.delete(clientKey);
  } else if (rateBuckets.size > 1000) {
    for (const [key, entry] of rateBuckets.entries()) {
      if (now - entry.windowStart > rateLimitTtlMs) {
        rateBuckets.delete(key);
      }
    }
  }
  if (bucket.count > rateLimitRps) {
    jsonLog("warn", "Rate limit exceeded", { clientKey, reqId });
    return res.status(429).json({ error: "Rate limit exceeded" });
  }
  const host = req.hostname;
  if (!hostAllowlist.has(host)) {
    jsonLog("warn", "Host blocked", { host, reqId });
    return res.status(403).json({ error: "Host not allowed" });
  }

  try {
    await verifyJwt(req.headers.authorization);
  } catch (error) {
    jsonLog("warn", "JWT rejected", { error: (error as Error).message, reqId });
    return res.status(401).json({ error: "Unauthorized" });
  }

  const { tool, payload, reflection } = req.body as {
    tool: string;
    payload?: Record<string, unknown>;
    reflection?: { question: string; answer: string; risk: string };
  };
  const payloadBytes = Buffer.byteLength(JSON.stringify(payload ?? {}), "utf8");
  if (payloadBytes > maxBodyBytes) {
    jsonLog("warn", "Payload too large", { payloadBytes, reqId });
    return res.status(413).json({ error: "Payload too large" });
  }

  if (!tool) {
    return res.status(400).json({ error: "Missing tool" });
  }

  if (reflectEnforce) {
    if (!reflection || !reflection.question || !reflection.answer || !reflection.risk) {
      return res.status(400).json({ error: "Reflection required" });
    }
  }

  const upstream = mcpConfig.upstreams.find((entry) => entry.name === req.params.upstream);
  if (!upstream) {
    return res.status(404).json({ error: "Unknown upstream" });
  }

  if (!upstream.allowedTools.includes(tool)) {
    jsonLog("warn", "Tool not allowed", { tool, reqId });
    return res.status(403).json({ error: "Tool not allowed" });
  }

  if (destructiveTools.has(tool)) {
    const confirm = req.headers["x-confirm-destructive"] === "true";
    if (!confirm) {
      return res.status(428).json({ error: "Destructive tool confirmation required" });
    }
  }

  jsonLog("info", "Tool request accepted", { tool, upstream: upstream.name, reqId, optimisticRaa });

  return res.json({ status: "accepted", upstream: upstream.name, tool, payload, reqId });
});

app.get("/health", (_, res) => {
  const reqId = res.locals.reqId ?? requestId();
  res.json({ status: "ok", upstreams: mcpConfig.upstreams.map((u) => u.name), reqId });
});

const port = Number(process.env.PORT ?? 8081);
const host = process.env.BIND_HOST ?? "127.0.0.1";

try {
  validateConfig(mcpConfig);
} catch (error) {
  jsonLog("error", "Invalid MCP config", { error: (error as Error).message });
  process.exit(1);
}

app.listen(port, host, () => {
  jsonLog("info", "MCP gateway listening", { host, port });
  if (optimisticRaa) {
    jsonLog("info", "Optimistic RAA flag enabled (no-op)", { host, port });
  }
});
