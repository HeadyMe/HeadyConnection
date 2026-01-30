from __future__ import annotations

import math
import sys
import tempfile
import unittest
import wave
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "heady_music_symphony" / "heady-symphony" / "app"
sys.path.insert(0, str(APP))

from voice_clone import TempArtifactStore, VoiceCloneRequest, clone_voice  # noqa: E402


def _write_reference_wav(path: Path, freq: int = 220) -> None:
    sample_rate = 22050
    duration = 0.5
    frames = int(sample_rate * duration)
    with wave.open(str(path), "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        payload = bytearray()
        for idx in range(frames):
            value = int(0.2 * 32767 * math.sin(2 * math.pi * freq * idx / sample_rate))
            payload.extend(value.to_bytes(2, "little", signed=True))
        wav_file.writeframes(payload)


class VoiceCloneTests(unittest.TestCase):
    def test_clone_creates_output_and_cleans_temp(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            reference = Path(tmpdir) / "reference.wav"
            _write_reference_wav(reference)
            with TempArtifactStore() as store:
                request = VoiceCloneRequest(reference_path=reference, text="Test phrase")
                result = clone_voice(request, artifact_store=store)
                self.assertTrue(result.output_path.exists())
                output_path = result.output_path
            self.assertFalse(output_path.exists(), "Temporary output should be cleaned after context exit")

    def test_clone_with_explicit_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            reference = Path(tmpdir) / "reference.wav"
            output = Path(tmpdir) / "output.wav"
            _write_reference_wav(reference)
            request = VoiceCloneRequest(reference_path=reference, text="Another phrase", output_path=output)
            result = clone_voice(request)
            self.assertTrue(result.output_path.exists())


if __name__ == "__main__":
    unittest.main()
