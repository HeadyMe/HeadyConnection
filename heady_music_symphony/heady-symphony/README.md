# heady-symphony

HeadySymphony core generation pipeline and API scaffolding.

## Voice Clone Prototype
This scaffold now includes a zero-shot voice cloning helper that can integrate with Coqui TTS
when the model is available. It also provides a deterministic synthetic fallback for environments
without the model.

### Quickstart
```
python3 app/voice_clone_cli.py \
  --reference /path/to/reference.wav \
  --text "Melancholy rain over the horizon."
```

### Configuration
Copy `.env.example` and set `HEADY_SYMPHONY_TTS_MODEL` for a custom model selection.

### Data Isolation
Reference samples remain local to the runtime; only non-sensitive metadata is emitted for logging.

## Next Steps
- Add runtime services and API contracts.
- Define storage and processing boundaries.
- Document compliance and data isolation.
