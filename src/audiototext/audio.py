"""Audio preparation helpers."""

from __future__ import annotations

import math
import subprocess
from pathlib import Path

from .constants import OPENAI_MAX_BYTES, OPENAI_SUPPORTED_FORMATS


def ensure_ffmpeg() -> None:
    try:
        subprocess.run(
            ["ffmpeg", "-version"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        raise RuntimeError("ffmpeg is required and must be available on PATH.") from exc


def convert_for_openai(input_path: Path, workspace: Path) -> tuple[Path, bool]:
    ext = input_path.suffix.lower().lstrip(".")
    if ext in OPENAI_SUPPORTED_FORMATS:
        return input_path, False

    output_path = workspace / f"{input_path.stem}.mp3"
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(input_path), str(output_path)],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return output_path, True


def split_audio_for_openai(audio_path: Path) -> list[Path]:
    if audio_path.stat().st_size < OPENAI_MAX_BYTES:
        return [audio_path]

    try:
        from pydub import AudioSegment
        from pydub.silence import split_on_silence
    except ImportError as exc:
        raise RuntimeError(
            "Large-file API transcription requires pydub. Install audiototext with the openai extra."
        ) from exc

    audio_format = audio_path.suffix.lower().lstrip(".")
    audio_segment = AudioSegment.from_file(audio_path, audio_format)
    min_chunks = math.ceil(audio_path.stat().st_size / (OPENAI_MAX_BYTES / 2))
    max_chunk_ms = max(1, int(len(audio_segment) // min_chunks))

    output_paths: list[Path] = []

    def export_chunk(chunk: AudioSegment) -> None:
        chunk_path = audio_path.with_name(f"{audio_path.stem}_{len(output_paths) + 1}{audio_path.suffix}")
        chunk.export(chunk_path, format=audio_format)
        output_paths.append(chunk_path)

    def raw_split(chunk: AudioSegment) -> None:
        piece_count = math.ceil(len(chunk) / max_chunk_ms)
        for idx in range(piece_count):
            start = max_chunk_ms * idx
            end = min(max_chunk_ms * (idx + 1), len(chunk))
            export_chunk(chunk[start:end])

    non_silent_chunks = split_on_silence(
        audio_segment,
        seek_step=5,
        min_silence_len=1250,
        silence_thresh=-25,
        keep_silence=True,
    )

    current_chunk = non_silent_chunks[0] if non_silent_chunks else audio_segment
    for next_chunk in non_silent_chunks[1:]:
        if len(current_chunk) > max_chunk_ms:
            raw_split(current_chunk)
            current_chunk = next_chunk
        elif len(current_chunk) + len(next_chunk) <= max_chunk_ms:
            current_chunk += next_chunk
        else:
            export_chunk(current_chunk)
            current_chunk = next_chunk

    if len(current_chunk) > max_chunk_ms:
        raw_split(current_chunk)
    else:
        export_chunk(current_chunk)

    return output_paths
