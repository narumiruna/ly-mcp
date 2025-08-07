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
            "list_bills",
            "get_bill_detail",
            "get_bill_related_bills",
            "get_bill_meets",
            "get_bill_doc_html",
        ]
        for tool_name in expected_bills_tools:
            assert tool_name in tool_names


@pytest.mark.asyncio
async def test_list_bills(server_params: StdioServerParameters) -> None:
    async with stdio_client(server_params) as (read, write), ClientSession(read, write) as session:
        await session.initialize()

        # Test basic search with pagination
        result = await session.call_tool("list_bills", {"page": 1, "limit": 5})

        assert len(result.content) == 1
        assert isinstance(result.content[0], TextContent)

        # Check response is string
        response_text = result.content[0].text
        assert isinstance(response_text, str)


@pytest.mark.asyncio
async def test_list_bills_with_filters(server_params: StdioServerParameters) -> None:
    async with stdio_client(server_params) as (read, write), ClientSession(read, write) as session:
        await session.initialize()

        # Test search with specific filters
        result = await session.call_tool("list_bills", {"term": 11, "bill_type": "法律案", "limit": 3})

        assert len(result.content) == 1
        assert isinstance(result.content[0], TextContent)

        # Check response is string
        response_text = result.content[0].text
        assert isinstance(response_text, str)


@pytest.mark.asyncio
async def test_list_bills_json(server_params: StdioServerParameters) -> None:
    async with stdio_client(server_params) as (read, write), ClientSession(read, write) as session:
        await session.initialize()

        # Test JSON response format
        result = await session.call_tool("search_bills", {"term": 11, "limit": 3})

        assert len(result.content) == 1
        assert isinstance(result.content[0], TextContent)

        response_text = result.content[0].text
        assert isinstance(response_text, str)

@pytest.mark.asyncio
async def test_get_bill_detail_error_handling(server_params: StdioServerParameters) -> None:
    async with stdio_client(server_params) as (read, write), ClientSession(read, write) as session:
        await session.initialize()

        # Test with invalid bill number to check error handling
        result = await session.call_tool("get_bill_detail", {"bill_no": "invalid_bill_number"})

        assert len(result.content) == 1
        assert isinstance(result.content[0], TextContent)

        # Should contain string response
        response_text = result.content[0].text
        assert isinstance(response_text, str)


@pytest.mark.asyncio
async def test_get_bill_detail_json(server_params: StdioServerParameters) -> None:
    async with stdio_client(server_params) as (read, write), ClientSession(read, write) as session:
        await session.initialize()

        # Test JSON response with a known bill
        result = await session.call_tool("get_bill_detail", {"bill_no": "203110077970000"})

        assert len(result.content) == 1
        assert isinstance(result.content[0], TextContent)

        response_text = result.content[0].text
        # Should be string
        assert isinstance(response_text, str)


@pytest.mark.asyncio
async def test_get_bill_related_bills(server_params: StdioServerParameters) -> None:
    async with stdio_client(server_params) as (read, write), ClientSession(read, write) as session:
        await session.initialize()

        # Test related bills with a known bill
        result = await session.call_tool("get_bill_related_bills", {"bill_no": "203110077970000"})

        assert len(result.content) == 1
        assert isinstance(result.content[0], TextContent)

        response_text = result.content[0].text
        # Should be string
        assert isinstance(response_text, str)
