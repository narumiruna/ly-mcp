import json
from typing import Annotated

from pydantic import Field

from lymcp.api import GetIvodRequest
from lymcp.api import GetMeetIvodsRequest
from lymcp.api import ListIvodsRequest
from lymcp.tools.support import serialize_tool_error as _serialize_tool_error


async def list_ivods(
    term: Annotated[int | None, Field(description="屆，例：11")] = None,
    session: Annotated[int | None, Field(description="會期，例：2")] = None,
    meeting_code: Annotated[str | None, Field(description="會議代碼，例：委員會-11-2-22-5")] = None,
    member_name: Annotated[str | None, Field(description="委員名稱，例：陳培瑜")] = None,
    committee_code: Annotated[int | None, Field(description="委員會代碼，例：22")] = None,
    meeting_code_data: Annotated[str | None, Field(description="會議資料.會議代碼，例：委員會-11-2-22-5")] = None,
    date: Annotated[str | None, Field(description="日期，格式：YYYY-MM-DD，例：2024-10-24")] = None,
    video_type: Annotated[str | None, Field(description="影片種類，Clip（片段）或 Full（完整）")] = None,
    page: Annotated[int, Field(description="頁數，預設1")] = 1,
    limit: Annotated[int, Field(description="每頁筆數，預設20，建議不超過100")] = 20,
    output_fields: Annotated[
        list[str] | None, Field(description="自訂回傳欄位（如需指定欄位，請填寫欄位名稱列表）")
    ] = None,
) -> str:
    """
    列出 IVOD（網路電視）影片列表。

    Args:
        term: 屆，例：11
        session: 會期，例：2
        meeting_code: 會議代碼，例：委員會-11-2-22-5
        member_name: 委員名稱，例：陳培瑜
        committee_code: 委員會代碼，例：22
        meeting_code_data: 會議資料.會議代碼，例：委員會-11-2-22-5
        date: 日期，格式：YYYY-MM-DD，例：2024-10-24
        video_type: 影片種類，Clip（片段）或 Full（完整）
        page: 頁數，預設1
        limit: 每頁筆數，預設20，建議不超過100
        output_fields: 自訂回傳欄位（如需指定欄位，請填寫欄位名稱列表）

    Returns:
        str: JSON 格式，包含 IVOD 影片列表資料。

    Raises:
        例外時回傳中文錯誤訊息字串。
    """
    try:
        req = ListIvodsRequest(
            term=term,
            session=session,
            meeting_code=meeting_code,
            member_name=member_name,
            committee_code=committee_code,
            meeting_code_data=meeting_code_data,
            date=date,
            video_type=video_type,
            page=page,
            limit=limit,
            output_fields=output_fields or [],
        )
        resp = await req.do()
        return json.dumps(resp, ensure_ascii=False, indent=2)
    except Exception as e:
        return _serialize_tool_error("Failed to list IVODs", e)


async def get_ivod(
    ivod_id: Annotated[str, Field(description="IVOD 編號，必填，例：156045")],
) -> str:
    """
    取得特定 IVOD（網路電視）影片的詳細資訊。

    Args:
        ivod_id: IVOD 編號，必填，例：156045

    Returns:
        str: JSON 格式，包含 IVOD 影片詳細資訊，包括播放頁面網址、影片網址、
             會議資料、影片長度、委員發言時間、逐字稿等。

    Raises:
        例外時回傳中文錯誤訊息字串。
    """
    try:
        req = GetIvodRequest(ivod_id=ivod_id)
        resp = await req.do()
        return json.dumps(resp, ensure_ascii=False, indent=2)
    except Exception as e:
        return _serialize_tool_error("Failed to get IVOD detail", e)


async def get_meet_ivods(
    meet_id: Annotated[str, Field(description="會議代碼，必填，例：院會-11-2-3")],
    term: Annotated[int | None, Field(description="屆，例：11")] = None,
    session: Annotated[int | None, Field(description="會期，例：2")] = None,
    meeting_code: Annotated[str | None, Field(description="會議代碼，例：委員會-11-2-22-5")] = None,
    member_name: Annotated[str | None, Field(description="委員名稱，例：陳培瑜")] = None,
    committee_code: Annotated[int | None, Field(description="委員會代碼，例：22")] = None,
    meeting_code_data: Annotated[str | None, Field(description="會議資料.會議代碼，例：委員會-11-2-22-5")] = None,
    date: Annotated[str | None, Field(description="日期，格式：YYYY-MM-DD，例：2024-10-24")] = None,
    video_type: Annotated[str | None, Field(description="影片種類，Clip（片段）或 Full（完整）")] = None,
    page: Annotated[int, Field(description="頁數，預設1")] = 1,
    limit: Annotated[int, Field(description="每頁筆數，預設20，建議不超過100")] = 20,
    output_fields: Annotated[
        list[str] | None, Field(description="自訂回傳欄位（如需指定欄位，請填寫欄位名稱列表）")
    ] = None,
) -> str:
    """
    取得特定會議相關的 IVOD（網路電視）影片列表。

    Args:
        meet_id: 會議代碼，必填，例：院會-11-2-3
        term: 屆，例：11
        session: 會期，例：2
        meeting_code: 會議代碼，例：委員會-11-2-22-5
        member_name: 委員名稱，例：陳培瑜
        committee_code: 委員會代碼，例：22
        meeting_code_data: 會議資料.會議代碼，例：委員會-11-2-22-5
        date: 日期，格式：YYYY-MM-DD，例：2024-10-24
        video_type: 影片種類，Clip（片段）或 Full（完整）
        page: 頁數，預設1
        limit: 每頁筆數，預設20，建議不超過100
        output_fields: 自訂回傳欄位（如需指定欄位，請填寫欄位名稱列表）

    Returns:
        str: JSON 格式，包含會議相關的 IVOD 影片列表資料。

    Raises:
        例外時回傳中文錯誤訊息字串。
    """
    try:
        req = GetMeetIvodsRequest(
            meet_id=meet_id,
            term=term,
            session=session,
            meeting_code=meeting_code,
            member_name=member_name,
            committee_code=committee_code,
            meeting_code_data=meeting_code_data,
            date=date,
            video_type=video_type,
            page=page,
            limit=limit,
            output_fields=output_fields or [],
        )
        resp = await req.do()
        return json.dumps(resp, ensure_ascii=False, indent=2)
    except Exception as e:
        return _serialize_tool_error("Failed to get meet IVODs", e)
