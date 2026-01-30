from __future__ import annotations

import asyncio
import os
import time
import uuid
from dataclasses import dataclass, field
from typing import Dict, Optional
from urllib import request
from urllib.error import URLError

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, HttpUrl


@dataclass
class RegistryEntry:
    spoke_id: str
    vertical_type: str
    endpoint_url: str
    policy_version: str
    execution_token: str
    status: str = "ACTIVE"
    last_seen: float = field(default_factory=time.time)
    failed_heartbeats: int = 0


class SpokeRegistration(BaseModel):
    spoke_id: str = Field(..., min_length=3)
    vertical_type: str
    endpoint_url: HttpUrl
    policy_version: str


class RegistryState:
    def __init__(self) -> None:
        self._entries: Dict[str, RegistryEntry] = {}

    def all(self) -> Dict[str, RegistryEntry]:
        return self._entries

    def register(self, payload: SpokeRegistration) -> RegistryEntry:
        token = f"HX-{payload.spoke_id}-{uuid.uuid4().hex}"
        entry = RegistryEntry(
            spoke_id=payload.spoke_id,
            vertical_type=payload.vertical_type,
            endpoint_url=str(payload.endpoint_url),
            policy_version=payload.policy_version,
            execution_token=token,
        )
        self._entries[payload.spoke_id] = entry
        return entry

    def mark_seen(self, spoke_id: str) -> None:
        entry = self._entries.get(spoke_id)
        if entry:
            entry.last_seen = time.time()
            entry.failed_heartbeats = 0
            entry.status = "ACTIVE"

    def mark_failed(self, spoke_id: str) -> None:
        entry = self._entries.get(spoke_id)
        if not entry:
            return
        entry.failed_heartbeats += 1
        if entry.failed_heartbeats >= 2:
            entry.status = "SUSPENDED"
            entry.execution_token = "REVOKED"


def _load_allowed_verticals() -> set[str]:
    env_value = os.getenv("ALLOWED_SPOKES", "")
    if not env_value:
        return {"Bio", "Corrections", "Legacy", "Sandbox", "Junior"}
    return {value.strip().capitalize() for value in env_value.split(",") if value.strip()}


ALLOWED_VERTICALS = _load_allowed_verticals()
HEARTBEAT_INTERVAL_S = int(os.getenv("HEARTBEAT_INTERVAL_S", "60"))

app = FastAPI(title="HeadyConductor Central Registry")
registry = RegistryState()


def _safe_get(url: str, timeout_s: float = 2.0) -> bool:
    try:
        req = request.Request(url, method="GET")
        with request.urlopen(req, timeout=timeout_s) as response:
            return 200 <= response.status < 400
    except URLError:
        return False


async def _heartbeat_loop() -> None:
    while True:
        await asyncio.sleep(HEARTBEAT_INTERVAL_S)
        entries = [entry for entry in registry.all().values() if entry.status != "SUSPENDED"]
        tasks = []
        for entry in entries:
            if entry.status == "SUSPENDED":
                continue
            tasks.append(asyncio.to_thread(_safe_get, entry.endpoint_url.rstrip("/") + "/health"))
        if not tasks:
            continue
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for entry, result in zip(entries, results):
            if isinstance(result, Exception) or result is False:
                registry.mark_failed(entry.spoke_id)
            else:
                registry.mark_seen(entry.spoke_id)


@app.on_event("startup")
async def start_heartbeat() -> None:
    asyncio.create_task(_heartbeat_loop())


@app.post("/register")
async def register_spoke(registration: SpokeRegistration):
    if registration.vertical_type not in ALLOWED_VERTICALS:
        raise HTTPException(status_code=403, detail="Unauthorized vertical type")

    entry = registry.register(registration)
    return {"status": "Registered", "token": entry.execution_token}


@app.get("/nodes")
async def get_active_nodes():
    return {
        spoke_id: {
            "vertical_type": entry.vertical_type,
            "endpoint_url": entry.endpoint_url,
            "policy_version": entry.policy_version,
            "status": entry.status,
            "last_seen": entry.last_seen,
        }
        for spoke_id, entry in registry.all().items()
    }


@app.get("/health")
async def health_check():
    return {"status": "ok", "registered": len(registry.all())}


@app.get("/")
async def root():
    return {
        "service": "HeadyConductor",
        "registry_size": len(registry.all()),
        "policy": "deny-by-default",
    }
