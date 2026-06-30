"""Optional DeepL translation support."""

from __future__ import annotations

from typing import Iterable

import deepl
import whisper
from whisper.utils import format_timestamp

from .config import CliConfig
from .models import Segment, TranscriptResult


def _normalize_target_language(target_language: str) -> str:
    if target_language == "English":
        return "English (British)"
    if target_language == "Chinese":
        return "Chinese (simplified)"
    if target_language == "Portuguese":
        return "Portuguese (European)"
    return target_language


def maybe_translate(results: Iterable[TranscriptResult], config: CliConfig) -> list[TranscriptResult]:
    if not config.deepl_api_key:
        return []

    target_language = _normalize_target_language(config.deepl_target_language or "English")
    translator = deepl.Translator(config.deepl_api_key)
    deepl_source_languages = {lang.code.upper() for lang in translator.get_source_languages()}
    deepl_target_languages = translator.get_target_languages()
    target_language_code = next(lang.code for lang in deepl_target_languages if lang.name == target_language).upper()
    target_family = target_language_code.split("-")[0]

    formality = "default"
    if config.deepl_formality == "formal":
        formality = "prefer_more"
    elif config.deepl_formality == "informal":
        formality = "prefer_less"

    translated_results: list[TranscriptResult] = []

    for result in results:
        source_code = whisper.tokenizer.TO_LANGUAGE_CODE.get(result.language.lower(), "").upper()
        if source_code == target_family or (source_code and source_code not in deepl_source_languages):
            continue

        translated_segments: list[Segment] = []
        batch_size = 200
        for batch_start in range(0, len(result.segments), batch_size):
            batch = result.segments[batch_start : batch_start + batch_size]
            source_text = [segment.text for segment in batch]

            if config.deepl_coherence_preference:
                response = translator.translate_text(
                    text="<br/>".join(source_text),
                    source_lang=source_code or None,
                    target_lang=target_language_code,
                    formality=formality,
                    split_sentences="nonewlines",
                    tag_handling="xml",
                    ignore_tags="br",
                    outline_detection=False,
                )
                translated_texts = response.text.split("<br/>")
            else:
                response = translator.translate_text(
                    text=source_text,
                    source_lang=source_code or None,
                    target_lang=target_language_code,
                    formality=formality,
                    split_sentences="nonewlines",
                )
                translated_texts = [item.text for item in response]

            for idx, translated_text in enumerate(translated_texts):
                source_segment = batch[idx]
                cleaned = translated_text.lstrip(",.").rstrip()
                translated_segments.append(
                    Segment(
                        id=source_segment.id,
                        start=source_segment.start,
                        end=source_segment.end,
                        text=cleaned,
                    )
                )
                if config.verbose:
                    print(
                        f"[{format_timestamp(source_segment.start)} --> "
                        f"{format_timestamp(source_segment.end)}] {cleaned}"
                    )

        translated_results.append(
            TranscriptResult(
                source_path=result.source_path,
                language=target_language,
                text="\n".join(segment.text for segment in translated_segments),
                segments=translated_segments,
            )
        )

    return translated_results
