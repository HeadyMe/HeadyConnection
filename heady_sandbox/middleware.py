from __future__ import annotations

import json
import re
from typing import Any, Dict

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


_PII_PATTERNS = {
    "ssn": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "dob": re.compile(r"\b\d{2}/\d{2}/\d{4}\b"),
    "name": re.compile(r"\b[A-Z][a-z]+\s[A-Z][a-z]+\b"),
}


def _mask_value(value: str) -> str:
    return "[REDACTED]"


def _scrub_pii(data: Any) -> Any:
    if isinstance(data, dict):
        return {key: _scrub_pii(value) for key, value in data.items()}
    if isinstance(data, list):
        return [_scrub_pii(item) for item in data]
    if isinstance(data, str):
        masked = data
        for pattern in _PII_PATTERNS.values():
            masked = pattern.sub(_mask_value(masked), masked)
        return masked
    return data


class PIIScrubMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        body = await request.body()
        request._body = body
        sanitized_payload: Dict[str, Any] = {}
        if request.headers.get("content-type", "").startswith("application/json") and body:
            try:
                parsed = json.loads(body)
                sanitized_payload = _scrub_pii(parsed)
            except json.JSONDecodeError:
                sanitized_payload = {"error": "invalid-json"}
        request.state.sanitized_payload = sanitized_payload
        return await call_next(request)
