"""CLI entrypoint."""

from __future__ import annotations

import sys

from .audio import ensure_ffmpeg
from .config import parse_args
from .providers import local_whisper, openai_api
from .translation import maybe_translate
from .writers import write_outputs


def main(argv: list[str] | None = None) -> int:
    config = parse_args(argv)
    missing = [path for path in config.audio_files if not path.is_file()]
    if missing:
        for path in missing:
            print(f"File not found: {path}", file=sys.stderr)
        return 2

    ensure_ffmpeg()

    provider_results = (
        openai_api.transcribe_files(config) if config.api_key else local_whisper.transcribe_files(config)
    )

    for result in provider_results:
        output_name = result.source_path.stem
        written_files = write_outputs(result.to_writer_payload(), config.output_dir, output_name, config.output_formats)
        if config.verbose:
            for file_path in written_files:
                print(file_path)

    translated_results = maybe_translate(provider_results, config)
    for result in translated_results:
        output_name = f"{result.source_path.stem}_{result.language}"
        written_files = write_outputs(result.to_writer_payload(), config.output_dir, output_name, config.output_formats)
        if config.verbose:
            for file_path in written_files:
                print(file_path)

    return 0
