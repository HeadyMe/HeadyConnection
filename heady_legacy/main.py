from __future__ import annotations

import asyncio
import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from config import ServiceConfig, register_with_hub
from stimulus import MemoryTrigger, StimulusLoop
from storage import CloudArchiveClient, CloudArchiveConfig

app = FastAPI(title="HeadyLegacy")

reengagement_hours = int(os.getenv("REENGAGEMENT_INTERVAL_HOURS", "48"))
stimulus_loop = StimulusLoop(reengagement_hours=reengagement_hours)


def _on_trigger(trigger: MemoryTrigger) -> None:
    app.state.last_prompted = trigger.trigger_id


@app.on_event("startup")
async def register_node() -> None:
    config = ServiceConfig()
    token = register_with_hub(config)
    app.state.execution_token = token
    asyncio.create_task(stimulus_loop.scheduler(_on_trigger))


@app.post("/triggers")
async def add_trigger(payload: dict):
    trigger = MemoryTrigger(
        trigger_id=payload["trigger_id"],
        prompt_type=payload["prompt_type"],
        prompt_value=payload["prompt_value"],
    )
    stimulus_loop.add_trigger(trigger)
    return {"status": "added"}


@app.post("/activity")
async def record_activity():
    stimulus_loop.record_activity()
    return {"status": "recorded"}


@app.get("/archive/manifest")
async def archive_manifest(object_name: str, provider: str = "aws"):
    config = CloudArchiveConfig(
        provider=provider,
        bucket_name=os.getenv("ARCHIVE_BUCKET", "heady-legacy-archive"),
        region=os.getenv("ARCHIVE_REGION", "us-east-1"),
        kms_key_id=os.getenv("ARCHIVE_KMS_KEY", "alias/heady-legacy"),
    )
    client = CloudArchiveClient(config)
    return client.prepare_upload_manifest(object_name)


@app.get("/health")
async def health_check():
    return {"status": "ok", "policy": "archival-engagement"}


@app.get("/")
async def root():
    html = """
    <html>
      <head><title>HeadyLegacy</title></head>
      <body>
        <h1>HeadyLegacy</h1>
        <p>Autobiography and archival stimulus loop engine.</p>
      </body>
    </html>
    """
    return HTMLResponse(content=html)
