from __future__ import annotations

import hashlib
import tempfile
from dataclasses import dataclass
from typing import Dict

from throttle import ComputeThrottle, TaskIntent


@dataclass
class EphemeralProcessor:
    throttle: ComputeThrottle

    def process(self, payload: bytes) -> Dict[str, object]:
        if not payload:
            raise ValueError("Payload must be non-empty.")
        governance = self.throttle.request_intent(
            vertical="HeadyBio",
            intent=TaskIntent.EPHEMERAL_PROCESSING,
            units=max(1.0, len(payload) / 8.0),
            metadata={"bytes": len(payload), "storage": "spooled"},
        )
        digest = hashlib.sha256(payload).hexdigest()
        with tempfile.SpooledTemporaryFile(max_size=1024 * 1024) as buffer:
            buffer.write(payload)
            buffer.flush()
            buffer.seek(0)
            data = buffer.read()
            overwrite = b"\x00" * len(data)
            buffer.seek(0)
            buffer.write(overwrite)
            buffer.truncate()
        return {
            "payload_bytes": len(payload),
            "hash": digest,
            "governance": governance.to_dict(),
        }
