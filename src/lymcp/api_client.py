from __future__ import annotations

from typing import Any

import httpx
from loguru import logger

from .models import APIResponse  # type: ignore[attr-defined]
from .models import GetBillDetailRequest
from .models import GetBillMeetsRequest
from .models import GetBillRelatedBillsRequest
from .models import SearchBillsRequest

BASE_URL = "https://ly.govapi.tw/v2"


class LegislativeYuanAPIClient:
    """立法院 API 客戶端"""

    def __init__(self, base_url: str = BASE_URL, timeout: float = 30.0):
        self.base_url = base_url
        self.timeout = timeout

    async def search_bills(
        self,
        term: int | None = None,
        session: int | None = None,
        bill_category: str | None = None,
        proposer: str | None = None,
        cosigner: str | None = None,
        bill_status: str | None = None,
        proposal_source: str | None = None,
        bill_no: str | None = None,
        proposal_date_start: str | None = None,
        proposal_date_end: str | None = None,
        page: int = 1,
        limit: int = 20,
    ) -> APIResponse:
        """搜尋議案"""
        try:
            request = SearchBillsRequest(
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

            search_response = await request.async_do()

            # 將 SearchBillsResponse 轉換為 APIResponse 以保持向後相容性
            bills_data = [bill.model_dump(by_alias=True) for bill in search_response.bills]

            return APIResponse(
                success=True,
                message="查詢成功",
                data=bills_data,
                total=search_response.total,
                page=search_response.page,
                limit=search_response.limit,
            )

        except Exception as e:
            logger.error(f"Error in search_bills: {e}")
            return APIResponse(
                success=False,
                message=f"API 請求失敗：{str(e)}",
                data=None,
            )

    async def get_bill_detail(self, bill_no: str) -> APIResponse:
        """取得議案詳細資料"""
        try:
            request = GetBillDetailRequest(bill_no=bill_no)
            bill_detail = await request.async_do()

            # 將 Pydantic 模型轉換為字典格式以保持向後相容性
            bill_data = bill_detail.model_dump(by_alias=True)

            return APIResponse(
                success=True,
                message="查詢成功",
                data=bill_data,
            )

        except Exception as e:
            logger.error(f"Error in get_bill_detail: {e}")
            return APIResponse(
                success=False,
                message=f"API 請求失敗：{str(e)}",
                data=None,
            )

    async def get_bill_related_bills(
        self, bill_no: str, page: int = 1, limit: int = 20
    ) -> APIResponse:
        """取得相關議案"""
        try:
            request = GetBillRelatedBillsRequest(
                bill_no=bill_no, page=page, limit=limit
            )
            related_response = await request.async_do()

            # 將 BillRelatedBillsResponse 轉換為 APIResponse 以保持向後相容性
            related_data = [bill.model_dump(by_alias=True) for bill in related_response.related_bills]

            return APIResponse(
                success=True,
                message="查詢成功",
                data=related_data,
                total=related_response.total,
                page=related_response.page,
                limit=related_response.limit,
            )

        except httpx.HTTPStatusError as e:
            return self._handle_http_error(e)
        except httpx.TimeoutException:
            return APIResponse(
                success=False,
                message="請求逾時。API 服務可能繁忙，請稍後再試。",
                data=None,
            )
        except httpx.ConnectError:
            return APIResponse(
                success=False,
                message="連線錯誤。請檢查網路連線或 API 服務是否正常。",
                data=None,
            )
        except Exception as e:
            logger.error(f"Unexpected error in get_bill_related_bills: {e}")
            return APIResponse(
                success=False,
                message=f"未預期的錯誤：{str(e)}",
                data=None,
            )

    async def get_bill_meets(
        self,
        bill_no: str,
        term: int | None = None,
        session: int | None = None,
        meeting_type: str | None = None,
        date: str | None = None,
        page: int = 1,
        limit: int = 20,
    ) -> APIResponse:
        """取得議案會議"""
        try:
            request = GetBillMeetsRequest(
                bill_no=bill_no,
                term=term,
                session=session,
                meeting_type=meeting_type,
                date=date,
                page=page,
                limit=limit,
            )
            meets_response = await request.async_do()

            # 將 BillMeetsResponse 轉換為 APIResponse 以保持向後相容性
            meets_data = [meeting.model_dump(by_alias=True) for meeting in meets_response.meetings]

            return APIResponse(
                success=True,
                message="查詢成功",
                data=meets_data,
                total=meets_response.total,
                page=meets_response.page,
                limit=meets_response.limit,
            )

        except httpx.HTTPStatusError as e:
            return self._handle_http_error(e)
        except httpx.TimeoutException:
            return APIResponse(
                success=False,
                message="請求逾時。API 服務可能繁忙，請稍後再試。",
                data=None,
            )
        except httpx.ConnectError:
            return APIResponse(
                success=False,
                message="連線錯誤。請檢查網路連線或 API 服務是否正常。",
                data=None,
            )
        except Exception as e:
            logger.error(f"Unexpected error in get_bill_meets: {e}")
            return APIResponse(
                success=False,
                message=f"未預期的錯誤：{str(e)}",
                data=None,
            )

    def _handle_http_error(self, error: httpx.HTTPStatusError) -> APIResponse:
        """處理 HTTP 錯誤"""
        status_code = error.response.status_code

        if status_code == 404:
            message = "查無資料：所查詢的資源不存在 (404)。請檢查參數是否正確。"
        elif status_code == 429:
            message = "請求過於頻繁 (429)。請稍後再試。"
        elif status_code == 500:
            message = "伺服器內部錯誤 (500)。API 服務可能暫時不可用。"
        else:
            message = f"API 請求失敗：HTTP {status_code}"

        logger.error(f"HTTP error {status_code}: {message}")

        return APIResponse(
            success=False,
            message=message,
            data=None,
        )


# 建立單例客戶端實例
api_client = LegislativeYuanAPIClient()


# 向後相容性的函數包裝器
async def make_api_request(
    endpoint: str, params: dict[str, Any] | None = None, description: str = "API request"
) -> APIResponse:
    """向後相容性的 API 請求函數"""
    logger.info(f"Making {description} request to {endpoint} with params: {params}")

    if endpoint == "/bills":
        # 處理搜尋議案請求
        search_params = params or {}
        return await api_client.search_bills(**search_params)

    elif endpoint.startswith("/bills/") and endpoint.endswith("/related"):
        # 處理相關議案請求
        bill_no = endpoint.split("/")[2]
        related_params = params or {}
        return await api_client.get_bill_related_bills(
            bill_no=bill_no,
            page=related_params.get("page", 1),
            limit=related_params.get("limit", 20),
        )

    elif endpoint.startswith("/bills/") and endpoint.endswith("/meets"):
        # 處理會議請求
        bill_no = endpoint.split("/")[2]
        meets_params = params or {}
        return await api_client.get_bill_meets(
            bill_no=bill_no,
            **meets_params,
        )

    elif endpoint.startswith("/bills/") and "/" not in endpoint[7:]:
        # 處理單一議案詳細資料請求
        bill_no = endpoint.split("/")[2]
        return await api_client.get_bill_detail(bill_no=bill_no)

    else:
        # 不支援的 endpoint
        return APIResponse(
            success=False,
            message=f"不支援的 API endpoint: {endpoint}",
            data=None,
        )
