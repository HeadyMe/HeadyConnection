from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

from config import ServiceConfig, register_with_hub
from middleware import PIIScrubMiddleware
from mode import ModeController

app = FastAPI(title="HeadySandbox")
app.add_middleware(PIIScrubMiddleware)
mode_controller = ModeController()


@app.on_event("startup")
async def register_node() -> None:
    config = ServiceConfig()
    token = register_with_hub(config)
    app.state.execution_token = token


@app.post("/evaluate")
async def evaluate(request: Request):
    payload = request.state.sanitized_payload
    return {"mode": mode_controller.mode, "payload": payload}


@app.post("/mode")
async def set_mode(payload: dict):
    mode_controller.set_mode(payload.get("mode", "Standard"))
    return {"mode": mode_controller.mode}


@app.get("/health")
async def health_check():
    return {"status": "ok", "policy": "hipaa-sandbox"}


@app.get("/")
async def root():
    html = """
    <html>
      <head><title>HeadySandbox</title></head>
      <body>
        <h1>HeadySandbox</h1>
        <p>Clinical sandbox with PII scrubbing and mode switching.</p>
      </body>
    </html>
    """
    return HTMLResponse(content=html)
