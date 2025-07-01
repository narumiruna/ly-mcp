import json
from typing import Annotated

from loguru import logger
from mcp.server.fastmcp import FastMCP
from pydantic import Field

from .api import BillDocHtmlRequest
from .api import BillMeetsRequest
from .api import BillRelatedBillsRequest
from .api import GetBillDetailRequest
from .api import SearchBillRequest

# https://github.com/jlowin/fastmcp/issues/81#issuecomment-2714245145
mcp = FastMCP("立法院 API v2 MCP Server", log_level="ERROR")


@mcp.tool()
async def search_bills(
    term: Annotated[int | None, Field(description="屆，例：11")] = None,
    session: Annotated[int | None, Field(description="會期，例：2")] = None,
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
    page: Annotated[int, Field(description="頁數，預設1")] = 1,
    limit: Annotated[int, Field(description="每頁筆數，預設20，建議不超過100")] = 20,
    output_fields: Annotated[
        list[str] | None, Field(description="自訂回傳欄位（如需指定欄位，請填寫欄位名稱列表）")
    ] = None,
) -> str:
    """
    搜尋立法院議案列表。

    Args:
        term: 屆，例：11
        session: 會期，例：2
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
        str: JSON 格式的議案查詢結果。

    Raises:
        例外時回傳中文錯誤訊息字串。
    """
    try:
        req = SearchBillRequest(
            session=session,
            term=term,
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
            page=page,
            limit=limit,
            output_fields=output_fields or [],
        )

        resp = await req.do()
        return json.dumps(resp, ensure_ascii=False, indent=2)

    except Exception as e:
        msg = f"Failed to search bills, got: {e}"
        logger.error(msg)
        return msg


@mcp.tool()
async def get_bill_detail(
    bill_no: Annotated[str, Field(description="議案編號，必填，例: 203110077970000")],
) -> str:
    """
    取得特定議案的詳細資訊。

    Args:
        bill_no: 議案編號，必填，例：203110077970000

    Returns:
        str: JSON 格式，包含議案基本資料、提案人資訊、議案流程、相關法條等詳細資訊。

    Raises:
        例外時回傳中文錯誤訊息字串。
    """
    try:
        req = GetBillDetailRequest(bill_no=bill_no)
        resp = await req.do()
        return json.dumps(resp, ensure_ascii=False, indent=2)
    except Exception as e:
        msg = f"Failed to get bill detail, got: {e}"
        logger.error(msg)
        return msg


@mcp.tool()
async def get_bill_related_bills(
    bill_no: Annotated[str, Field(description="議案編號，必填，例: 203110077970000")],
    page: Annotated[int, Field(description="頁數，預設1")] = 1,
    limit: Annotated[int, Field(description="每頁筆數，預設20，建議不超過50")] = 20,
) -> str:
    """
    取得特定議案的相關議案列表。

    Args:
        bill_no: 議案編號，必填，例：203110077970000
        page: 頁數，預設1
        limit: 每頁筆數，預設20，建議不超過50

    Returns:
        str: JSON 格式，包含該議案的相關議案資訊（關聯類型、相關議案編號等）。

    Raises:
        例外時回傳中文錯誤訊息字串。
    """
    try:
        req = BillRelatedBillsRequest(bill_no=bill_no, page=page, limit=limit)
        resp = await req.do()
        return json.dumps(resp, ensure_ascii=False, indent=2)
    except Exception as e:
        msg = f"Failed to get bill related bills, got: {e}"
        logger.error(msg)
        return msg


@mcp.tool()
async def get_bill_meets(
    bill_no: Annotated[str, Field(description="議案編號，必填，例: 203110077970000")],
    term: Annotated[int | None, Field(description="屆，例: 11")] = None,
    session: Annotated[int | None, Field(description="會期，例: 2")] = None,
    meeting_type: Annotated[str | None, Field(description="會議種類，例: 院會、委員會")] = None,
    date: Annotated[str | None, Field(description="會議日期，格式：YYYY-MM-DD，例: 2024-10-25")] = None,
    page: Annotated[int, Field(description="頁數，預設1")] = 1,
    limit: Annotated[int, Field(description="每頁筆數，預設20")] = 20,
) -> str:
    """
    取得特定議案的相關會議列表。

    Args:
        bill_no: 議案編號，必填，例：203110077970000
        term: 屆期篩選，例：11
        session: 會期篩選，例：2
        meeting_type: 會議種類篩選，例：院會、委員會
        date: 會議日期篩選，格式：YYYY-MM-DD
        page: 頁數，預設1
        limit: 每頁筆數，預設20

    Returns:
        str: JSON 格式，包含該議案在各會議中的審議紀錄（會議資訊、審議結果、發言紀錄等）。

    Raises:
        例外時回傳中文錯誤訊息字串。
    """
    try:
        req = BillMeetsRequest(
            bill_no=bill_no,
            term=term,
            session=session,
            meeting_type=meeting_type,
            date=date,
            page=page,
            limit=limit,
        )
        resp = await req.do()
        return json.dumps(resp, ensure_ascii=False, indent=2)
    except Exception as e:
        msg = f"Failed to get bill meets, got: {e}"
        logger.error(msg)
        return msg


@mcp.tool()
async def get_bill_doc_html(
    bill_no: Annotated[str, Field(description="議案編號，必填，例: 203110077970000")],
) -> str:
    """
    取得特定議案的文件 HTML 內容列表。

    Args:
        bill_no: 議案編號，必填，例：203110077970000

    Returns:
        str: JSON 格式，包含該議案的所有相關文件 HTML 內容（議案本文、附件、修正對照表等）。

    Notes:
        若回傳空白內容，可能原因包含：該議案尚無正式文件、文件尚未數位化、或 API 資料延遲更新。
        建議先使用 get_bill_detail 確認議案存在後再查詢文件內容。

    Raises:
        例外時回傳中文錯誤訊息字串。
    """
    try:
        req = BillDocHtmlRequest(bill_no=bill_no)
        resp = await req.do()
        return json.dumps(resp, ensure_ascii=False, indent=2)
    except Exception as e:
        msg = f"Failed to get bill doc html, got: {e}"
        logger.error(msg)
        return msg


def main() -> None:
    mcp.run()
