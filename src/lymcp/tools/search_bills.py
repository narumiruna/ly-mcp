import json
from typing import Annotated
from typing import Any

from loguru import logger
from pydantic import Field

from ..api_client import make_api_request
from ..models import extract_bill_summary


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
