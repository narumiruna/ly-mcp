import asyncio
import json
from pathlib import Path
from typing import Any

import typer

from lymcp import api

_compact_output = False
_output_path: Path | None = None


def configure_output(*, compact: bool, output_path: Path | None) -> None:
    global _compact_output, _output_path
    _compact_output = compact
    _output_path = output_path


def _fields(value: str | None) -> list[str]:
    if not value:
        return []
    return [field.strip() for field in value.split(",") if field.strip()]


def _json_text(payload: dict[str, Any]) -> str:
    if _compact_output:
        return json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    return json.dumps(payload, ensure_ascii=False, indent=2)


def _emit(payload: dict[str, Any], *, err: bool = False) -> None:
    text = _json_text(payload)
    if _output_path is not None and not err:
        _output_path.write_text(f"{text}\n", encoding="utf-8")
        return
    typer.echo(text, err=err)


def _error_payload(action: str, error: Exception) -> dict[str, Any]:
    if isinstance(error, api.LymcpApiError):
        return {"ok": False, "error": error.to_dict()}
    return {
        "ok": False,
        "error": {
            "type": "unexpected_error",
            "message": f"{action}: {error}",
        },
    }


def _run(request: Any, action: str) -> None:
    try:
        _emit(asyncio.run(request.do()))
    except Exception as e:
        _emit(_error_payload(action, e), err=True)
        raise typer.Exit(1) from e
