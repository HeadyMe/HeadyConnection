from __future__ import annotations

import hashlib
import importlib.util
import math
import wave
from dataclasses import dataclass
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Optional


@dataclass(frozen=True)
class VoiceCloneRequest:
    reference_path: Path
    text: str
    output_path: Optional[Path] = None
    model_name: Optional[str] = None
    require_model: bool = False


@dataclass(frozen=True)
class VoiceCloneResult:
    output_path: Path
    backend: str
    reference_hash: str


class TempArtifactStore:
    def __init__(self) -> None:
        self._temp_dir: Optional[TemporaryDirectory[str]] = None

    def __enter__(self) -> "TempArtifactStore":
        self._temp_dir = TemporaryDirectory()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        if self._temp_dir is not None:
            self._temp_dir.cleanup()
            self._temp_dir = None

    def create_path(self, filename: str) -> Path:
        if self._temp_dir is None:
            raise RuntimeError("TempArtifactStore must be used as a context manager.")
        return Path(self._temp_dir.name) / filename


def _hash_reference(reference_path: Path) -> str:
    payload = reference_path.read_bytes()
    return hashlib.sha256(payload).hexdigest()


def _coqui_available() -> bool:
    return importlib.util.find_spec("TTS") is not None


def _clone_with_coqui(request: VoiceCloneRequest, output_path: Path) -> VoiceCloneResult:
    from TTS.api import TTS

    model_name = request.model_name or "tts_models/multilingual/multi-dataset/xtts_v2"
    tts = TTS(model_name=model_name, progress_bar=False, gpu=False)
    tts.tts_to_file(
        text=request.text,
        speaker_wav=str(request.reference_path),
        file_path=str(output_path),
    )
    return VoiceCloneResult(
        output_path=output_path,
        backend="coqui-xtts",
        reference_hash=_hash_reference(request.reference_path),
    )


def _clone_with_synthetic(request: VoiceCloneRequest, output_path: Path) -> VoiceCloneResult:
    reference_hash = _hash_reference(request.reference_path)
    seed = int(reference_hash[:8], 16)
    base_freq = 180 + (seed % 140)
    sample_rate = 22050
    duration_sec = min(5.0, max(1.0, len(request.text) / 20.0))
    total_frames = int(sample_rate * duration_sec)
    amplitude = 0.3

    with wave.open(str(output_path), "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        frames = bytearray()
        for idx in range(total_frames):
            value = int(amplitude * 32767 * math.sin(2 * math.pi * base_freq * idx / sample_rate))
            frames.extend(value.to_bytes(2, "little", signed=True))
        wav_file.writeframes(frames)

    return VoiceCloneResult(
        output_path=output_path,
        backend="synthetic-reference",
        reference_hash=reference_hash,
    )


def clone_voice(request: VoiceCloneRequest, *, artifact_store: Optional[TempArtifactStore] = None) -> VoiceCloneResult:
    if not request.reference_path.exists():
        raise FileNotFoundError(f"Reference sample not found: {request.reference_path}")
    if not request.text.strip():
        raise ValueError("Text prompt must be non-empty.")

    output_path = request.output_path
    if output_path is None:
        if artifact_store is None:
            raise RuntimeError("artifact_store is required when output_path is not provided.")
        output_path = artifact_store.create_path("voice_clone.wav")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    if _coqui_available():
        return _clone_with_coqui(request, output_path)
    if request.require_model:
        raise RuntimeError("Coqui TTS is not installed; set require_model=False for synthetic fallback.")
    return _clone_with_synthetic(request, output_path)
