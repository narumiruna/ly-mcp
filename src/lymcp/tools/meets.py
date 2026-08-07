import json
from typing import Annotated

from pydantic import Field

from lymcp.api import GetMeetBillsRequest
from lymcp.api import GetMeetInterpellationsRequest
from lymcp.api import GetMeetRequest
from lymcp.api import ListMeetsRequest
from lymcp.tools.support import serialize_tool_error as _serialize_tool_error


async def list_meets(
    term: Annotated[int | None, Field(description="屆，例：11")] = None,
    meeting_code: Annotated[str | None, Field(description="會議代碼，例：院會-11-2-6")] = None,
    session: Annotated[int | None, Field(description="會期，例：2")] = None,
    meeting_type: Annotated[str | None, Field(description="會議種類，例：院會")] = None,
    meeting_attendee: Annotated[str | None, Field(description="出席委員，例：陳秀寳")] = None,
    date: Annotated[str | None, Field(description="日期，格式：YYYY-MM-DD，例：2024-10-25")] = None,
    committee_code: Annotated[int | None, Field(description="委員會代號，例：23")] = None,
    meeting_id: Annotated[str | None, Field(description="會議編號，例：2024102368")] = None,
    meeting_bills_bill_no: Annotated[str | None, Field(description="關係文書議案編號，例：202110071090000")] = None,
    meeting_bills_law_no: Annotated[str | None, Field(description="關係文書法律編號，例：01177")] = None,
    page: Annotated[int, Field(description="頁數，預設1")] = 1,
    limit: Annotated[int, Field(description="每頁筆數，預設20，建議不超過100")] = 20,
    output_fields: Annotated[
        list[str] | None, Field(description="自訂回傳欄位（如需指定欄位，請填寫欄位名稱列表）")
    ] = None,
) -> str:
    """
    列出立法院會議列表。

    Args:
        term: 屆，例：11
        meeting_code: 會議代碼，例：院會-11-2-6
        session: 會期，例：2
        meeting_type: 會議種類，例：院會
        meeting_attendee: 出席委員，例：陳秀寳
        date: 日期，格式：YYYY-MM-DD，例：2024-10-25
        committee_code: 委員會代號，例：23
        meeting_id: 會議編號，例：2024102368
        meeting_bills_bill_no: 關係文書議案編號，例：202110071090000
        meeting_bills_law_no: 關係文書法律編號，例：01177
        page: 頁數，預設1
        limit: 每頁筆數，預設20，建議不超過100
        output_fields: 自訂回傳欄位（如需指定欄位，請填寫欄位名稱列表）

    Returns:
        str: JSON 格式的會議列表。

    Raises:
        例外時回傳中文錯誤訊息字串。
    """
    try:
        req = ListMeetsRequest(
            term=term,
            meeting_code=meeting_code,
            session=session,
            meeting_type=meeting_type,
            meeting_attendee=meeting_attendee,
            date=date,
            committee_code=committee_code,
            meeting_id=meeting_id,
            meeting_bills_bill_no=meeting_bills_bill_no,
            meeting_bills_law_no=meeting_bills_law_no,
            page=page,
            limit=limit,
            output_fields=output_fields or [],
        )
        resp = await req.do()
        return json.dumps(resp, ensure_ascii=False, indent=2)
    except Exception as e:
        return _serialize_tool_error("Failed to list meets", e)


async def get_meet(meet_id: Annotated[str, Field(description="會議代碼，例：院會-11-2-3")]) -> str:
    """
    取得特定會議的詳細資訊。

    Args:
        meet_id: 會議代碼，例：院會-11-2-3

    Returns:
        str: JSON 格式的會議詳細資訊。

    Raises:
        例外時回傳中文錯誤訊息字串。
    """
    try:
        req = GetMeetRequest(meet_id=meet_id)
        resp = await req.do()
        return json.dumps(resp, ensure_ascii=False, indent=2)
    except Exception as e:
        return _serialize_tool_error("Failed to get meet detail", e)


async def get_meet_bills(
    meet_id: Annotated[str, Field(description="會議代碼，例：院會-11-2-3")],
    term: Annotated[int | None, Field(description="屆，例：11")] = None,
    session: Annotated[int | None, Field(description="會期，例：2")] = None,
    bill_flow_status: Annotated[str | None, Field(description="議案流程狀態，如：交付審查、三讀")] = None,
    bill_type: Annotated[str | None, Field(description="議案類別，如：法律案、預算案")] = None,
    proposer: Annotated[str | None, Field(description="提案人姓名")] = None,
    co_proposer: Annotated[str | None, Field(description="連署人姓名")] = None,
    law_number: Annotated[str | None, Field(description="法律編號")] = None,
    bill_status: Annotated[str | None, Field(description="議案狀態，如：交付審查、三讀、排入院會")] = None,
    meeting_code: Annotated[str | None, Field(description="會議代碼")] = None,
    proposal_source: Annotated[str | None, Field(description="提案來源，如：委員提案、政府提案")] = None,
    bill_number: Annotated[str | None, Field(description="議案編號")] = None,
    proposal_number: Annotated[str | None, Field(description="提案編號")] = None,
    reference_number: Annotated[str | None, Field(description="字號")] = None,
    article_number: Annotated[str | None, Field(description="法條編號")] = None,
    proposal_date: Annotated[str | None, Field(description="提案日期，格式：YYYY-MM-DD")] = None,
    proposal_unit_or_member: Annotated[str | None, Field(description="提案單位或提案委員")] = None,
    page: Annotated[int, Field(description="頁數，預設1")] = 1,
    limit: Annotated[int, Field(description="每頁筆數，預設20，建議不超過100")] = 20,
    output_fields: Annotated[
        list[str] | None, Field(description="自訂回傳欄位（如需指定欄位，請填寫欄位名稱列表）")
    ] = None,
) -> str:
    """
    取得會議內的議案列表。

    Args:
        meet_id: 會議代碼，例：院會-11-2-3
        term: 屆，例：11
        session: 會期，例：2
        bill_flow_status: 議案流程狀態，如：交付審查、三讀
        bill_type: 議案類別，如：法律案、預算案
        proposer: 提案人姓名
        co_proposer: 連署人姓名
        law_number: 法律編號
        bill_status: 議案狀態，如：交付審查、三讀、排入院會
        meeting_code: 會議代碼
        proposal_source: 提案來源，如：委員提案、政府提案
        bill_number: 議案編號
        proposal_number: 提案編號
        reference_number: 字號
        article_number: 法條編號
        proposal_date: 提案日期，格式：YYYY-MM-DD
        proposal_unit_or_member: 提案單位或提案委員
        page: 頁數，預設1
        limit: 每頁筆數，預設20，建議不超過100
        output_fields: 自訂回傳欄位（如需指定欄位，請填寫欄位名稱列表）

    Returns:
        str: JSON 格式的會議內議案資料。

    Raises:
        例外時回傳中文錯誤訊息字串。
    """
    try:
        req = GetMeetBillsRequest(
            meet_id=meet_id,
            term=term,
            session=session,
            bill_flow_status=bill_flow_status,
            bill_type=bill_type,
            proposer=proposer,
            co_proposer=co_proposer,
            law_number=law_number,
            bill_status=bill_status,
            meeting_code=meeting_code,
            proposal_source=proposal_source,
            bill_number=bill_number,
            proposal_number=proposal_number,
            reference_number=reference_number,
            article_number=article_number,
            proposal_date=proposal_date,
            proposal_unit_or_member=proposal_unit_or_member,
            page=page,
            limit=limit,
            output_fields=output_fields or [],
        )
        resp = await req.do()
        return json.dumps(resp, ensure_ascii=False, indent=2)
    except Exception as e:
        return _serialize_tool_error("Failed to get meet bills", e)


async def get_meet_interpellations(
    meet_id: Annotated[str, Field(description="會議代碼，例：院會-11-2-3")],
    interpellation_member: Annotated[str | None, Field(description="質詢委員，例：羅智強")] = None,
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
    取得會議內的質詢列表。

    Args:
        meet_id: 會議代碼，例：院會-11-2-3
        interpellation_member: 質詢委員，例：羅智強
        term: 屆，例：11
        session: 會期，例：2
        meeting_code: 會議代碼，例：院會-11-2-6
        page: 頁數，預設1
        limit: 每頁筆數，預設20，建議不超過100
        output_fields: 自訂回傳欄位（如需指定欄位，請填寫欄位名稱列表）

    Returns:
        str: JSON 格式的會議內質詢資料。

    Raises:
        例外時回傳中文錯誤訊息字串。
    """
    try:
        req = GetMeetInterpellationsRequest(
            meet_id=meet_id,
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
        return _serialize_tool_error("Failed to get meet interpellations", e)
