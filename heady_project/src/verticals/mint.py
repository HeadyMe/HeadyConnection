from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict

from throttle import ComputeThrottle, TaskIntent

PHI = (1 + 5**0.5) / 2


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


@dataclass
class TokenIssuer:
    throttle: ComputeThrottle
    ledger_path: Path

    def issue(self, work_signal: float) -> Dict[str, object]:
        if work_signal <= 0:
            raise ValueError("Work signal must be positive.")
        governance = self.throttle.request_intent(
            vertical="HeadyMint",
            intent=TaskIntent.BACKGROUND_MINING,
            units=work_signal,
            metadata={"phi": PHI, "ledger": str(self.ledger_path)},
        )
        reward = work_signal * PHI
        payload = {
            "timestamp": utc_now(),
            "work_signal": work_signal,
            "reward": reward,
        }
        payload_bytes = json.dumps(payload, sort_keys=True).encode("utf-8")
        payload_hash = hashlib.sha256(payload_bytes).hexdigest()
        entry = {**payload, "hash": payload_hash}
        self.ledger_path.parent.mkdir(parents=True, exist_ok=True)
        with self.ledger_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(entry) + "\n")
        return {"entry": entry, "governance": governance.to_dict()}
