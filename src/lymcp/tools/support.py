import json

from loguru import logger

from lymcp.api import LymcpApiError


def serialize_tool_error(action: str, error: Exception) -> str:
    logger.error("{}: {}", action, error)
    if isinstance(error, LymcpApiError):
        payload = {"ok": False, "error": error.to_dict()}
    else:
        payload = {
            "ok": False,
            "error": {
                "type": "unexpected_error",
                "message": f"{action}: {error}",
            },
        }
    return json.dumps(payload, ensure_ascii=False, indent=2)
