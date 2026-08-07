import json
from typing import Annotated

from pydantic import Field

from lymcp.api import GetGazetteAgendaRequest
from lymcp.api import GetGazetteAgendasRequest
from lymcp.api import GetGazetteRequest
from lymcp.api import ListGazetteAgendasRequest
from lymcp.api import ListGazettesRequest
from lymcp.tools.support import serialize_tool_error as _serialize_tool_error


async def list_gazettes(
    gazette_id: Annotated[str | None, Field(description="公報編號，例：1137701")] = None,
    volume: Annotated[int | None, Field(description="卷，例：113")] = None,
    page: Annotated[int, Field(description="頁數，預設1")] = 1,
    limit: Annotated[int, Field(description="每頁筆數，預設20，建議不超過100")] = 20,
    output_fields: Annotated[
        list[str] | None, Field(description="自訂回傳欄位（如需指定欄位，請填寫欄位名稱列表）")
    ] = None,
) -> str:
    """
    列出立法院公報列表。

    Args:
        gazette_id: 公報編號，例：1137701
        volume: 卷，例：113
        page: 頁數，預設1
        limit: 每頁筆數，預設20，建議不超過100
        output_fields: 自訂回傳欄位（如需指定欄位，請填寫欄位名稱列表）

    Returns:
        str: JSON 格式的公報查詢結果。

    Raises:
        例外時回傳中文錯誤訊息字串。
    """
    try:
        req = ListGazettesRequest(
            gazette_id=gazette_id,
            volume=volume,
            page=page,
            limit=limit,
            output_fields=output_fields or [],
        )
        resp = await req.do()
        return json.dumps(resp, ensure_ascii=False, indent=2)
    except Exception as e:
        return _serialize_tool_error("Failed to list gazettes", e)


async def get_gazette(
    gazette_id: Annotated[str, Field(description="公報編號，必填，例：1137701")],
) -> str:
    """
    取得特定公報的詳細資訊。

    Args:
        gazette_id: 公報編號，必填，例：1137701

    Returns:
        str: JSON 格式，包含公報詳細資訊。

    Raises:
        例外時回傳中文錯誤訊息字串。
    """
    try:
        req = GetGazetteRequest(gazette_id=gazette_id)
        resp = await req.do()
        return json.dumps(resp, ensure_ascii=False, indent=2)
    except Exception as e:
        return _serialize_tool_error("Failed to get gazette detail", e)


async def get_gazette_agendas(
    gazette_id: Annotated[str, Field(description="路徑中的公報編號，必填，例：1137701")],
    gazette_number: Annotated[str | None, Field(description="查詢條件中的公報編號，例：1137701")] = None,
    volume: Annotated[int | None, Field(description="卷，例：113")] = None,
    issue: Annotated[int | None, Field(description="期，例：77")] = None,
    booklet: Annotated[int | None, Field(description="冊別，例：1")] = None,
    term: Annotated[int | None, Field(description="屆，例：11")] = None,
    meeting_date: Annotated[str | None, Field(description="會議日期，格式：YYYY-MM-DD，例：2024-10-04")] = None,
    page: Annotated[int, Field(description="頁數，預設1")] = 1,
    limit: Annotated[int, Field(description="每頁筆數，預設20，建議不超過100")] = 20,
    output_fields: Annotated[
        list[str] | None, Field(description="自訂回傳欄位（如需指定欄位，請填寫欄位名稱列表）")
    ] = None,
) -> str:
    """
    取得特定公報所含的公報目錄列表。

    Args:
        gazette_id: 路徑中的公報編號，必填，例：1137701
        gazette_number: 查詢條件中的公報編號，例：1137701
        volume: 卷，例：113
        issue: 期，例：77
        booklet: 冊別，例：1
        term: 屆，例：11
        meeting_date: 會議日期，格式：YYYY-MM-DD，例：2024-10-04
        page: 頁數，預設1
        limit: 每頁筆數，預設20，建議不超過100
        output_fields: 自訂回傳欄位（如需指定欄位，請填寫欄位名稱列表）

    Returns:
        str: JSON 格式，包含該公報的公報目錄資訊。

    Raises:
        例外時回傳中文錯誤訊息字串。
    """
    try:
        req = GetGazetteAgendasRequest(
            gazette_id=gazette_id,
            gazette_number=gazette_number,
            volume=volume,
            issue=issue,
            booklet=booklet,
            term=term,
            meeting_date=meeting_date,
            page=page,
            limit=limit,
            output_fields=output_fields or [],
        )
        resp = await req.do()
        return json.dumps(resp, ensure_ascii=False, indent=2)
    except Exception as e:
        return _serialize_tool_error("Failed to get gazette agendas", e)


async def list_gazette_agendas(
    gazette_id: Annotated[str | None, Field(description="公報編號，例：1137701")] = None,
    volume: Annotated[int | None, Field(description="卷，例：113")] = None,
    issue: Annotated[int | None, Field(description="期，例：77")] = None,
    booklet: Annotated[int | None, Field(description="冊別，例：1")] = None,
    term: Annotated[int | None, Field(description="屆，例：11")] = None,
    meeting_date: Annotated[str | None, Field(description="會議日期，格式：YYYY-MM-DD，例：2024-10-04")] = None,
    page: Annotated[int, Field(description="頁數，預設1")] = 1,
    limit: Annotated[int, Field(description="每頁筆數，預設20，建議不超過100")] = 20,
    output_fields: Annotated[
        list[str] | None, Field(description="自訂回傳欄位（如需指定欄位，請填寫欄位名稱列表）")
    ] = None,
) -> str:
    """
    列出公報目錄列表。

    Args:
        gazette_id: 公報編號，例：1137701
        volume: 卷，例：113
        issue: 期，例：77
        booklet: 冊別，例：1
        term: 屆，例：11
        meeting_date: 會議日期，格式：YYYY-MM-DD，例：2024-10-04
        page: 頁數，預設1
        limit: 每頁筆數，預設20，建議不超過100
        output_fields: 自訂回傳欄位（如需指定欄位，請填寫欄位名稱列表）

    Returns:
        str: JSON 格式的公報目錄查詢結果。

    Raises:
        例外時回傳中文錯誤訊息字串。
    """
    try:
        req = ListGazetteAgendasRequest(
            gazette_id=gazette_id,
            volume=volume,
            issue=issue,
            booklet=booklet,
            term=term,
            meeting_date=meeting_date,
            page=page,
            limit=limit,
            output_fields=output_fields or [],
        )
        resp = await req.do()
        return json.dumps(resp, ensure_ascii=False, indent=2)
    except Exception as e:
        return _serialize_tool_error("Failed to list gazette agendas", e)


async def get_gazette_agenda(
    gazette_agenda_id: Annotated[str, Field(description="公報議程編號，必填，例：1137701_00001")],
) -> str:
    """
    取得特定公報目錄的詳細資訊。

    Args:
        gazette_agenda_id: 公報議程編號，必填，例：1137701_00001

    Returns:
        str: JSON 格式，包含公報目錄詳細資訊。

    Raises:
        例外時回傳中文錯誤訊息字串。
    """
    try:
        req = GetGazetteAgendaRequest(gazette_agenda_id=gazette_agenda_id)
        resp = await req.do()
        return json.dumps(resp, ensure_ascii=False, indent=2)
    except Exception as e:
        return _serialize_tool_error("Failed to get gazette agenda detail", e)
