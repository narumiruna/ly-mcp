import json

from lymcp.api import GetStatRequest
from lymcp.tools.support import serialize_tool_error as _serialize_tool_error


async def get_stat() -> str:
    """
    取得立法院 API 的統計資訊。

    Returns:
        str: JSON 格式的統計資訊。

    Raises:
        例外時回傳中文錯誤訊息字串。
    """
    try:
        req = GetStatRequest()
        resp = await req.do()
        return json.dumps(resp, ensure_ascii=False, indent=2)
    except Exception as e:
        return _serialize_tool_error("Failed to get statistics", e)
