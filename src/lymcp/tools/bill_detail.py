import json
from typing import Annotated

from loguru import logger
from pydantic import Field

from ..api_client import make_api_request
from ..models import extract_bill_summary


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
