from __future__ import annotations

import json
import os
import uuid
from dataclasses import dataclass
from typing import Optional
from urllib import request
from urllib.error import URLError


@dataclass(frozen=True)
class ServiceConfig:
    hub_url: str = os.getenv("HUB_URL", "http://heady-conductor:8000")
    node_id: str = os.getenv("NODE_ID", str(uuid.uuid4()))
    vertical_type: str = os.getenv("VERTICAL_TYPE", "Bio")
    endpoint_url: str = os.getenv("ENDPOINT_URL", "http://heady-bio:8000")
    policy_version: str = os.getenv("POLICY_VERSION", "2025-01-01")
    register_timeout_s: float = float(os.getenv("REGISTER_TIMEOUT_S", "2.5"))


def register_with_hub(config: ServiceConfig) -> Optional[str]:
    payload = {
        "spoke_id": config.node_id,
        "vertical_type": config.vertical_type,
        "endpoint_url": config.endpoint_url,
        "policy_version": config.policy_version,
    }
    body = json.dumps(payload).encode("utf-8")
    req = request.Request(
        f"{config.hub_url.rstrip('/')}/register",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=config.register_timeout_s) as response:
            data = json.loads(response.read().decode("utf-8"))
            return data.get("token")
    except URLError:
        return None
