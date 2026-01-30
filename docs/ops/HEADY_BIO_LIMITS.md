# HeadyBio Payload Limits

HeadyBio enforces a maximum payload size to avoid accidental persistence or excessive memory usage.

## Configuration
- `HEADY_BIO_MAX_BYTES` (default: 104857600 / 100MB)

## Verification
Upload a payload larger than the limit and confirm HTTP 413.
