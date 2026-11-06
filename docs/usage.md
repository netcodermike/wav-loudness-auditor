# Using WAV Loudness Auditor

## Quick start

Generate synthetic audio with `python examples/make_fixture.py`, then run `python app.py examples/demo.wav`. Supply your own PCM16 WAV path to measure it without modifying it.

## Supported workflow

1. Per-channel peak, RMS, crest factor and DC offset.
2. Clipped-sample counts and format validation.
3. Machine-readable JSON output.

## Validation and troubleshooting

Run the commands in the README. Invalid inputs produce explicit errors rather than silently changing the requested operation. Browser audio requires a user gesture; microphone apps require HTTPS or localhost and permission. For file tools, supply supported input formats and writable output directories.

## Limitations

PCM16 uncompressed WAV only; RMS is not integrated LUFS and sample peaks are not intersample true peaks.

Tests use synthetic fixtures. These tests do not certify hardware compatibility, real-world forecast quality, trained-model accuracy, or production suitability for every input.
