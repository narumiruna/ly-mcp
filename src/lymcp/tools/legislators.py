import json
from typing import Annotated

from pydantic import Field

from lymcp.api import GetLegislatorCosignBillsRequest
from lymcp.api import GetLegislatorMeetsRequest
from lymcp.api import GetLegislatorProposeBillsRequest
from lymcp.api import GetLegislatorRequest
from lymcp.api import ListLegislatorsRequest
from lymcp.tools.support import serialize_tool_error as _serialize_tool_error


async def list_legislators(
    term: Annotated[int | None, Field(description="屆，例：11")] = None,
    party: Annotated[str | None, Field(description="黨籍，例：民主進步黨")] = None,
    district_name: Annotated[str | None, Field(description="選區名稱，例：臺南市第6選舉區")] = None,
    legislator_id: Annotated[int | None, Field(description="歷屆立法委員編號，例：1160")] = None,
    legislator_name: Annotated[str | None, Field(description="委員姓名，例：韓國瑜")] = None,
    page: Annotated[int, Field(description="頁數，預設1")] = 1,
    limit: Annotated[int, Field(description="每頁筆數，預設20，建議不超過100")] = 20,
    output_fields: Annotated[
        list[str] | None, Field(description="自訂回傳欄位（如需指定欄位，請填寫欄位名稱列表）")
    ] = None,
) -> str:
    """
    取得立法委員列表。

    Args:
        term: 屆，例：11
        party: 黨籍，例：民主進步黨
        district_name: 選區名稱，例：臺南市第6選舉區
        legislator_id: 歷屆立法委員編號，例：1160
        legislator_name: 委員姓名，例：韓國瑜
        page: 頁數，預設1
        limit: 每頁筆數，預設20，建議不超過100
        output_fields: 自訂回傳欄位（如需指定欄位，請填寫欄位名稱列表）

    Returns:
        str: JSON 格式的立法委員列表。

    Raises:
        例外時回傳中文錯誤訊息字串。
    """
    try:
        req = ListLegislatorsRequest(
            term=term,
            party=party,
            district_name=district_name,
            legislator_id=legislator_id,
            legislator_name=legislator_name,
            page=page,
            limit=limit,
            output_fields=output_fields or [],
        )
        resp = await req.do()
        return json.dumps(resp, ensure_ascii=False, indent=2)
    except Exception as e:
        return _serialize_tool_error("Failed to list legislators", e)


async def get_legislator(
    term: Annotated[int, Field(description="屆，例：11")],
    name: Annotated[str, Field(description="委員姓名，例：韓國瑜")],
) -> str:
    """
    取得特定立法委員的詳細資訊。

    Args:
        term: 屆，例：11
        name: 委員姓名，例：韓國瑜

    Returns:
        str: JSON 格式，包含該立法委員的詳細資訊。

    Raises:
        例外時回傳中文錯誤訊息字串。
    """
    try:
        req = GetLegislatorRequest(term=term, name=name)
        resp = await req.do()
        return json.dumps(resp, ensure_ascii=False, indent=2)
    except Exception as e:
        return _serialize_tool_error("Failed to get legislator", e)


async def get_legislator_propose_bills(
    term: Annotated[int, Field(description="屆，例：11")],
    name: Annotated[str, Field(description="委員姓名，例：韓國瑜")],
    bill_term: Annotated[int | None, Field(description="議案所屬屆期，例：11")] = None,
    session: Annotated[int | None, Field(description="議案所屬會期，例：2")] = None,
    bill_flow_status: Annotated[str | None, Field(description="議案流程狀態，如：交付審查、三讀")] = None,
    bill_type: Annotated[str | None, Field(description="議案類別，如：法律案、預算案")] = None,
    proposer: Annotated[str | None, Field(description="提案人姓名")] = None,
    cosigner: Annotated[str | None, Field(description="連署人姓名")] = None,
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
    取得委員為提案人的法案列表。

    Args:
        term: 屆，例：11
        name: 委員姓名，例：韓國瑜
        bill_term: 議案所屬屆期，例：11
        session: 議案所屬會期，例：2
        bill_flow_status: 議案流程狀態，如：交付審查、三讀
        bill_type: 議案類別，如：法律案、預算案
        proposer: 提案人姓名
        cosigner: 連署人姓名
        law_number: 法律編號
        bill_status: 議案狀態，如：交付審查、三讀、排入院會
        meeting_code: 會議代碼
        proposal_source: 提案來源，如：委員提案、政府提案
        bill_number: 議案編號
        proposal_number: 提案編號
        reference_number: 字號
        article_number: 法條編號
        proposal_date: 提案日期，格式：YYYY-MM-DD
        page: 頁數，預設1
        limit: 每頁筆數，預設20，建議不超過100
        output_fields: 自訂回傳欄位（如需指定欄位，請填寫欄位名稱列表）

    Returns:
        str: JSON 格式的委員為提案人的法案列表。

    Raises:
        例外時回傳中文錯誤訊息字串。
    """
    try:
        req = GetLegislatorProposeBillsRequest(
            term=term,
            name=name,
            bill_term=bill_term,
            session=session,
            bill_flow_status=bill_flow_status,
            bill_type=bill_type,
            proposer=proposer,
            co_proposer=cosigner,
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
        return _serialize_tool_error("Failed to get legislator propose bills", e)


async def get_legislator_cosign_bills(
    term: Annotated[int, Field(description="屆，例：11")],
    name: Annotated[str, Field(description="委員姓名，例：韓國瑜")],
    bill_term: Annotated[int | None, Field(description="議案所屬屆期，例：11")] = None,
    session: Annotated[int | None, Field(description="議案所屬會期，例：2")] = None,
    bill_flow_status: Annotated[str | None, Field(description="議案流程狀態，如：交付審查、三讀")] = None,
    bill_type: Annotated[str | None, Field(description="議案類別，如：法律案、預算案")] = None,
    proposer: Annotated[str | None, Field(description="提案人姓名")] = None,
    cosigner: Annotated[str | None, Field(description="連署人姓名")] = None,
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
    取得委員為連署人的法案列表。

    Args:
        term: 屆，例：11
        name: 委員姓名，例：韓國瑜
        bill_term: 議案所屬屆期，例：11
        session: 議案所屬會期，例：2
        bill_flow_status: 議案流程狀態，如：交付審查、三讀
        bill_type: 議案類別，如：法律案、預算案
        proposer: 提案人姓名
        cosigner: 連署人姓名
        law_number: 法律編號
        bill_status: 議案狀態，如：交付審查、三讀、排入院會
        meeting_code: 會議代碼
        proposal_source: 提案來源，如：委員提案、政府提案
        bill_number: 議案編號
        proposal_number: 提案編號
        reference_number: 字號
        article_number: 法條編號
        proposal_date: 提案日期，格式：YYYY-MM-DD
        page: 頁數，預設1
        limit: 每頁筆數，預設20，建議不超過100
        output_fields: 自訂回傳欄位（如需指定欄位，請填寫欄位名稱列表）

    Returns:
        str: JSON 格式的委員為連署人的法案列表。

    Raises:
        例外時回傳中文錯誤訊息字串。
    """
    try:
        req = GetLegislatorCosignBillsRequest(
            term=term,
            name=name,
            bill_term=bill_term,
            session=session,
            bill_flow_status=bill_flow_status,
            bill_type=bill_type,
            proposer=proposer,
            co_proposer=cosigner,
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
        return _serialize_tool_error("Failed to get legislator cosign bills", e)


async def get_legislator_meets(
    term: Annotated[int, Field(description="屆，例：11")],
    name: Annotated[str, Field(description="委員姓名，例：韓國瑜")],
    meet_term: Annotated[int | None, Field(description="會議所屬屆期，例：11")] = None,
    meeting_code: Annotated[str | None, Field(description="會議代碼，例：院會-11-2-6")] = None,
    session: Annotated[int | None, Field(description="會期，例：2")] = None,
    meeting_type: Annotated[str | None, Field(description="會議種類，例：院會")] = None,
    member: Annotated[str | None, Field(description="出席委員，例：陳秀寳")] = None,
    date: Annotated[str | None, Field(description="日期，例：2024-10-25")] = None,
    committee_code: Annotated[int | None, Field(description="委員會代號，例：23")] = None,
    meet_id: Annotated[str | None, Field(description="會議編號，例：2024102368")] = None,
    bill_no_nested: Annotated[str | None, Field(description="關係文書議案編號，例：202110071090000")] = None,
    law_number_nested: Annotated[str | None, Field(description="關係文書法律編號，例：01177")] = None,
    page: Annotated[int, Field(description="頁數，預設1")] = 1,
    limit: Annotated[int, Field(description="每頁筆數，預設20，建議不超過100")] = 20,
    output_fields: Annotated[
        list[str] | None, Field(description="自訂回傳欄位（如需指定欄位，請填寫欄位名稱列表）")
    ] = None,
) -> str:
    """
    取得委員出席的會議列表。

    Args:
        term: 屆，例：11
        name: 委員姓名，例：韓國瑜
        meet_term: 會議所屬屆期，例：11
        meeting_code: 會議代碼，例：院會-11-2-6
        session: 會期，例：2
        meeting_type: 會議種類，例：院會
        member: 出席委員，例：陳秀寳
        date: 日期，例：2024-10-25
        committee_code: 委員會代號，例：23
        meet_id: 會議編號，例：2024102368
        bill_no_nested: 關係文書議案編號，例：202110071090000
        law_number_nested: 關係文書法律編號，例：01177
        page: 頁數，預設1
        limit: 每頁筆數，預設20，建議不超過100
        output_fields: 自訂回傳欄位（如需指定欄位，請填寫欄位名稱列表）

    Returns:
        str: JSON 格式的委員出席會議列表。

    Raises:
        例外時回傳中文錯誤訊息字串。
    """
    try:
        req = GetLegislatorMeetsRequest(
            term=term,
            name=name,
            meet_term=meet_term,
            meeting_code=meeting_code,
            session=session,
            meeting_type=meeting_type,
            member=member,
            date=date,
            committee_code=committee_code,
            meet_id=meet_id,
            bill_no_nested=bill_no_nested,
            law_number_nested=law_number_nested,
            page=page,
            limit=limit,
            output_fields=output_fields or [],
        )
        resp = await req.do()
        return json.dumps(resp, ensure_ascii=False, indent=2)
    except Exception as e:
        return _serialize_tool_error("Failed to get legislator meets", e)
