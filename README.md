# audiototext

`audiototext` is a self-hosted CLI for turning audio into plain text, captions, and translated transcripts.

It supports local Whisper models, the OpenAI speech API, batch processing, and subtitle export in `txt`, `srt`, `vtt`, `tsv`, and `json`. If you want a hosted browser workflow instead of local setup, see [mp3totext.ai](https://mp3totext.ai/).

## Why this project

- Transcribe MP3, WAV, M4A, MP4, and other ffmpeg-readable formats.
- Choose between local inference and the OpenAI API.
- Export readable transcripts or subtitle files for players and editors.
- Translate finished transcripts with DeepL when needed.
- Process one file or many files with the same command.

## Quick start

Requirements:

- Python `3.11+`
- `ffmpeg` on your `PATH`

Install:

```bash
pip install -e .
```

Optional extras:

```bash
pip install -e .[openai,test]
```

Run a local transcription:

```bash
audiototext recordings/interview.mp3 --model small --output-formats txt,srt
```

Run with the OpenAI speech API:

```bash
audiototext recordings/interview.mp3 --api-key $OPENAI_API_KEY --output-formats txt,vtt
```

Translate the result with DeepL:

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
- `--api-key ...` to use the OpenAI speech API
- `--output-formats txt,vtt,srt,tsv,json`
- `--output-dir audio_transcription`
- `--deepl-api-key ...`
- `--deepl-target-language Spanish`

## Project layout

- `src/audiototext` contains the package code.
- `tests/test_config.py` covers argument parsing.
- `.github/workflows/ci.yml` runs the basic CI job.

## Related tools

`audiototext` focuses on the self-hosted CLI workflow. If you want a browser-based option for direct audio transcription, see [mp3totext.ai](https://mp3totext.ai/). If your workflow is more focused on social clips, captions, and transcript-driven content repurposing, see [socialtranscript.io](https://socialtranscript.io/).

## Release flow

Use [RELEASE.md](RELEASE.md) for the first public GitHub push and tag workflow.

## Notes

- Large local Whisper models can be slow on CPU-only machines.
- Large OpenAI API files are converted and chunked automatically when needed.
- Avoid passing production API keys directly in shared shell history. Environment variables are safer.
- Keep example media files small and clearly licensed before publishing this repository.

## Publish checklist

- Set your Git remote to your own GitHub repository.
- Review the license and author metadata in `LICENSE`.
- Replace placeholder example content with files you have rights to distribute.
- Run `pytest`.
- Tag the first release after the README and package metadata match your public repo.
