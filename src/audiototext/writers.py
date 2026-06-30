"""Output writers."""

from __future__ import annotations

from pathlib import Path
from typing import Any


def write_outputs(result_payload: dict[str, Any], output_dir: Path, output_name: str, formats: tuple[str, ...]) -> list[Path]:
    from whisper.utils import WriteTXT, get_writer

    class PlainTextWriter(WriteTXT):
        def write_result(self, result: dict[str, Any], file, **kwargs) -> None:  # type: ignore[override]
            print(result["text"], file=file, flush=True)

    output_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for output_format in formats:
        fix_vtt = output_format == "vtt" and result_payload["segments"] and result_payload["segments"][0].get("start") == 0
        if fix_vtt:
            result_payload["segments"][0]["start"] += 0.001

        writer = PlainTextWriter(str(output_dir)) if output_format == "txt" else get_writer(output_format, str(output_dir))
        writer(result_payload, output_name)
        output_path = output_dir / f"{output_name}.{output_format}"
        written.append(output_path)

        if fix_vtt:
            result_payload["segments"][0]["start"] = 0

    return written
