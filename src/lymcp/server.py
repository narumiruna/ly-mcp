import json
from typing import Annotated

from loguru import logger
from mcp.server.fastmcp import FastMCP
from pydantic import Field

from lymcp.api import GetBillDocHtmlRequest
from lymcp.api import GetBillMeetsRequest
from lymcp.api import GetBillRelatedBillsRequest
from lymcp.api import GetBillRequest
from lymcp.api import GetCommitteeMeetsRequest
from lymcp.api import GetCommitteeRequest
from lymcp.api import GetGazetteAgendaRequest
from lymcp.api import GetGazetteAgendasRequest
from lymcp.api import GetGazetteRequest
from lymcp.api import GetInterpellationRequest
from lymcp.api import GetIvodRequest
from lymcp.api import GetLegislatorInterpellationsRequest
from lymcp.api import GetMeetIvodsRequest
from lymcp.api import GetStatRequest
from lymcp.api import ListBillRequest
from lymcp.api import ListCommitteesRequest
from lymcp.api import ListGazetteAgendasRequest
from lymcp.api import ListGazettesRequest
from lymcp.api import ListInterpellationsRequest
from lymcp.api import ListIvodsRequest

# https://github.com/jlowin/fastmcp/issues/81#issuecomment-2714245145
mcp = FastMCP("立法院 API v2 MCP Server", log_level="ERROR")

@mcp.tool()
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
        msg = f"Failed to get statistics, got: {e}"
        logger.error(msg)
        return msg

@mcp.tool()
async def list_bills(
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
    列出立法院議案列表。

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
        req = ListBillRequest(
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
        msg = f"Failed to list bills, got: {e}"
        logger.error(msg)
        return msg


@mcp.tool()
async def get_bill(
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
        req = GetBillRequest(bill_no=bill_no)
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
        req = GetBillRelatedBillsRequest(bill_no=bill_no, page=page, limit=limit)
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
        req = GetBillMeetsRequest(
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
        req = GetBillDocHtmlRequest(bill_no=bill_no)
        resp = await req.do()
        return json.dumps(resp, ensure_ascii=False, indent=2)
    except Exception as e:
        msg = f"Failed to get bill doc html, got: {e}"
        logger.error(msg)
        return msg


@mcp.tool()
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
        msg = f"Failed to list committees, got: {e}"
        logger.error(msg)
        return msg


@mcp.tool()
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
        msg = f"Failed to get committee, got: {e}"
        logger.error(msg)
        return msg


@mcp.tool()
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
        msg = f"Failed to get committee meets, got: {e}"
        logger.error(msg)
        return msg


@mcp.tool()
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
        msg = f"Failed to list gazettes, got: {e}"
        logger.error(msg)
        return msg


@mcp.tool()
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
        msg = f"Failed to get gazette detail, got: {e}"
        logger.error(msg)
        return msg


@mcp.tool()
async def get_gazette_agendas(
    gazette_id: Annotated[str, Field(description="公報編號，必填，例：1137701")],
    volume: Annotated[int | None, Field(description="卷，例：113")] = None,
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
        gazette_id: 公報編號，必填，例：1137701
        volume: 卷，例：113
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
            volume=volume,
            term=term,
            meeting_date=meeting_date,
            page=page,
            limit=limit,
            output_fields=output_fields or [],
        )
        resp = await req.do()
        return json.dumps(resp, ensure_ascii=False, indent=2)
    except Exception as e:
        msg = f"Failed to get gazette agendas, got: {e}"
        logger.error(msg)
        return msg


@mcp.tool()
async def list_gazette_agendas(
    gazette_id: Annotated[str | None, Field(description="公報編號，例：1137701")] = None,
    volume: Annotated[int | None, Field(description="卷，例：113")] = None,
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
            term=term,
            meeting_date=meeting_date,
            page=page,
            limit=limit,
            output_fields=output_fields or [],
        )
        resp = await req.do()
        return json.dumps(resp, ensure_ascii=False, indent=2)
    except Exception as e:
        msg = f"Failed to list gazette agendas, got: {e}"
        logger.error(msg)
        return msg


@mcp.tool()
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
        msg = f"Failed to get gazette agenda detail, got: {e}"
        logger.error(msg)
        return msg


@mcp.tool()
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
        msg = f"Failed to list interpellations, got: {e}"
        logger.error(msg)
        return msg


@mcp.tool()
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
        msg = f"Failed to get interpellation detail, got: {e}"
        logger.error(msg)
        return msg


@mcp.tool()
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
        msg = f"Failed to get legislator interpellations, got: {e}"
        logger.error(msg)
        return msg


@mcp.tool()
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
        msg = f"Failed to list IVODs, got: {e}"
        logger.error(msg)
        return msg


@mcp.tool()
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
        msg = f"Failed to get IVOD detail, got: {e}"
        logger.error(msg)
        return msg


@mcp.tool()
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
        msg = f"Failed to get meet IVODs, got: {e}"
        logger.error(msg)
        return msg


def main() -> None:
    mcp.run()
