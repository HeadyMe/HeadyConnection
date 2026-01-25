#!/usr/bin/env python3
import sys
import os
import time
import json
import datetime
from fastapi import FastAPI, Request
from pydantic import BaseModel

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Mocks or Imports
try:
    from compute_throttle import HeadyComputeThrottle, UserRequest, TaskIntent
    from ip_registry import IPRegistry
except ImportError:
    pass

app = FastAPI()

def log_event(event_type, details):
    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "component": "api_server",
        "event": event_type,
        "details": details
    }
    print(json.dumps(entry), flush=True)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    process_time = time.time() - start
    log_event("http_request", {
        "method": request.method,
        "path": request.url.path,
        "status": response.status_code,
        "duration": round(process_time, 4)
    })
    return response

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/telemetry")
def telemetry():
    throttle = HeadyComputeThrottle()
    req = UserRequest("monitor", TaskIntent.STANDARD_WEB)
    alloc = throttle.calculate_allocation(req)
    log_event("telemetry_read", alloc)
    return alloc

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="error")
