import json

import pytest
from mcp import ClientSession
from mcp import StdioServerParameters
from mcp import stdio_client
from mcp.types import TextContent


@pytest.fixture
def server_params() -> StdioServerParameters:
    return StdioServerParameters(command="uv", args=["run", "mcpservertemplate"])


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
            "get_bill_meets"
        ]
        for tool_name in expected_bills_tools:
            assert tool_name in tool_names


@pytest.mark.asyncio
async def test_call_tool(server_params: StdioServerParameters) -> None:
    async with stdio_client(server_params) as (read, write), ClientSession(read, write) as session:
        await session.initialize()

        a = 1234
        b = 5678
        result = await session.call_tool("add_numbers", {"a": a, "b": b})

        assert len(result.content) == 1
        assert isinstance(result.content[0], TextContent)
        assert float(result.content[0].text) == a + b


@pytest.mark.asyncio
async def test_search_bills(server_params: StdioServerParameters) -> None:
    async with stdio_client(server_params) as (read, write), ClientSession(read, write) as session:
        await session.initialize()

        # Test basic search with pagination
        result = await session.call_tool("search_bills", {
            "page": 1,
            "limit": 5
        })

        assert len(result.content) == 1
        assert isinstance(result.content[0], TextContent)

        # Parse JSON response to verify structure
        response_data = json.loads(result.content[0].text)
        assert "total" in response_data
        assert "page" in response_data
        assert "limit" in response_data
        assert isinstance(response_data.get("total"), int)


@pytest.mark.asyncio
async def test_search_bills_with_filters(server_params: StdioServerParameters) -> None:
    async with stdio_client(server_params) as (read, write), ClientSession(read, write) as session:
        await session.initialize()

        # Test search with specific filters
        result = await session.call_tool("search_bills", {
            "term": 11,
            "bill_category": "法律案",
            "limit": 3
        })

        assert len(result.content) == 1
        assert isinstance(result.content[0], TextContent)

        # Verify we get valid JSON response
        response_data = json.loads(result.content[0].text)
        assert "total" in response_data


@pytest.mark.asyncio
async def test_get_bill_detail_error_handling(server_params: StdioServerParameters) -> None:
    async with stdio_client(server_params) as (read, write), ClientSession(read, write) as session:
        await session.initialize()

        # Test with invalid bill number to check error handling
        result = await session.call_tool("get_bill_detail", {
            "bill_no": "invalid_bill_number"
        })

        assert len(result.content) == 1
        assert isinstance(result.content[0], TextContent)

        # Should contain error message
        response_text = result.content[0].text
        assert "Error fetching bill detail" in response_text or "error" in response_text.lower()
