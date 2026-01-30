from __future__ import annotations

import os

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import HTMLResponse

from config import ServiceConfig, register_with_hub
from processor import process_genomic_stream, process_in_memory

app = FastAPI(title="HeadyBio")
max_bytes = int(os.getenv("HEADY_BIO_MAX_BYTES", "104857600"))


@app.on_event("startup")
async def register_node() -> None:
    config = ServiceConfig()
    token = register_with_hub(config)
    app.state.execution_token = token


@app.post("/ingest")
async def ingest_genomic_file(file: UploadFile = File(...)):
    try:
        result = process_genomic_stream(file.file, max_bytes=max_bytes)
    except ValueError:
        raise HTTPException(status_code=413, detail="Payload exceeds maximum size")
    return {
        "bytes_processed": result.byte_count,
        "sha256": result.sha256,
        "storage": "memory-only",
    }


@app.post("/ingest-inline")
async def ingest_inline(payload: bytes):
    result = process_in_memory(payload)
    return {
        "bytes_processed": result.byte_count,
        "sha256": result.sha256,
        "storage": "memory-only",
    }


@app.get("/health")
async def health_check():
    return {"status": "ok", "policy": "process-and-destroy"}


@app.get("/")
async def root():
    html = """
    <html>
      <head><title>HeadyBio</title></head>
      <body>
        <h1>HeadyBio</h1>
        <p>Genomic processing with process-and-destroy handling.</p>
      </body>
    </html>
    """
    return HTMLResponse(content=html)
