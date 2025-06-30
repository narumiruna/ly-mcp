from typing import Any

from pydantic import BaseModel
from pydantic import Field


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
