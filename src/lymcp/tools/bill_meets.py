from typing import Annotated

from pydantic import Field

from .direct_api import get_bill_meets_json


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
    # 使用新的結構化 API 直接取得資料
    return await get_bill_meets_json(
        bill_no=bill_no,
        term=term,
        session=session,
        meeting_type=meeting_type,
        date=date,
        page=page,
        limit=limit,
    )
