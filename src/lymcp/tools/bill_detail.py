import json
from typing import Annotated

from pydantic import Field

from ..api_client import api_client


async def get_bill_detail(
    bill_no: Annotated[str, Field(description="議案編號，例: 203110077970000")],
) -> str:
    """
    取得特定議案的詳細資訊。

    參數說明：
    - bill_no: 議案編號，必填 (例: 203110077970000)

    回傳內容包含議案基本資料、提案人資訊、議案流程、相關法條等詳細資訊。
    """
    api_response = await api_client.get_bill_detail(bill_no=bill_no)

    if not api_response.success:
        return f"❌ {api_response.message}"

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
    api_response = await api_client.get_bill_related_bills(
        bill_no=bill_no, page=page, limit=limit
    )

    if not api_response.success:
        return f"❌ {api_response.message}"

    return f"✅ {api_response.message}\n\n{json.dumps(api_response.data, ensure_ascii=False, indent=2)}"
