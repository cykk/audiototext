"""Argument parsing and runtime configuration."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

from .constants import (
    DEEPL_TARGET_LANGUAGES,
    DEFAULT_OUTPUT_FORMATS,
    SUPPORTED_OUTPUT_FORMATS,
    WHISPER_LANGUAGE_CHOICES,
    WHISPER_MODELS,
)


def _parse_bool(value: str) -> bool:
    return value.lower() != "false"


def _parse_output_formats(value: str) -> tuple[str, ...]:
    formats = tuple(part.strip().lower() for part in value.split(",") if part.strip())
    invalid = [item for item in formats if item not in SUPPORTED_OUTPUT_FORMATS]
    if invalid:
        raise argparse.ArgumentTypeError(
            f"Unsupported output format(s): {', '.join(invalid)}. "
            f"Supported formats: {', '.join(sorted(SUPPORTED_OUTPUT_FORMATS))}."
        )
    return formats or DEFAULT_OUTPUT_FORMATS


@dataclass
class CliConfig:
    audio_files: list[Path]
    task: str
    model: str
    language: str
    prompt: str | None
    coherence_preference: bool
    api_key: str | None
    output_formats: tuple[str, ...]
    output_dir: Path
    deepl_api_key: str | None
    deepl_target_language: str | None
    deepl_coherence_preference: bool
    deepl_formality: str
    verbose: bool


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="audiototext",
        description="Transcribe audio to text with local Whisper models or the OpenAI speech API.",
        epilog="Project site: https://mp3totext.io",
    )
    parser.add_argument("audio_files", nargs="+", help="One or more audio or video files to transcribe.")
    parser.add_argument("--task", default="transcribe", choices=("transcribe", "translate"))
    parser.add_argument("--model", default="small", choices=WHISPER_MODELS)
    parser.add_argument("--language", default="Auto-Detect", choices=WHISPER_LANGUAGE_CHOICES)
    parser.add_argument("--prompt", help="Optional prompt to bias style, spelling, or terminology.")
    parser.add_argument(
        "--coherence-preference",
        default="true",
        choices=("true", "false", "True", "False"),
        type=_parse_bool,
        help="Use previous text as context. Set false to reduce repetition in difficult audio.",
    )
    parser.add_argument(
        "--api-key",
        help="OpenAI API key. If set, audiototext uses the cloud speech API instead of local Whisper.",
    )
    parser.add_argument(
        "--output-formats",
        "--output-format",
        default=",".join(DEFAULT_OUTPUT_FORMATS),
        type=_parse_output_formats,
        help="Comma-separated output formats: txt,vtt,srt,tsv,json",
    )
    parser.add_argument("--output-dir", default="audio_transcription")
    parser.add_argument("--deepl-api-key", help="DeepL API key for optional post-translation.")
    parser.add_argument("--deepl-target-language", choices=DEEPL_TARGET_LANGUAGES)
    parser.add_argument(
        "--deepl-coherence-preference",
        default="true",
        choices=("true", "false", "True", "False"),
        type=_parse_bool,
        help="Translate batches with shared context when possible.",
    )
    parser.add_argument(
        "--deepl-formality",
        default="default",
        choices=("default", "formal", "informal"),
    )
    parser.add_argument("--quiet", action="store_true", help="Reduce console logging.")
    return parser


def parse_args(argv: list[str] | None = None) -> CliConfig:
    args = build_parser().parse_args(argv)
    audio_files = [Path(item).expanduser() for item in args.audio_files]
    return CliConfig(
        audio_files=audio_files,
        task=args.task,
        model=args.model,
        language=args.language,
        prompt=args.prompt,
        coherence_preference=args.coherence_preference,
        api_key=args.api_key,
        output_formats=args.output_formats,
        output_dir=Path(args.output_dir),
        deepl_api_key=args.deepl_api_key,
        deepl_target_language=args.deepl_target_language,
        deepl_coherence_preference=args.deepl_coherence_preference,
        deepl_formality=args.deepl_formality,
        verbose=not args.quiet,
    )
