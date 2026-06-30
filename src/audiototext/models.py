"""Data structures for transcription results."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class Segment:
    id: int
    start: float
    end: float
    text: str

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "Segment":
        return cls(
            id=int(payload.get("id", 0)),
            start=float(payload["start"]),
            end=float(payload["end"]),
            text=str(payload.get("text", "")).strip(),
        )


@dataclass
class TranscriptResult:
    source_path: Path
    language: str
    text: str
    segments: list[Segment]

    @classmethod
    def from_payload(cls, source_path: Path, payload: dict[str, Any]) -> "TranscriptResult":
        segments = [Segment.from_dict(segment) for segment in payload.get("segments", [])]
        text = "\n".join(segment.text for segment in segments) if segments else str(payload.get("text", "")).strip()
        language = str(payload.get("language", "unknown"))
        return cls(source_path=source_path, language=language, text=text, segments=segments)

    def to_writer_payload(self) -> dict[str, Any]:
        return {
            "language": self.language,
            "text": self.text,
            "segments": [
                {
                    "id": segment.id,
                    "start": segment.start,
                    "end": segment.end,
                    "text": segment.text,
                }
                for segment in self.segments
            ],
        }
