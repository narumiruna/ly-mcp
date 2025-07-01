"""
直接使用結構化 API 回應的工具
這些工具直接回傳 Pydantic 模型，提供更好的類型提示
"""
import json
from typing import Annotated

from pydantic import Field

from ..models import BillDetail
from ..models import BillMeetsResponse
from ..models import BillRelatedBillsResponse
from ..models import GetBillDetailRequest
from ..models import GetBillMeetsRequest
from ..models import GetBillRelatedBillsRequest
from ..models import SearchBillsRequest
from ..models import SearchBillsResponse


async def search_bills_direct(
    term: Annotated[int | None, Field(description="議案所屬屆期，例: 11")] = None,
    session: Annotated[int | None, Field(description="議案所屬會期，例: 2")] = None,
    bill_category: Annotated[str | None, Field(description="議案類別，例: 法律案")] = None,
    proposer: Annotated[str | None, Field(description="提案人，例: 徐欣瑩")] = None,
    cosigner: Annotated[str | None, Field(description="連署人，例: 林德福")] = None,
    bill_status: Annotated[str | None, Field(description="議案目前所處狀態，例: 交付審查、三讀、排入院會")] = None,
    proposal_source: Annotated[str | None, Field(description="議案的提案來源屬性，例: 委員提案")] = None,
    bill_no: Annotated[str | None, Field(description="議案編號，例: 202110068550000")] = None,
    proposal_date_start: Annotated[str | None, Field(description="提案日期起始，格式: YYYY-MM-DD")] = None,
    proposal_date_end: Annotated[str | None, Field(description="提案日期結束，格式: YYYY-MM-DD")] = None,
    page: Annotated[int, Field(description="頁數")] = 1,
    limit: Annotated[int, Field(description="每頁筆數")] = 20,
) -> SearchBillsResponse:
    """
    直接搜尋立法院議案，回傳結構化資料。

    使用範例：
    ```python
    result = await search_bills_direct(term=11, limit=5)
    for bill in result.bills:
        print(f"議案：{bill.title}")
        print(f"提案人：{bill.proposer}")
    ```
    """
    request = SearchBillsRequest(
        term=term,
        session=session,
        bill_category=bill_category,
        proposer=proposer,
        cosigner=cosigner,
        bill_status=bill_status,
        proposal_source=proposal_source,
        bill_no=bill_no,
        proposal_date_start=proposal_date_start,
        proposal_date_end=proposal_date_end,
        page=page,
        limit=limit,
    )

    return await request.async_do()


async def get_bill_detail_direct(
    bill_no: Annotated[str, Field(description="議案編號，例: 203110077970000")],
) -> BillDetail:
    """
    直接取得議案詳細資料，回傳結構化資料。

    使用範例：
    ```python
    bill = await get_bill_detail_direct("203110077970000")
    print(f"議案標題：{bill.title}")
    print(f"議案狀態：{bill.status}")
    if bill.law_numbers:
        print(f"相關法律：{bill.law_numbers}")
    ```
    """
    request = GetBillDetailRequest(bill_no=bill_no)
    return await request.async_do()


async def get_bill_related_bills_direct(
    bill_no: Annotated[str, Field(description="議案編號，例: 203110077970000")],
    page: Annotated[int, Field(description="頁數")] = 1,
    limit: Annotated[int, Field(description="每頁筆數")] = 20,
) -> BillRelatedBillsResponse:
    """
    直接取得相關議案，回傳結構化資料。

    使用範例：
    ```python
    result = await get_bill_related_bills_direct("203110077970000")
    print(f"查詢議案：{result.bill_no}")
    for related in result.related_bills:
        print(f"相關議案：{related.related_bill_no} ({related.relation_type})")
    ```
    """
    request = GetBillRelatedBillsRequest(
        bill_no=bill_no, page=page, limit=limit
    )
    return await request.async_do()


async def get_bill_meets_direct(
    bill_no: Annotated[str, Field(description="議案編號，例: 203110077970000")],
    term: Annotated[int | None, Field(description="屆，例: 11")] = None,
    session: Annotated[int | None, Field(description="會期，例: 2")] = None,
    meeting_type: Annotated[str | None, Field(description="會議種類，例: 院會")] = None,
    date: Annotated[str | None, Field(description="日期，例: 2024-10-25")] = None,
    page: Annotated[int, Field(description="頁數")] = 1,
    limit: Annotated[int, Field(description="每頁筆數")] = 20,
) -> BillMeetsResponse:
    """
    直接取得議案會議，回傳結構化資料。

    使用範例：
    ```python
    result = await get_bill_meets_direct("203110077970000")
    print(f"查詢議案：{result.bill_no}")
    for meeting in result.meetings:
        print(f"會議：{meeting.meeting_name} ({meeting.meeting_date})")
        print(f"審議結果：{meeting.discussion_result}")
    ```
    """
    request = GetBillMeetsRequest(
        bill_no=bill_no,
        term=term,
        session=session,
        meeting_type=meeting_type,
        date=date,
        page=page,
        limit=limit,
    )
    return await request.async_do()


# 為了演示，也提供 JSON 字符串版本
async def get_bill_meets_json(
    bill_no: Annotated[str, Field(description="議案編號，例: 203110077970000")],
    term: Annotated[int | None, Field(description="屆，例: 11")] = None,
    session: Annotated[int | None, Field(description="會期，例: 2")] = None,
    meeting_type: Annotated[str | None, Field(description="會議種類，例: 院會")] = None,
    date: Annotated[str | None, Field(description="日期，例: 2024-10-25")] = None,
    page: Annotated[int, Field(description="頁數")] = 1,
    limit: Annotated[int, Field(description="每頁筆數")] = 20,
) -> str:
    """
    取得議案會議並回傳 JSON 字符串（用於 MCP 工具）。
    """
    try:
        result = await get_bill_meets_direct(
            bill_no=bill_no,
            term=term,
            session=session,
            meeting_type=meeting_type,
            date=date,
            page=page,
            limit=limit,
        )

        return f"✅ 查詢成功\n\n{json.dumps(result.model_dump(by_alias=True), ensure_ascii=False, indent=2)}"

    except Exception as e:
        return f"❌ 查詢失敗：{str(e)}"
