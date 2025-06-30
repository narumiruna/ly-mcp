import json
from typing import Any

import httpx
from loguru import logger

from .models import APIResponse

BASE_URL = "https://ly.govapi.tw/v2"


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
