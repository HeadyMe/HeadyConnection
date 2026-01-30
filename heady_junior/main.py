from __future__ import annotations

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.responses import HTMLResponse

from config import ServiceConfig, register_with_hub
from safety import SafetyFilter

app = FastAPI(title="HeadyJunior")
filter_policy = SafetyFilter()
activity_log = []


def require_parental_token(parental_token: str = Header(..., alias="parental_token")) -> str:
    config = ServiceConfig()
    if parental_token != config.parental_token:
        raise HTTPException(status_code=403, detail="Invalid parental token")
    return parental_token


@app.on_event("startup")
async def register_node() -> None:
    config = ServiceConfig()
    token = register_with_hub(config)
    app.state.execution_token = token


@app.post("/entries", dependencies=[Depends(require_parental_token)])
async def create_entry(payload: dict):
    text = payload.get("text", "")
    if not filter_policy.is_allowed(text):
        raise HTTPException(status_code=400, detail="Content blocked")
    activity_log.append({"text": text})
    return {"status": "accepted", "count": len(activity_log)}


@app.get("/activity", dependencies=[Depends(require_parental_token)])
async def list_activity():
    return {"entries": activity_log}


@app.get("/health")
async def health_check():
    return {"status": "ok", "policy": "coppa-walled-garden"}


@app.get("/")
async def root():
    html = """
    <html>
      <head><title>HeadyJunior</title></head>
      <body>
        <h1>HeadyJunior</h1>
        <p>COPPA-compliant walled garden with parental oversight.</p>
      </body>
    </html>
    """
    return HTMLResponse(content=html)
