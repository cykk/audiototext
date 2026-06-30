"""OpenAI speech API provider."""

from __future__ import annotations

import tempfile
from pathlib import Path

from openai import OpenAI

from ..audio import convert_for_openai, split_audio_for_openai
from ..config import CliConfig
from ..models import TranscriptResult


def transcribe_files(config: CliConfig) -> list[TranscriptResult]:
    client = OpenAI(api_key=config.api_key)
    results: list[TranscriptResult] = []

    endpoint = client.audio.transcriptions if config.task == "transcribe" else client.audio.translations

    for audio_path in config.audio_files:
        with tempfile.TemporaryDirectory(prefix="audiototext-") as tmp_dir:
            temp_dir = Path(tmp_dir)
            converted_path, _ = convert_for_openai(audio_path, temp_dir)
            chunks = split_audio_for_openai(converted_path)

            combined_payload = None
            for chunk in chunks:
                with chunk.open("rb") as audio_handle:
                    payload = endpoint.create(
                        model="whisper-1",
                        file=audio_handle,
                        response_format="verbose_json",
                        prompt=config.prompt or None,
                        temperature=0,
                    ).model_dump()

                if combined_payload is None:
                    combined_payload = payload
                    continue

                last_end = combined_payload["segments"][-1]["end"] if combined_payload["segments"] else 0
                for segment in payload["segments"]:
                    segment["start"] += last_end
                    segment["end"] += last_end
                combined_payload["segments"].extend(payload["segments"])
                if "duration" in combined_payload and "duration" in payload:
                    combined_payload["duration"] += payload["duration"]

            if combined_payload is None:
                raise RuntimeError(f"No transcription result returned for {audio_path}")

            results.append(TranscriptResult.from_payload(audio_path, combined_payload))

    return results
