import json
from typing import Annotated

from pydantic import Field

from lymcp.api import GetInterpellationRequest
from lymcp.api import GetLegislatorInterpellationsRequest
from lymcp.api import ListInterpellationsRequest
from lymcp.tools.support import serialize_tool_error as _serialize_tool_error


async def list_interpellations(
    interpellation_member: Annotated[str | None, Field(description="質詢委員姓名，例：羅智強")] = None,
    term: Annotated[int | None, Field(description="屆，例：11")] = None,
    session: Annotated[int | None, Field(description="會期，例：2")] = None,
    meeting_code: Annotated[str | None, Field(description="會議代碼，例：院會-11-2-6")] = None,
    page: Annotated[int, Field(description="頁數，預設1")] = 1,
    limit: Annotated[int, Field(description="每頁筆數，預設20，建議不超過100")] = 20,
    output_fields: Annotated[
        list[str] | None, Field(description="自訂回傳欄位（如需指定欄位，請填寫欄位名稱列表）")
    ] = None,
) -> str:
    """
    列出立法院質詢列表。

    Args:
        interpellation_member: 質詢委員姓名，例：羅智強
        term: 屆期，例：11
        session: 會期，例：2
        meeting_code: 會議代碼，例：院會-11-2-6
        page: 頁數，預設1
        limit: 每頁筆數，預設20，建議不超過100
        output_fields: 自訂回傳欄位（如需指定欄位，請填寫欄位名稱列表）

    Returns:
        str: JSON 格式的質詢查詢結果。

    Raises:
        例外時回傳中文錯誤訊息字串。
    """
    try:
        req = ListInterpellationsRequest(
            interpellation_member=interpellation_member,
            term=term,
            session=session,
            meeting_code=meeting_code,
            page=page,
            limit=limit,
            output_fields=output_fields or [],
        )
        resp = await req.do()
        return json.dumps(resp, ensure_ascii=False, indent=2)
    except Exception as e:
        return _serialize_tool_error("Failed to list interpellations", e)


async def get_interpellation(
    interpellation_id: Annotated[str, Field(description="質詢編號，必填，例：11-1-1-1")],
) -> str:
    """
    取得特定質詢的詳細資訊。

    Args:
        interpellation_id: 質詢編號，必填，例：11-1-1-1

    Returns:
        str: JSON 格式，包含質詢詳細資訊。

    Raises:
        例外時回傳中文錯誤訊息字串。
    """
    try:
        req = GetInterpellationRequest(interpellation_id=interpellation_id)
        resp = await req.do()
        return json.dumps(resp, ensure_ascii=False, indent=2)
    except Exception as e:
        return _serialize_tool_error("Failed to get interpellation detail", e)


async def get_legislator_interpellations(
    term: Annotated[int, Field(description="屆，必填，例：11")],
    name: Annotated[str, Field(description="委員姓名，必填，例：韓國瑜")],
    interpellation_member: Annotated[str | None, Field(description="質詢委員姓名，例：羅智強")] = None,
    session: Annotated[int | None, Field(description="會期，例：2")] = None,
    meeting_code: Annotated[str | None, Field(description="會議代碼，例：院會-11-2-6")] = None,
    page: Annotated[int, Field(description="頁數，預設1")] = 1,
    limit: Annotated[int, Field(description="每頁筆數，預設20，建議不超過100")] = 20,
    output_fields: Annotated[
        list[str] | None, Field(description="自訂回傳欄位（如需指定欄位，請填寫欄位名稱列表）")
    ] = None,
) -> str:
    """
    取得委員為質詢委員的質詢列表。

    Args:
        term: 屆期，必填，例：11
        name: 委員姓名，必填，例：韓國瑜
        interpellation_member: 質詢委員姓名，例：羅智強
        session: 會期，例：2
        meeting_code: 會議代碼，例：院會-11-2-6
        page: 頁數，預設1
        limit: 每頁筆數，預設20，建議不超過100
        output_fields: 自訂回傳欄位（如需指定欄位，請填寫欄位名稱列表）

    Returns:
        str: JSON 格式，包含委員為質詢委員的質詢資料。

    Raises:
        例外時回傳中文錯誤訊息字串。
    """
    try:
        req = GetLegislatorInterpellationsRequest(
            term=term,
            name=name,
            interpellation_member=interpellation_member,
            term_query=term,
            session=session,
            meeting_code=meeting_code,
            page=page,
            limit=limit,
            output_fields=output_fields or [],
        )
        resp = await req.do()
        return json.dumps(resp, ensure_ascii=False, indent=2)
    except Exception as e:
        return _serialize_tool_error("Failed to get legislator interpellations", e)
