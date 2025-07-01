import json
from typing import Annotated

from pydantic import Field

from ..api_client import api_client


async def search_bills(
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
) -> str:
    """
    搜尋立法院議案列表。可依據屆期、會期、議案類別、提案人等條件進行篩選。

    參數說明：
    - term: 屆期，如第11屆
    - session: 會期，如第2會期
    - bill_category: 議案類別，如「法律案」、「預算案」
    - proposer: 提案人姓名
    - cosigner: 連署人姓名
    - bill_status: 議案狀態，如「交付審查」、「三讀」、「排入院會」、「委員會抽出逕付二讀(交付協商)」
    - proposal_source: 提案來源，如「委員提案」、「政府提案」
    - bill_no: 特定議案編號
    - proposal_date_start: 提案日期起始，格式: YYYY-MM-DD
    - proposal_date_end: 提案日期結束，格式: YYYY-MM-DD
    - page: 頁數 (預設1)
    - limit: 每頁筆數 (預設20，建議不超過100)

    回傳結構化議案摘要資訊，包含議案編號、標題、類別、提案人、狀態等主要資訊。

    常見議案狀態說明：
    - 「三讀」: 已完成立法程序
    - 「排入院會」: 等待院會審議
    - 「交付審查」: 送交委員會審查
    - 「委員會抽出逕付二讀(交付協商)」: 委員會審查完成，進入協商程序
    """
    api_response = await api_client.search_bills(
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

    if not api_response.success:
        return f"❌ {api_response.message}"

    return f"✅ {api_response.message}\n\n{json.dumps(api_response.data, ensure_ascii=False, indent=2)}"
