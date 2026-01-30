# Operations Runbook

Local-first scaffolding only. Extend with service orchestration when ready.

## Voice Clone Helper
The voice cloning helper accepts a local reference voice sample and text prompt. When the
Coqui TTS dependency is present, it performs zero-shot cloning; otherwise it produces a
deterministic synthetic output tied to the reference hash.

### Run
```
python3 app/voice_clone_cli.py \
  --reference /path/to/reference.wav \
  --text "Signal check complete."
```

### Resource Cleanup
When `--output` is not provided, the helper writes to a temporary file and cleans it up after
execution unless `--keep-temp` is set. This prevents orphaned `.wav` artifacts.
