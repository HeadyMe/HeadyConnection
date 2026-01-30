from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Dict, List, Tuple

from throttle import ComputeThrottle, TaskIntent


SCALES: Dict[str, Tuple[str, ...]] = {
    "lydian": ("C", "D", "E", "F#", "G", "A", "B"),
    "dorian": ("D", "E", "F", "G", "A", "B", "C"),
    "aeolian": ("A", "B", "C", "D", "E", "F", "G"),
    "mixolydian": ("G", "A", "B", "C", "D", "E", "F"),
}


def _mood_to_mode(narrative: str) -> str:
    lowered = narrative.lower()
    if any(word in lowered for word in ("melancholy", "rain", "loss", "somber")):
        return "aeolian"
    if any(word in lowered for word in ("drift", "mystery", "travel", "wander")):
        return "dorian"
    if any(word in lowered for word in ("victory", "bright", "celebration", "rise")):
        return "lydian"
    return "mixolydian"


@dataclass
class NarrativeToMIDI:
    throttle: ComputeThrottle

    def render(self, narrative: str) -> Dict[str, object]:
        if not narrative.strip():
            raise ValueError("Narrative must be a non-empty string.")
        mode = _mood_to_mode(narrative)
        scale = SCALES[mode]
        seed = int(hashlib.sha256(narrative.encode("utf-8")).hexdigest(), 16)
        tempo = 72 + (seed % 48)
        notes: List[Dict[str, object]] = []
        for idx in range(8):
            note = scale[(seed + idx) % len(scale)]
            duration = 0.5 + ((seed >> idx) % 3) * 0.25
            notes.append({"note": note, "duration": duration, "velocity": 90 - idx * 2})
        governance = self.throttle.request_intent(
            vertical="HeadySymphony",
            intent=TaskIntent.REALTIME_AUDIO,
            units=len(narrative) * 0.5,
            metadata={"mode": mode, "tempo_bpm": tempo},
        )
        return {
            "narrative": narrative,
            "midi": {"tempo_bpm": tempo, "mode": mode, "notes": notes},
            "governance": governance.to_dict(),
        }
