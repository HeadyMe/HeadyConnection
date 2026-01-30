from __future__ import annotations

import argparse
from pathlib import Path

from voice_clone import TempArtifactStore, VoiceCloneRequest, clone_voice
from voice_clone_config import VoiceCloneConfig


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="HeadySymphony zero-shot voice cloning helper.")
    parser.add_argument("--reference", required=True, help="Path to reference voice sample (wav).")
    parser.add_argument("--text", required=True, help="Text to synthesize with reference voice.")
    parser.add_argument("--output", help="Output file path for the cloned voice (wav).")
    parser.add_argument("--model", help="Optional Coqui TTS model name.")
    parser.add_argument("--require-model", action="store_true", help="Fail if Coqui TTS is not available.")
    parser.add_argument(
        "--keep-temp",
        action="store_true",
        help="Keep temporary output when --output is not provided.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config = VoiceCloneConfig.from_env()
    request = VoiceCloneRequest(
        reference_path=Path(args.reference),
        text=args.text,
        output_path=Path(args.output) if args.output else None,
        model_name=args.model or config.model_name,
        require_model=args.require_model,
    )

    if request.output_path is not None:
        result = clone_voice(request)
        print(f"Voice clone written to {result.output_path} (backend={result.backend})")
        return 0

    with TempArtifactStore() as store:
        result = clone_voice(request, artifact_store=store)
        print(f"Temporary voice clone generated at {result.output_path} (backend={result.backend})")
        if args.keep_temp:
            persisted = Path.cwd() / result.output_path.name
            persisted.write_bytes(result.output_path.read_bytes())
            print(f"Persisted copy at {persisted}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
