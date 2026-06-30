"""Local Whisper provider."""

from __future__ import annotations

import os

import torch
import whisper

from ..config import CliConfig
from ..constants import ENGLISH_ONLY_BASE_MODELS
from ..models import TranscriptResult


def transcribe_files(config: CliConfig) -> list[TranscriptResult]:
    device = "cuda" if torch.cuda.is_available() else "cpu"
    language = None if config.language == "Auto-Detect" else config.language
    model_name = config.model

    if language == "English" and model_name in ENGLISH_ONLY_BASE_MODELS:
        model_name = f"{model_name}.en"

    model = whisper.load_model(model_name, device=device)
    if device == "cpu":
        torch.set_num_threads(max(1, os.cpu_count() or 1))

    results: list[TranscriptResult] = []
    options = {
        "task": config.task,
        "verbose": config.verbose,
        "fp16": device == "cuda",
        "best_of": 5,
        "beam_size": 5,
        "patience": None,
        "length_penalty": None,
        "suppress_tokens": "-1",
        "temperature": (0.0, 0.2, 0.4, 0.6, 0.8, 1.0),
        "condition_on_previous_text": config.coherence_preference,
        "initial_prompt": config.prompt,
        "word_timestamps": False,
    }

    for audio_path in config.audio_files:
        if language:
            options["language"] = language
        else:
            audio = whisper.load_audio(str(audio_path))
            audio = whisper.pad_or_trim(audio)
            mel = whisper.log_mel_spectrogram(audio).to(model.device)
            _, probabilities = model.detect_language(mel)
            detected_code = max(probabilities, key=probabilities.get)
            options["language"] = whisper.tokenizer.LANGUAGES[detected_code].title()

        payload = whisper.transcribe(model, str(audio_path), **options)
        results.append(TranscriptResult.from_payload(audio_path, payload))
    return results
