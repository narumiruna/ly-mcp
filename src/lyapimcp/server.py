from typing import Annotated
from typing import Any
from typing import Dict

import httpx
from mcp.server.fastmcp import FastMCP
from pydantic import Field

# https://github.com/jlowin/fastmcp/issues/81#issuecomment-2714245145
mcp = FastMCP("立法院 API v2 MCP Server", log_level="ERROR")

BASE_URL = "https://ly.govapi.tw/v2"


@mcp.tool()
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
) -> str:
    """搜尋立法院議案列表。可依據屆期、會期、議案類別、提案人等條件進行篩選。"""

    params: Dict[str, Any] = {"page": page, "limit": limit}

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

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{BASE_URL}/bills", params=params)
            response.raise_for_status()
            return response.text
        except httpx.HTTPError as e:
            return f"Error fetching bills: {e}"


@mcp.tool()
async def get_bill_detail(
    bill_no: Annotated[str, Field(description="議案編號，例: 203110077970000")]
) -> str:
    """取得特定議案的詳細資訊。"""

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{BASE_URL}/bills/{bill_no}")
            response.raise_for_status()
            return response.text
        except httpx.HTTPError as e:
            return f"Error fetching bill detail: {e}"


@mcp.tool()
async def get_bill_related_bills(
    bill_no: Annotated[str, Field(description="議案編號，例: 203110077970000")]
) -> str:
    """取得特定議案的相關議案列表。"""

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{BASE_URL}/bills/{bill_no}/related_bills")
            response.raise_for_status()
            return response.text
        except httpx.HTTPError as e:
            return f"Error fetching related bills: {e}"


@mcp.tool()
async def get_bill_doc_html(
    bill_no: Annotated[str, Field(description="議案編號，例: 203110077970000")]
) -> str:
    """取得特定議案的文件 HTML 內容列表。"""

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{BASE_URL}/bills/{bill_no}/doc_html")
            response.raise_for_status()
            return response.text
        except httpx.HTTPError as e:
            return f"Error fetching bill document HTML: {e}"


@mcp.tool()
async def get_bill_meets(
    bill_no: Annotated[str, Field(description="議案編號，例: 203110077970000")],
    term: Annotated[int | None, Field(description="屆，例: 11")] = None,
    session: Annotated[int | None, Field(description="會期，例: 2")] = None,
    meeting_type: Annotated[str | None, Field(description="會議種類，例: 院會")] = None,
    date: Annotated[str | None, Field(description="日期，例: 2024-10-25")] = None,
    page: Annotated[int, Field(description="頁數")] = 1,
    limit: Annotated[int, Field(description="每頁筆數")] = 20,
) -> str:
    """取得特定議案的相關會議列表。"""

    params: Dict[str, Any] = {"page": page, "limit": limit}

    if term is not None:
        params["屆"] = term
    if session is not None:
        params["會期"] = session
    if meeting_type:
        params["會議種類"] = meeting_type
    if date:
        params["日期"] = date

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{BASE_URL}/bills/{bill_no}/meets", params=params)
            response.raise_for_status()
            return response.text
        except httpx.HTTPError as e:
            return f"Error fetching bill meetings: {e}"


@mcp.tool()
def add_numbers(
    a: Annotated[float, Field(description="The first number")],
    b: Annotated[float, Field(description="The second number")],
) -> str:
    """Add two numbers and return the result as a string."""
    return str(a + b)


def main():
    mcp.run()
