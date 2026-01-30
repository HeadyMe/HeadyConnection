from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class VoiceCloneConfig:
    model_name: str

    @classmethod
    def from_env(cls) -> "VoiceCloneConfig":
        model_name = os.getenv("HEADY_SYMPHONY_TTS_MODEL", "tts_models/multilingual/multi-dataset/xtts_v2")
        return cls(model_name=model_name)
