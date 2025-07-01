from __future__ import annotations

from enum import Enum
from functools import cache
from typing import Any

import httpx
from pydantic import BaseModel
from pydantic import Field


class BillStatus(str, Enum):
    """議案狀態枚舉"""
    UNDER_REVIEW = "交付審查"
    THIRD_READING = "三讀"
    SCHEDULED = "排入院會"
    COMMITTEE_FORWARDED = "委員會抽出逕付二讀(交付協商)"


class BillCategory(str, Enum):
    """議案類別枚舉"""
    LAW = "法律案"
    BUDGET = "預算案"
    DECISION = "決議案"
    INQUIRY = "質詢案"


class ProposalSource(str, Enum):
    """提案來源枚舉"""
    COMMITTEE = "委員提案"
    GOVERNMENT = "政府提案"


class MeetingType(str, Enum):
    """會議類型枚舉"""
    PLENARY = "院會"
    COMMITTEE = "委員會"


class Bill(BaseModel):
    """議案資料模型"""
    bill_no: str | None = Field(None, alias="議案編號", description="議案編號")
    title: str | None = Field(None, alias="議案名稱", description="議案標題")
    category: str | None = Field(None, alias="議案類別", description="議案類別")
    term: int | None = Field(None, alias="屆", description="屆期")
    session: int | None = Field(None, alias="會期", description="會期")
    proposer: str | list[str] | None = Field(None, alias="提案人", description="提案人")
    cosigner: str | list[str] | None = Field(None, alias="連署人", description="連署人")
    proposal_date: str | None = Field(None, alias="提案日期", description="提案日期")
    proposal_source: str | None = Field(None, alias="提案來源", description="提案來源")
    status: str | None = Field(None, alias="議案狀態", description="議案狀態")
    latest_progress_date: str | None = Field(None, alias="最新進度日期", description="最新進度日期")

    class Config:
        populate_by_name = True


class BillDetail(Bill):
    """議案詳細資料模型"""
    law_numbers: list[str] | None = Field(None, alias="法律編號:str", description="相關法律編號")
    bill_process: list[dict] | None = Field(None, alias="議案流程", description="議案流程")
    related_attachments: list[dict] | None = Field(None, alias="相關附件", description="相關附件")


class RelatedBill(BaseModel):
    """相關議案模型"""
    relation_type: str | None = Field(None, alias="關聯類型", description="關聯類型")
    related_bill_no: str | None = Field(None, alias="相關議案編號", description="相關議案編號")

    class Config:
        populate_by_name = True


class Meeting(BaseModel):
    """會議資料模型"""
    meeting_date: str | None = Field(None, alias="會議日期", description="會議日期")
    meeting_type: str | None = Field(None, alias="會議種類", description="會議種類")
    meeting_name: str | None = Field(None, alias="會議名稱", description="會議名稱")
    agenda_item: str | None = Field(None, alias="議程項目", description="議程項目")
    discussion_result: str | None = Field(None, alias="審議結果", description="審議結果")

    class Config:
        populate_by_name = True


class SearchBillsResponse(BaseModel):
    """搜尋議案回應模型"""
    bills: list[Bill] = Field(default_factory=list, description="議案列表")
    total: int | None = Field(None, description="總筆數")
    page: int = Field(description="目前頁數")
    limit: int = Field(description="每頁筆數")

    class Config:
        populate_by_name = True


class BillRelatedBillsResponse(BaseModel):
    """相關議案回應模型"""
    related_bills: list[RelatedBill] = Field(default_factory=list, description="相關議案列表")
    total: int | None = Field(None, description="總筆數")
    page: int = Field(description="目前頁數")
    limit: int = Field(description="每頁筆數")
    bill_no: str = Field(description="查詢的議案編號")

    class Config:
        populate_by_name = True


class BillMeetsResponse(BaseModel):
    """議案會議回應模型"""
    meetings: list[Meeting] = Field(default_factory=list, description="會議列表")
    total: int | None = Field(None, description="總筆數")
    page: int = Field(description="目前頁數")
    limit: int = Field(description="每頁筆數")
    bill_no: str = Field(description="查詢的議案編號")

    class Config:
        populate_by_name = True


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


class SearchBillsRequest(BaseModel):
    """搜尋議案請求模型"""
    term: int | None = None
    session: int | None = None
    bill_category: str | None = None
    proposer: str | None = None
    cosigner: str | None = None
    bill_status: str | None = None
    proposal_source: str | None = None
    bill_no: str | None = None
    proposal_date_start: str | None = None
    proposal_date_end: str | None = None
    page: int = 1
    limit: int = 20

    def do(self) -> SearchBillsResponse:
        """同步執行搜尋議案請求"""
        try:
            resp = httpx.get(
                url="https://ly.govapi.tw/v2/bills",
                params=self._build_params(),
                timeout=30.0
            )
            resp.raise_for_status()

            data = resp.json()
            if isinstance(data, dict) and "data" in data:
                bills_data = data["data"]
            else:
                bills_data = data if isinstance(data, list) else []

            bills = [Bill.model_validate(bill_data) for bill_data in bills_data]

            return SearchBillsResponse(
                bills=bills,
                total=len(bills),
                page=self.page,
                limit=self.limit
            )
        except httpx.HTTPStatusError as e:
            raise httpx.HTTPStatusError(
                f"API 請求失敗：HTTP {e.response.status_code}",
                request=e.request,
                response=e.response
            )
        except Exception as e:
            raise RuntimeError(f"未預期的錯誤：{str(e)}") from e

    async def async_do(self) -> SearchBillsResponse:
        """非同步執行搜尋議案請求"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.get(
                    url="https://ly.govapi.tw/v2/bills",
                    params=self._build_params(),
                )
                resp.raise_for_status()

                data = resp.json()
                if isinstance(data, dict) and "data" in data:
                    bills_data = data["data"]
                else:
                    bills_data = data if isinstance(data, list) else []

                bills = [Bill.model_validate(bill_data) for bill_data in bills_data]

                return SearchBillsResponse(
                    bills=bills,
                    total=len(bills),
                    page=self.page,
                    limit=self.limit
                )
        except httpx.HTTPStatusError as e:
            raise httpx.HTTPStatusError(
                f"API 請求失敗：HTTP {e.response.status_code}",
                request=e.request,
                response=e.response
            )
        except Exception as e:
            raise RuntimeError(f"未預期的錯誤：{str(e)}") from e

    def _build_params(self) -> dict[str, Any]:
        """建構請求參數"""
        params = {}
        for field_name, field_value in self.model_dump().items():
            if field_value is not None:
                params[field_name] = field_value
        return params


class GetBillDetailRequest(BaseModel):
    """取得議案詳細資料請求模型"""
    bill_no: str

    def do(self) -> BillDetail:
        """同步執行取得議案詳細資料請求"""
        try:
            resp = httpx.get(
                url=f"https://ly.govapi.tw/v2/bills/{self.bill_no}",
                timeout=30.0
            )
            resp.raise_for_status()

            data = resp.json()
            # 如果 API 回傳的是包裝格式，提取 data 欄位
            if isinstance(data, dict) and "data" in data:
                data = data["data"]

            return BillDetail.model_validate(data)
        except httpx.HTTPStatusError as e:
            raise httpx.HTTPStatusError(
                f"API 請求失敗：HTTP {e.response.status_code}",
                request=e.request,
                response=e.response
            )
        except Exception as e:
            raise RuntimeError(f"未預期的錯誤：{str(e)}") from e

    async def async_do(self) -> BillDetail:
        """非同步執行取得議案詳細資料請求"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.get(
                    url=f"https://ly.govapi.tw/v2/bills/{self.bill_no}",
                )
                resp.raise_for_status()

                data = resp.json()
                # 如果 API 回傳的是包裝格式，提取 data 欄位
                if isinstance(data, dict) and "data" in data:
                    data = data["data"]

                return BillDetail.model_validate(data)
        except httpx.HTTPStatusError as e:
            raise httpx.HTTPStatusError(
                f"API 請求失敗：HTTP {e.response.status_code}",
                request=e.request,
                response=e.response
            )
        except Exception as e:
            raise RuntimeError(f"未預期的錯誤：{str(e)}") from e


class GetBillRelatedBillsRequest(BaseModel):
    """取得相關議案請求模型"""
    bill_no: str
    page: int = 1
    limit: int = 20

    def do(self) -> BillRelatedBillsResponse:
        """同步執行取得相關議案請求"""
        try:
            resp = httpx.get(
                url=f"https://ly.govapi.tw/v2/bills/{self.bill_no}/related",
                params={"page": self.page, "limit": self.limit},
                timeout=30.0
            )
            resp.raise_for_status()

            data = resp.json()
            if isinstance(data, dict) and "data" in data:
                related_data = data["data"]
            else:
                related_data = data if isinstance(data, list) else []

            related_bills = [RelatedBill.model_validate(item) for item in related_data]

            return BillRelatedBillsResponse(
                related_bills=related_bills,
                total=len(related_bills),
                page=self.page,
                limit=self.limit,
                bill_no=self.bill_no
            )
        except httpx.HTTPStatusError as e:
            raise httpx.HTTPStatusError(
                f"API 請求失敗：HTTP {e.response.status_code}",
                request=e.request,
                response=e.response
            )
        except Exception as e:
            raise RuntimeError(f"未預期的錯誤：{str(e)}") from e

    async def async_do(self) -> BillRelatedBillsResponse:
        """非同步執行取得相關議案請求"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.get(
                    url=f"https://ly.govapi.tw/v2/bills/{self.bill_no}/related",
                    params={"page": self.page, "limit": self.limit},
                )
                resp.raise_for_status()

                data = resp.json()
                if isinstance(data, dict) and "data" in data:
                    related_data = data["data"]
                else:
                    related_data = data if isinstance(data, list) else []

                related_bills = [RelatedBill.model_validate(item) for item in related_data]

                return BillRelatedBillsResponse(
                    related_bills=related_bills,
                    total=len(related_bills),
                    page=self.page,
                    limit=self.limit,
                    bill_no=self.bill_no
                )
        except httpx.HTTPStatusError as e:
            raise httpx.HTTPStatusError(
                f"API 請求失敗：HTTP {e.response.status_code}",
                request=e.request,
                response=e.response
            )
        except Exception as e:
            raise RuntimeError(f"未預期的錯誤：{str(e)}") from e


class GetBillMeetsRequest(BaseModel):
    """取得議案會議請求模型"""
    bill_no: str
    term: int | None = None
    session: int | None = None
    meeting_type: str | None = None
    date: str | None = None
    page: int = 1
    limit: int = 20

    def do(self) -> BillMeetsResponse:
        """同步執行取得議案會議請求"""
        try:
            params: dict[str, Any] = {"page": self.page, "limit": self.limit}
            if self.term is not None:
                params["term"] = str(self.term)
            if self.session is not None:
                params["session"] = str(self.session)
            if self.meeting_type is not None:
                params["meeting_type"] = self.meeting_type
            if self.date is not None:
                params["date"] = self.date

            resp = httpx.get(
                url=f"https://ly.govapi.tw/v2/bills/{self.bill_no}/meets",
                params=params,
                timeout=30.0
            )
            resp.raise_for_status()

            data = resp.json()
            if isinstance(data, dict) and "data" in data:
                meets_data = data["data"]
            else:
                meets_data = data if isinstance(data, list) else []

            meetings = [Meeting.model_validate(meet) for meet in meets_data]

            return BillMeetsResponse(
                meetings=meetings,
                total=len(meetings),
                page=self.page,
                limit=self.limit,
                bill_no=self.bill_no
            )
        except httpx.HTTPStatusError as e:
            raise httpx.HTTPStatusError(
                f"API 請求失敗：HTTP {e.response.status_code}",
                request=e.request,
                response=e.response
            )
        except Exception as e:
            raise RuntimeError(f"未預期的錯誤：{str(e)}") from e

    async def async_do(self) -> BillMeetsResponse:
        """非同步執行取得議案會議請求"""
        try:
            params: dict[str, Any] = {"page": self.page, "limit": self.limit}
            if self.term is not None:
                params["term"] = str(self.term)
            if self.session is not None:
                params["session"] = str(self.session)
            if self.meeting_type is not None:
                params["meeting_type"] = self.meeting_type
            if self.date is not None:
                params["date"] = self.date

            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.get(
                    url=f"https://ly.govapi.tw/v2/bills/{self.bill_no}/meets",
                    params=params,
                )
                resp.raise_for_status()

                data = resp.json()
                if isinstance(data, dict) and "data" in data:
                    meets_data = data["data"]
                else:
                    meets_data = data if isinstance(data, list) else []

                meetings = [Meeting.model_validate(meet) for meet in meets_data]

                return BillMeetsResponse(
                    meetings=meetings,
                    total=len(meetings),
                    page=self.page,
                    limit=self.limit,
                    bill_no=self.bill_no
                )
        except httpx.HTTPStatusError as e:
            raise httpx.HTTPStatusError(
                f"API 請求失敗：HTTP {e.response.status_code}",
                request=e.request,
                response=e.response
            )
        except Exception as e:
            raise RuntimeError(f"未預期的錯誤：{str(e)}") from e


# 快取功能的便利函數
@cache
def search_bills_cached(
    term: int | None = None,
    session: int | None = None,
    bill_category: str | None = None,
    proposer: str | None = None,
    page: int = 1,
    limit: int = 20
) -> SearchBillsResponse:
    """快取版本的議案搜尋"""
    request = SearchBillsRequest(
        term=term,
        session=session,
        bill_category=bill_category,
        proposer=proposer,
        page=page,
        limit=limit
    )
    return request.do()


@cache
def get_bill_detail_cached(bill_no: str) -> BillDetail:
    """快取版本的議案詳細資料取得"""
    request = GetBillDetailRequest(bill_no=bill_no)
    return request.do()
