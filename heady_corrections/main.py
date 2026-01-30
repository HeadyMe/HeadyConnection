from __future__ import annotations

import os

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from config import ServiceConfig, register_with_hub
from drift_engine import SemanticDrift
from risk_scoring import calculate_risk_score

app = FastAPI(title="HeadyCorrections")

semantic_drift = SemanticDrift()
drift_threshold = float(os.getenv("DRIFT_THRESHOLD", "7"))


@app.on_event("startup")
async def register_node() -> None:
    config = ServiceConfig()
    token = register_with_hub(config)
    app.state.execution_token = token


@app.post("/evaluate")
async def evaluate(narrative: str):
    result = semantic_drift.evaluate_risk(narrative, threshold=drift_threshold)
    return {"variance_score": result.variance_score, "risk_alert": result.risk_alert}


@app.post("/risk-score")
async def risk_score(payload: dict):
    score = calculate_risk_score(payload)
    return {"score": score}


@app.get("/health")
async def health_check():
    return {"status": "ok", "policy": "criminogenic-monitoring"}


@app.get("/")
async def root():
    html = """
    <html>
      <head><title>HeadyCorrections</title></head>
      <body>
        <h1>HeadyCorrections</h1>
        <p>Criminogenic monitoring with semantic drift detection.</p>
      </body>
    </html>
    """
    return HTMLResponse(content=html)
