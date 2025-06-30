import json
from typing import Annotated

from pydantic import Field

from ..api_client import make_api_request


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
        # 若 data 為 dict 且有 "data" key，則進入 data 子欄位
        bill_data = api_response.data
        if isinstance(bill_data, dict) and "data" in bill_data and isinstance(bill_data["data"], dict):
            bill_data = bill_data["data"]

        # 格式化結構化摘要
        if isinstance(bill_data, dict):
            structured_summary = "## 議案詳細資訊摘要\n\n"

            # 基本資訊
            structured_summary += "### 📋 基本資訊\n"
            structured_summary += f"- **議案編號**: {bill_data.get('議案編號', 'N/A')}\n"
            structured_summary += f"- **屆期**: 第{bill_data.get('屆', 'N/A')}屆第{bill_data.get('會期', 'N/A')}會期\n"
            structured_summary += f"- **提案日期**: {bill_data.get('提案日期', 'N/A')}\n"
            structured_summary += f"- **最新進度日期**: {bill_data.get('最新進度日期', 'N/A')}\n"
            structured_summary += f"- **目前狀態**: {bill_data.get('狀態', 'N/A')}\n\n"

            # 法律相關
            if bill_data.get("法律編號:str"):
                structured_summary += "### ⚖️ 相關法律\n"
                for law in bill_data.get("法律編號:str", []):
                    structured_summary += f"- {law}\n"
                structured_summary += "\n"

            # 議案流程
            if bill_data.get("議案流程"):
                structured_summary += "### 🔄 議案流程\n"
                for process in bill_data.get("議案流程", []):
                    if isinstance(process, dict):
                        status = process.get("狀態", "N/A")
                        dates = process.get("日期", [])
                        if dates:
                            date_str = ", ".join(dates) if isinstance(dates, list) else str(dates)
                            structured_summary += f"- **{status}**: {date_str}\n"
                        else:
                            structured_summary += f"- **{status}**\n"
                structured_summary += "\n"

            # 相關附件
            if bill_data.get("相關附件"):
                structured_summary += "### 📎 相關附件\n"
                for attachment in bill_data.get("相關附件", []):
                    if isinstance(attachment, dict):
                        name = attachment.get("名稱", "N/A")
                        structured_summary += f"- {name}\n"
                structured_summary += "\n"

            return f"✅ {api_response.message}\n\n{structured_summary}"
        else:
            return f"✅ {api_response.message}\n\n{json.dumps(bill_data, ensure_ascii=False, indent=2)}"

    return f"✅ {api_response.message}\n\n{json.dumps(api_response.data, ensure_ascii=False, indent=2)}"


async def get_bill_related_bills(
    bill_no: Annotated[str, Field(description="議案編號，例: 203110077970000")],
    page: Annotated[int, Field(description="頁數")] = 1,
    limit: Annotated[int, Field(description="每頁筆數")] = 20,
) -> str:
    """
    取得特定議案的相關議案列表。

    參數說明：
    - bill_no: 議案編號，必填 (例: 203110077970000)
    - page: 頁數 (預設1)
    - limit: 每頁筆數 (預設20，建議不超過50)

    回傳該議案的相關議案資訊，包含關聯類型、相關議案編號等。
    """

    params = {"page": page, "limit": limit}
    api_response = await make_api_request(f"/bills/{bill_no}/related_bills", params, f"取得議案 {bill_no} 相關議案")

    if not api_response.success:
        return f"❌ {api_response.message}"

    # 檢查資料是否過大（超過20000字元時進行截斷提示）
    data_str = json.dumps(api_response.data, ensure_ascii=False, indent=2)
    if len(data_str) > 20000:
        return (
            f"✅ {api_response.message}\n\n"
            "⚠️ 相關議案內容過大，僅顯示部分內容。建議使用分頁參數查詢。\n\n"
            f"{data_str[:15000]}\n\n...(內容過長，已截斷)"
        )

    return f"✅ {api_response.message}\n\n{data_str}"


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

    # 檢查是否為空的結構化資料
    if isinstance(api_response.data, dict | list) and not api_response.data:
        return "⚠️ 該議案暫無文件 HTML 內容。\n\n" "該議案目前沒有可用的文件內容，可能正在處理中或尚未上傳至系統。"

    return f"✅ {api_response.message}\n\n{json.dumps(api_response.data, ensure_ascii=False, indent=2)}"
