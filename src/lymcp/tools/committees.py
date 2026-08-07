import json
from typing import Annotated

from pydantic import Field

from lymcp.api import GetCommitteeMeetsRequest
from lymcp.api import GetCommitteeRequest
from lymcp.api import ListCommitteesRequest
from lymcp.tools.support import serialize_tool_error as _serialize_tool_error


async def list_committees(
    committee_type: Annotated[str | None, Field(description="委員會類別")] = None,
    comt_cd: Annotated[str | None, Field(description="委員會代號")] = None,
    page: Annotated[int, Field(description="頁數，預設1")] = 1,
    limit: Annotated[int, Field(description="每頁筆數，預設20，建議不超過100")] = 20,
    output_fields: Annotated[
        list[str] | None, Field(description="自訂回傳欄位（如需指定欄位，請填寫欄位名稱列表）")
    ] = None,
) -> str:
    """
    列出委員會列表。

    Args:
        committee_type: 委員會類別
        comt_cd: 委員會代號
        page: 頁數，預設1
        limit: 每頁筆數，預設20，建議不超過100
        output_fields: 自訂回傳欄位（如需指定欄位，請填寫欄位名稱列表）

    Returns:
        str: JSON 格式的委員會查詢結果。

    Raises:
        例外時回傳中文錯誤訊息字串。
    """
    try:
        req = ListCommitteesRequest(
            committee_type=committee_type,
            comt_cd=comt_cd,
            page=page,
            limit=limit,
            output_fields=output_fields or [],
        )
        resp = await req.do()
        return json.dumps(resp, ensure_ascii=False, indent=2)
    except Exception as e:
        return _serialize_tool_error("Failed to list committees", e)


async def get_committee(
    comt_cd: Annotated[str, Field(description="委員會代號，必填，例: 15")],
) -> str:
    """
    取得特定委員會資訊。

    Args:
        comt_cd: 委員會代號，必填，例：15

    Returns:
        str: JSON 格式，包含委員會基本資料、委員資訊等詳細資訊。

    Raises:
        例外時回傳中文錯誤訊息字串。
    """
    try:
        req = GetCommitteeRequest(comt_cd=comt_cd)
        resp = await req.do()
        return json.dumps(resp, ensure_ascii=False, indent=2)
    except Exception as e:
        return _serialize_tool_error("Failed to get committee", e)


async def get_committee_meets(
    comt_cd: Annotated[str, Field(description="委員會代號，必填，例: 15")],
    term: Annotated[int | None, Field(description="屆，例: 11")] = None,
    meeting_code: Annotated[str | None, Field(description="會議代碼")] = None,
    session: Annotated[int | None, Field(description="會期，例: 2")] = None,
    meeting_type: Annotated[str | None, Field(description="會議種類，例: 院會、委員會")] = None,
    member: Annotated[str | None, Field(description="會議資料.出席委員")] = None,
    date: Annotated[str | None, Field(description="日期，格式：YYYY-MM-DD")] = None,
    committee_code: Annotated[str | None, Field(description="委員會代號")] = None,
    meet_id: Annotated[str | None, Field(description="會議資料.會議編號")] = None,
    bill_no: Annotated[str | None, Field(description="議事網資料.關係文書.議案.議案編號")] = None,
    law_number: Annotated[str | None, Field(description="議事網資料.關係文書.議案.法律編號")] = None,
    page: Annotated[int, Field(description="頁數，預設1")] = 1,
    limit: Annotated[int, Field(description="每頁筆數，預設20，建議不超過100")] = 20,
    output_fields: Annotated[
        list[str] | None, Field(description="自訂回傳欄位（如需指定欄位，請填寫欄位名稱列表）")
    ] = None,
) -> str:
    """
    取得委員會相關會議列表。

    Args:
        comt_cd: 委員會代號，必填，例：15
        term: 屆期篩選，例：11
        meeting_code: 會議代碼
        session: 會期篩選，例：2
        meeting_type: 會議種類篩選，例：院會、委員會
        member: 會議資料.出席委員
        date: 日期，格式：YYYY-MM-DD
        committee_code: 委員會代號
        meet_id: 會議資料.會議編號
        bill_no: 議事網資料.關係文書.議案.議案編號
        law_number: 議事網資料.關係文書.議案.法律編號
        page: 頁數，預設1
        limit: 每頁筆數，預設20，建議不超過100
        output_fields: 自訂回傳欄位（如需指定欄位，請填寫欄位名稱列表）

    Returns:
        str: JSON 格式，包含該委員會的相關會議資訊（會議編號、會議日期、出席委員等）。

    Raises:
        例外時回傳中文錯誤訊息字串。
    """
    try:
        req = GetCommitteeMeetsRequest(
            comt_cd=comt_cd,
            term=term,
            meeting_code=meeting_code,
            session=session,
            meeting_type=meeting_type,
            member=member,
            date=date,
            committee_code=committee_code,
            meet_id=meet_id,
            bill_no=bill_no,
            law_number=law_number,
            page=page,
            limit=limit,
            output_fields=output_fields or [],
        )
        resp = await req.do()
        return json.dumps(resp, ensure_ascii=False, indent=2)
    except Exception as e:
        return _serialize_tool_error("Failed to get committee meets", e)
