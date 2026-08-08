# audiototext

`audiototext` is an open-source Python command-line tool for converting audio into plain text, subtitles, and translated transcripts.

It supports local Whisper models, the OpenAI speech API, batch processing, and transcript export in `txt`, `srt`, `vtt`, `tsv`, and `json`.

## Features

- Transcribe MP3, WAV, M4A, MP4, and other ffmpeg-compatible formats
- Choose between local inference and cloud API transcription
- Export transcripts as plain text or subtitle files
- Process one file or multiple files in a single command
- Optionally translate transcripts with DeepL

## Requirements

- Python `3.11+`
- `ffmpeg` available on your `PATH`

This project works on Windows, macOS, and Linux where Python and ffmpeg are installed.

## Installation

Install from source:

```bash
pip install -e .
```

Install with optional extras:

```bash
pip install -e .[openai,test]
```

## Quick start

Transcribe a local audio file:

```bash
audiototext recordings/interview.mp3 --model small --output-formats txt,srt
```

Use the OpenAI speech API:

```bash
audiototext recordings/interview.mp3 --api-key $OPENAI_API_KEY --output-formats txt,vtt
```

Translate the transcript with DeepL:

```bash
audiototext recordings/interview.mp3 \
  --output-formats txt,srt \
  --deepl-api-key $DEEPL_API_KEY \
  --deepl-target-language Spanish
```

## Usage

```bash
audiototext FILE [FILE ...] [options]
```

Common options:

- `--task transcribe|translate`
- `--model tiny|base|small|medium|large-v2|turbo`
- `--language Auto-Detect|English|French|...`
- `--api-key ...`
- `--output-formats txt,vtt,srt,tsv,json`
- `--output-dir audio_transcription`
- `--deepl-api-key ...`
- `--deepl-target-language Spanish`

## Output formats

`audiototext` can generate:

- `txt` for readable transcripts
- `srt` for subtitle workflows
- `vtt` for web and media subtitle support
- `tsv` for timestamped tabular output
- `json` for structured downstream processing

## Project structure

- `src/audiototext` contains the application code
- `tests/` contains automated tests
- `.github/workflows/` contains CI configuration

## Notes

- Large local Whisper models may be slow on CPU-only systems
- Large API files are automatically converted and chunked when needed
- API keys are better provided through environment variables than shell history
- Example media files should be clearly licensed before redistribution

## License

This project is released under the MIT License. See `LICENSE` for details.

## Source code and releases

Use this project page for source distribution and release files.

If you are looking for packaged Python distribution files, check the published release artifacts or the related Python package distribution maintained for this project.

## Related resources

If you prefer an online audio and video transcription workflow instead of a self-hosted CLI, see [transvio.ai](https://transvio.ai/).

If you prefer a browser-based MP3-to-text workflow, see [mp3totext.io](https://mp3totext.io/).
