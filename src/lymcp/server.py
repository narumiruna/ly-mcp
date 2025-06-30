import json
from typing import Annotated
from typing import Any

import httpx
from loguru import logger
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel
from pydantic import Field

# https://github.com/jlowin/fastmcp/issues/81#issuecomment-2714245145
mcp = FastMCP("立法院 API v2 MCP Server", log_level="ERROR")

BASE_URL = "https://ly.govapi.tw/v2"


# Data models for structured responses
class BillSummary(BaseModel):
    """議案摘要資訊"""

    bill_no: str | None = Field(None, description="議案編號")
    title: str | None = Field(None, description="議案標題")
    category: str | None = Field(None, description="議案類別")
    proposer: str | None = Field(None, description="提案人")
    status: str | None = Field(None, description="議案狀態")
    proposal_date: str | None = Field(None, description="提案日期")


class APIResponse(BaseModel):
    """標準化 API 回應格式"""

    success: bool = Field(description="請求是否成功")
    message: str = Field(description="回應訊息或錯誤說明")
    data: Any | None = Field(None, description="回應資料")
    total: int | None = Field(None, description="總筆數")
    page: int | None = Field(None, description="目前頁數")
    limit: int | None = Field(None, description="每頁筆數")


async def make_api_request(
    endpoint: str, params: dict[str, Any] | None = None, description: str = "API request"
) -> APIResponse:
    """統一的 API 請求處理函數，包含完整的錯誤處理和記錄"""

    url = f"{BASE_URL}{endpoint}"
    logger.info(f"Making {description} request to {url} with params: {params}")

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.get(url, params=params)

            # 記錄回應狀態
            logger.info(f"API response status: {response.status_code}")

            # 處理各種 HTTP 狀態碼
            if response.status_code == 404:
                return APIResponse(
                    success=False,
                    message="查無資料：所查詢的資源不存在 (404)。請檢查參數是否正確。",
                    data=None,
                    total=None,
                    page=None,
                    limit=None,
                )
            elif response.status_code == 429:
                return APIResponse(
                    success=False,
                    message="請求過於頻繁 (429)。請稍後再試。",
                    data=None,
                    total=None,
                    page=None,
                    limit=None,
                )
            elif response.status_code == 500:
                return APIResponse(
                    success=False,
                    message="伺服器內部錯誤 (500)。API 服務可能暫時不可用。",
                    data=None,
                    total=None,
                    page=None,
                    limit=None,
                )
            elif response.status_code != 200:
                return APIResponse(
                    success=False,
                    message=f"API 請求失敗：HTTP {response.status_code}",
                    data=None,
                    total=None,
                    page=None,
                    limit=None,
                )

            # 檢查回應內容
            if not response.text or response.text.strip() == "":
                logger.warning(f"Empty response from {url}")
                return APIResponse(
                    success=False,
                    message="API 回傳空白內容。可能原因：該資源無資料、API 資料延遲更新、或查詢條件過於嚴格。",
                    data=None,
                    total=None,
                    page=None,
                    limit=None,
                )

            # 嘗試解析 JSON
            try:
                data = response.json()
                logger.info(f"Successfully parsed JSON response with {len(str(data))} characters")

                # 檢查 API 是否回傳錯誤 (有些 API 回傳 200 但內容是錯誤)
                if isinstance(data, dict) and data.get("error") is True:
                    error_message = data.get("message", "API 回傳錯誤但未提供詳細訊息")
                    return APIResponse(
                        success=False,
                        message=f"API 錯誤：{error_message}",
                        data=None,
                        total=None,
                        page=None,
                        limit=None,
                    )

                # 提取分頁資訊
                total = data.get("total") if isinstance(data, dict) else None
                page = data.get("page") if isinstance(data, dict) else None
                limit = data.get("limit") if isinstance(data, dict) else None

                return APIResponse(success=True, data=data, message="查詢成功", total=total, page=page, limit=limit)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON response: {e}")
                return APIResponse(
                    success=False,
                    message=f"API 回傳資料格式異常：無法解析 JSON 格式。原始內容長度：{len(response.text)} 字元",
                    data=None,
                    total=None,
                    page=None,
                    limit=None,
                )

        except httpx.TimeoutException:
            logger.error(f"Timeout for request to {url}")
            return APIResponse(
                success=False,
                message="請求逾時。API 服務可能繁忙，請稍後再試。",
                data=None,
                total=None,
                page=None,
                limit=None,
            )
        except httpx.ConnectError:
            logger.error(f"Connection error for request to {url}")
            return APIResponse(
                success=False,
                message="連線錯誤。請檢查網路連線或 API 服務是否正常。",
                data=None,
                total=None,
                page=None,
                limit=None,
            )
        except Exception as e:
            logger.error(f"Unexpected error for request to {url}: {e}")
            return APIResponse(
                success=False, message=f"未預期的錯誤：{str(e)}", data=None, total=None, page=None, limit=None
            )


def extract_bill_summary(bill_data: dict[str, Any]) -> BillSummary:
    """從 API 資料中提取議案摘要資訊"""
    # 處理提案人可能是 list 的情況
    proposer = bill_data.get("提案人")
    if isinstance(proposer, list):
        proposer = ", ".join(proposer) if proposer else None

    return BillSummary(
        bill_no=bill_data.get("議案編號"),
        title=bill_data.get("議案名稱") or bill_data.get("案由"),
        category=bill_data.get("議案類別"),
        proposer=proposer,
        status=bill_data.get("議案狀態"),
        proposal_date=bill_data.get("提案日期"),
    )


@mcp.tool()
async def search_bills(
    term: Annotated[int | None, Field(description="議案所屬屆期，例: 11")] = None,
    session: Annotated[int | None, Field(description="議案所屬會期，例: 2")] = None,
    bill_category: Annotated[str | None, Field(description="議案類別，例: 法律案")] = None,
    proposer: Annotated[str | None, Field(description="提案人，例: 徐欣瑩")] = None,
    cosigner: Annotated[str | None, Field(description="連署人，例: 林德福")] = None,
    bill_status: Annotated[str | None, Field(description="議案目前所處狀態，例: 交付審查")] = None,
    proposal_source: Annotated[str | None, Field(description="議案的提案來源屬性，例: 委員提案")] = None,
    bill_no: Annotated[str | None, Field(description="議案編號，例: 202110068550000")] = None,
    page: Annotated[int, Field(description="頁數")] = 1,
    limit: Annotated[int, Field(description="每頁筆數")] = 20,
    structured: Annotated[bool, Field(description="是否回傳結構化摘要資訊")] = False,
) -> str:
    """
    搜尋立法院議案列表。可依據屆期、會期、議案類別、提案人等條件進行篩選。

    參數說明：
    - term: 屆期，如第11屆
    - session: 會期，如第2會期
    - bill_category: 議案類別，如「法律案」、「預算案」
    - proposer: 提案人姓名
    - cosigner: 連署人姓名
    - bill_status: 議案狀態，如「交付審查」、「一讀」
    - proposal_source: 提案來源，如「委員提案」、「政府提案」
    - bill_no: 特定議案編號
    - page: 頁數 (預設1)
    - limit: 每頁筆數 (預設20，建議不超過100)
    - structured: 是否回傳結構化摘要 (預設False，回傳完整JSON)

    回傳格式：
    - structured=False: 完整 JSON 資料
    - structured=True: 結構化摘要，包含議案編號、標題、類別、提案人、狀態等主要資訊
    """

    params: dict[str, Any] = {"page": page, "limit": limit}

    if term is not None:
        params["屆"] = term
    if session is not None:
        params["會期"] = session
    if bill_category:
        params["議案類別"] = bill_category
    if proposer:
        params["提案人"] = proposer
    if cosigner:
        params["連署人"] = cosigner
    if bill_status:
        params["議案狀態"] = bill_status
    if proposal_source:
        params["提案來源"] = proposal_source
    if bill_no:
        params["議案編號"] = bill_no

    # 使用統一的 API 請求處理
    api_response = await make_api_request("/bills", params, "搜尋議案列表")

    if not api_response.success:
        return f"❌ {api_response.message}"

    if structured and api_response.data:
        try:
            # 提取結構化摘要
            bills_data = api_response.data
            if isinstance(bills_data, dict) and "bills" in bills_data:
                bills = bills_data["bills"]
                summaries = [extract_bill_summary(bill) for bill in bills]

                result = {
                    "查詢結果摘要": {
                        "總筆數": api_response.total,
                        "目前頁數": api_response.page,
                        "每頁筆數": api_response.limit,
                        "本頁筆數": len(summaries),
                    },
                    "議案列表": [summary.model_dump() for summary in summaries],
                }
                return f"✅ {api_response.message}\n\n{json.dumps(result, ensure_ascii=False, indent=2)}"
            else:
                return "⚠️ 資料格式異常：無法提取議案列表"
        except Exception as e:
            logger.error(f"Failed to structure bills data: {e}")
            return f"⚠️ 結構化處理失敗：{str(e)}\n\n原始資料：{json.dumps(api_response.data, ensure_ascii=False)}"

    # 回傳完整 JSON
    return f"✅ {api_response.message}\n\n{json.dumps(api_response.data, ensure_ascii=False, indent=2)}"


@mcp.tool()
async def get_bill_detail(
    bill_no: Annotated[str, Field(description="議案編號，例: 203110077970000")],
    structured: Annotated[bool, Field(description="是否回傳結構化摘要資訊")] = False,
) -> str:
    """
    取得特定議案的詳細資訊。

    參數說明：
    - bill_no: 議案編號，必填 (例: 203110077970000)
    - structured: 是否回傳結構化摘要 (預設False，回傳完整JSON)

    回傳內容包含議案基本資料、提案人資訊、議案流程、相關法條等詳細資訊。
    """

    api_response = await make_api_request(f"/bills/{bill_no}", None, f"取得議案 {bill_no} 詳細資訊")

    if not api_response.success:
        return f"❌ {api_response.message}"

    if structured and api_response.data:
        try:
            bill_data = api_response.data
            summary = extract_bill_summary(bill_data)

            # 提取更多詳細資訊
            detail_info = {
                "基本資訊": summary.model_dump(),
                "議案流程": bill_data.get("議案流程", []),
                "提案說明": bill_data.get("提案說明") or bill_data.get("案由"),
                "相關法條": bill_data.get("相關法條", []),
                "委員會": bill_data.get("委員會"),
                "文件": bill_data.get("文件", []),
            }

            return f"✅ {api_response.message}\n\n{json.dumps(detail_info, ensure_ascii=False, indent=2)}"
        except Exception as e:
            logger.error(f"Failed to structure bill detail: {e}")
            return f"⚠️ 結構化處理失敗：{str(e)}\n\n原始資料：{json.dumps(api_response.data, ensure_ascii=False)}"

    return f"✅ {api_response.message}\n\n{json.dumps(api_response.data, ensure_ascii=False, indent=2)}"


@mcp.tool()
async def get_bill_related_bills(bill_no: Annotated[str, Field(description="議案編號，例: 203110077970000")]) -> str:
    """
    取得特定議案的相關議案列表。

    參數說明：
    - bill_no: 議案編號，必填 (例: 203110077970000)

    回傳該議案的相關議案資訊，包含關聯類型、相關議案編號等。
    """

    api_response = await make_api_request(f"/bills/{bill_no}/related_bills", None, f"取得議案 {bill_no} 相關議案")

    if not api_response.success:
        return f"❌ {api_response.message}"

    return f"✅ {api_response.message}\n\n{json.dumps(api_response.data, ensure_ascii=False, indent=2)}"


@mcp.tool()
async def get_bill_doc_html(bill_no: Annotated[str, Field(description="議案編號，例: 203110077970000")]) -> str:
    """
    取得特定議案的文件 HTML 內容列表。

    參數說明：
    - bill_no: 議案編號，必填 (例: 203110077970000)

    回傳該議案的所有相關文件 HTML 內容，包含議案本文、附件、修正對照表等。

    注意事項：
    - 若回傳空白內容，可能原因包含：該議案尚無正式文件、文件尚未數位化、或 API 資料延遲更新
    - 建議先使用 get_bill_detail 確認議案存在後再查詢文件內容
    """

    api_response = await make_api_request(f"/bills/{bill_no}/doc_html", None, f"取得議案 {bill_no} 文件內容")

    if not api_response.success:
        return f"❌ {api_response.message}"

    # 特別處理文件內容的空白檢查
    if api_response.data is None or (isinstance(api_response.data, str) and not api_response.data.strip()):
        return (
            "⚠️ 該議案暫無文件 HTML 內容。\n\n"
            "可能原因：\n"
            "1. 該議案尚未產生正式文件\n"
            "2. 文件尚未完成數位化\n"
            "3. API 資料庫更新延遲\n"
            "4. 議案處於早期階段，僅有提案資訊\n\n"
            "建議：請稍後再試，或使用 get_bill_detail 取得議案基本資訊。"
        )

    return f"✅ {api_response.message}\n\n{json.dumps(api_response.data, ensure_ascii=False, indent=2)}"


@mcp.tool()
async def get_bill_meets(
    bill_no: Annotated[str, Field(description="議案編號，例: 203110077970000")],
    term: Annotated[int | None, Field(description="屆，例: 11")] = None,
    session: Annotated[int | None, Field(description="會期，例: 2")] = None,
    meeting_type: Annotated[str | None, Field(description="會議種類，例: 院會")] = None,
    date: Annotated[str | None, Field(description="日期，例: 2024-10-25")] = None,
    page: Annotated[int, Field(description="頁數")] = 1,
    limit: Annotated[int, Field(description="每頁筆數")] = 20,
) -> str:
    """
    取得特定議案的相關會議列表。

    參數說明：
    - bill_no: 議案編號，必填 (例: 203110077970000)
    - term: 屆期篩選 (例: 11)
    - session: 會期篩選 (例: 2)
    - meeting_type: 會議種類篩選 (例: 院會、委員會)
    - date: 會議日期篩選 (格式: YYYY-MM-DD)
    - page: 頁數 (預設1)
    - limit: 每頁筆數 (預設20)

    回傳該議案在各個會議中的審議紀錄，包含會議資訊、審議結果、發言紀錄等。
    """

    params: dict[str, Any] = {"page": page, "limit": limit}

    if term is not None:
        params["屆"] = term
    if session is not None:
        params["會期"] = session
    if meeting_type:
        params["會議種類"] = meeting_type
    if date:
        params["日期"] = date

    api_response = await make_api_request(f"/bills/{bill_no}/meets", params, f"取得議案 {bill_no} 相關會議")

    if not api_response.success:
        return f"❌ {api_response.message}"

    return f"✅ {api_response.message}\n\n{json.dumps(api_response.data, ensure_ascii=False, indent=2)}"


def main():
    mcp.run()
