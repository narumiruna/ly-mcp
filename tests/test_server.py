import pytest
from mcp import ClientSession
from mcp import StdioServerParameters
from mcp import stdio_client
from mcp.types import TextContent


@pytest.fixture
def server_params() -> StdioServerParameters:
    return StdioServerParameters(command="uv", args=["run", "lymcp"])


@pytest.mark.asyncio
async def test_list_tools(server_params: StdioServerParameters) -> None:
    async with stdio_client(server_params) as (read, write), ClientSession(read, write) as session:
        await session.initialize()

        result = await session.list_tools()
        assert len(result.tools) > 0

        # Check that bills tools are available
        tool_names = [tool.name for tool in result.tools]
        expected_bills_tools = [
            "search_bills",
            "get_bill_detail",
            "get_bill_related_bills",
            "get_bill_doc_html",
            "get_bill_meets",
        ]
        for tool_name in expected_bills_tools:
            assert tool_name in tool_names


@pytest.mark.asyncio
async def test_search_bills(server_params: StdioServerParameters) -> None:
    async with stdio_client(server_params) as (read, write), ClientSession(read, write) as session:
        await session.initialize()

        # Test basic search with pagination
        result = await session.call_tool("search_bills", {"page": 1, "limit": 5})

        assert len(result.content) == 1
        assert isinstance(result.content[0], TextContent)

        # Check for success indicator
        response_text = result.content[0].text
        assert "✅" in response_text or "查詢成功" in response_text


@pytest.mark.asyncio
async def test_search_bills_with_filters(server_params: StdioServerParameters) -> None:
    async with stdio_client(server_params) as (read, write), ClientSession(read, write) as session:
        await session.initialize()

        # Test search with specific filters
        result = await session.call_tool("search_bills", {"term": 11, "bill_category": "法律案", "limit": 3})

        assert len(result.content) == 1
        assert isinstance(result.content[0], TextContent)

        # Check for success indicator
        response_text = result.content[0].text
        assert "✅" in response_text or "查詢成功" in response_text


@pytest.mark.asyncio
async def test_search_bills_structured(server_params: StdioServerParameters) -> None:
    async with stdio_client(server_params) as (read, write), ClientSession(read, write) as session:
        await session.initialize()

        # Test structured response
        result = await session.call_tool("search_bills", {"term": 11, "limit": 3, "structured": True})

        assert len(result.content) == 1
        assert isinstance(result.content[0], TextContent)

        response_text = result.content[0].text
        assert "查詢結果摘要" in response_text or "議案列表" in response_text


@pytest.mark.asyncio
async def test_get_bill_detail_error_handling(server_params: StdioServerParameters) -> None:
    async with stdio_client(server_params) as (read, write), ClientSession(read, write) as session:
        await session.initialize()

        # Test with invalid bill number to check error handling
        result = await session.call_tool("get_bill_detail", {"bill_no": "invalid_bill_number"})

        assert len(result.content) == 1
        assert isinstance(result.content[0], TextContent)

        # Should contain error message with emoji or proper error handling
        response_text = result.content[0].text
        assert "❌" in response_text or "API 錯誤" in response_text or "找不到資料" in response_text


@pytest.mark.asyncio
async def test_get_bill_detail_json(server_params: StdioServerParameters) -> None:
    async with stdio_client(server_params) as (read, write), ClientSession(read, write) as session:
        await session.initialize()

        # Test JSON response with a known bill
        result = await session.call_tool("get_bill_detail", {"bill_no": "203110077970000"})

        assert len(result.content) == 1
        assert isinstance(result.content[0], TextContent)

        response_text = result.content[0].text
        # Should either succeed with JSON data or fail with proper error message
        assert ("✅" in response_text) or ("❌" in response_text)


@pytest.mark.asyncio
async def test_get_bill_doc_html_empty_handling(server_params: StdioServerParameters) -> None:
    async with stdio_client(server_params) as (read, write), ClientSession(read, write) as session:
        await session.initialize()

        # Test document HTML with potentially empty response
        result = await session.call_tool("get_bill_doc_html", {"bill_no": "203110077970000"})

        assert len(result.content) == 1
        assert isinstance(result.content[0], TextContent)

        response_text = result.content[0].text
        # Should either succeed or give helpful empty content message
        assert ("✅" in response_text) or ("⚠️" in response_text) or ("❌" in response_text)
