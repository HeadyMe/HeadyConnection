from __future__ import annotations

import hashlib
import io
import tempfile
from dataclasses import dataclass
from typing import BinaryIO


@dataclass(frozen=True)
class ProcessResult:
    byte_count: int
    sha256: str


def _stream_to_tempfile(source: BinaryIO, max_bytes: int | None = None) -> BinaryIO:
    temp = tempfile.TemporaryFile()
    total = 0
    while chunk := source.read(1024 * 1024):
        total += len(chunk)
        if max_bytes is not None and total > max_bytes:
            temp.close()
            raise ValueError("Payload exceeds maximum size")
        temp.write(chunk)
    temp.seek(0)
    return temp


def process_genomic_stream(source: BinaryIO, max_bytes: int | None = None) -> ProcessResult:
    temp_stream = _stream_to_tempfile(source, max_bytes=max_bytes)
    digest = hashlib.sha256()
    total = 0
    while chunk := temp_stream.read(1024 * 1024):
        digest.update(chunk)
        total += len(chunk)
    temp_stream.close()
    return ProcessResult(byte_count=total, sha256=digest.hexdigest())


def process_in_memory(payload: bytes) -> ProcessResult:
    buffer = io.BytesIO(payload)
    digest = hashlib.sha256(payload).hexdigest()
    return ProcessResult(byte_count=buffer.getbuffer().nbytes, sha256=digest)
