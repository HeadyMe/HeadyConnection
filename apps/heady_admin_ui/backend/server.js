import express from "express";
import cors from "cors";
import helmet from "helmet";
import morgan from "morgan";

const app = express();
const port = process.env.PORT || 9000;
const token = process.env.HEADY_ADMIN_TOKEN || "changeme";

const data = {
  profile: {
    name: "Heady Admin",
    email: "admin@example.com",
    notifications: { email: true, sms: false },
  },
  tasks: [],
  documents: [],
  events: [],
  messages: [],
  finance: [],
  audit: [],
};

const audit = (action, payload = {}) => {
  data.audit.push({
    id: `audit_${Date.now()}`,
    action,
    payload,
    ts: new Date().toISOString(),
  });
};

const auth = (req, res, next) => {
  const authHeader = req.headers.authorization || "";
  if (authHeader !== `Bearer ${token}`) {
    return res.status(401).json({ error: "Unauthorized" });
  }
  return next();
};

app.use(helmet());
app.use(cors());
app.use(express.json());
app.use(morgan("tiny"));
app.use(auth);

app.get("/api/profile", (req, res) => {
  res.json(data.profile);
});

app.put("/api/profile", (req, res) => {
  data.profile = { ...data.profile, ...req.body };
  audit("profile.update", req.body);
  res.json(data.profile);
});

const registerCollection = (key) => {
  app.get(`/api/${key}`, (req, res) => {
    res.json(data[key]);
  });

  app.post(`/api/${key}`, (req, res) => {
    const entry = { id: `${key}_${Date.now()}`, ...req.body };
    data[key].push(entry);
    audit(`${key}.create`, entry);
    res.status(201).json(entry);
  });

  app.put(`/api/${key}/:id`, (req, res) => {
    const index = data[key].findIndex((item) => item.id === req.params.id);
    if (index === -1) {
      return res.status(404).json({ error: "Not found" });
    }
    data[key][index] = { ...data[key][index], ...req.body };
    audit(`${key}.update`, data[key][index]);
    return res.json(data[key][index]);
  });

  app.delete(`/api/${key}/:id`, (req, res) => {
    const index = data[key].findIndex((item) => item.id === req.params.id);
    if (index === -1) {
      return res.status(404).json({ error: "Not found" });
    }
    const [removed] = data[key].splice(index, 1);
    audit(`${key}.delete`, removed);
    return res.status(204).send();
  });
};

["tasks", "documents", "events", "messages", "finance"].forEach(registerCollection);

app.get("/api/audit", (req, res) => {
  res.json(data.audit);
});

app.listen(port, () => {
  console.log(`Heady Admin API listening on ${port}`);
});
