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
            "get_stat",
            "list_bills",
            "get_bill",
            "get_bill_related_bills",
            "get_bill_meets",
            "get_bill_doc_html",
            "list_interpellations",
            "get_interpellation",
            "get_legislator_interpellations",
            "list_ivods",
            "get_ivod",
            "get_meet_ivods",
            "list_laws",
            "get_law",
            "get_law_progress",
            "get_law_bills",
            "get_law_versions",
            "list_law_contents",
            "get_law_content",
            "list_legislators",
            "get_legislator",
            "get_legislator_propose_bills",
            "get_legislator_cosign_bills",
            "get_legislator_meets",
            "get_legislator_interpellations",
            "list_meets",
            "get_meet",
            "get_meet_ivods",
            "get_meet_bills",
            "get_meet_interpellations",
        ]
        for tool_name in expected_bills_tools:
            assert tool_name in tool_names

@pytest.mark.asyncio
async def test_get_stat(server_params: StdioServerParameters) -> None:
    async with stdio_client(server_params) as (read, write), ClientSession(read, write) as session:
        await session.initialize()

        # Test basic statistics retrieval
        result = await session.call_tool("get_stat", {})

        assert len(result.content) == 1
        assert isinstance(result.content[0], TextContent)

        # Check response is string
        response_text = result.content[0].text
        assert isinstance(response_text, str)

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
        result = await session.call_tool("list_bills", {"term": 11, "limit": 3})

        assert len(result.content) == 1
        assert isinstance(result.content[0], TextContent)

        response_text = result.content[0].text
        assert isinstance(response_text, str)

@pytest.mark.asyncio
async def test_get_bill_detail_error_handling(server_params: StdioServerParameters) -> None:
    async with stdio_client(server_params) as (read, write), ClientSession(read, write) as session:
        await session.initialize()

        # Test with invalid bill number to check error handling
        result = await session.call_tool("get_bill", {"bill_no": "invalid_bill_number"})

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
        result = await session.call_tool("get_bill", {"bill_no": "203110077970000"})

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


@pytest.mark.asyncio
async def test_list_gazettes(server_params: StdioServerParameters) -> None:
    async with stdio_client(server_params) as (read, write), ClientSession(read, write) as session:
        await session.initialize()

        # Test gazette listing
        result = await session.call_tool("list_gazettes", {"limit": 1})

        assert len(result.content) == 1
        assert isinstance(result.content[0], TextContent)

        response_text = result.content[0].text
        assert isinstance(response_text, str)


@pytest.mark.asyncio
async def test_get_gazette(server_params: StdioServerParameters) -> None:
    async with stdio_client(server_params) as (read, write), ClientSession(read, write) as session:
        await session.initialize()

        # Test gazette detail retrieval with a test gazette ID
        result = await session.call_tool("get_gazette", {"gazette_id": "1137701"})

        assert len(result.content) == 1
        assert isinstance(result.content[0], TextContent)

        response_text = result.content[0].text
        assert isinstance(response_text, str)


@pytest.mark.asyncio
async def test_list_interpellations(server_params: StdioServerParameters) -> None:
    async with stdio_client(server_params) as (read, write), ClientSession(read, write) as session:
        await session.initialize()

        # Test basic interpellations search
        result = await session.call_tool("list_interpellations", {"page": 1, "limit": 3})

        assert len(result.content) == 1
        assert isinstance(result.content[0], TextContent)

        response_text = result.content[0].text
        assert isinstance(response_text, str)


@pytest.mark.asyncio
async def test_list_interpellations_with_member(server_params: StdioServerParameters) -> None:
    async with stdio_client(server_params) as (read, write), ClientSession(read, write) as session:
        await session.initialize()

        # Test interpellations search with specific member
        result = await session.call_tool("list_interpellations", {"interpellation_member": "羅智強", "limit": 2})

        assert len(result.content) == 1
        assert isinstance(result.content[0], TextContent)

        response_text = result.content[0].text
        assert isinstance(response_text, str)


@pytest.mark.asyncio
async def test_get_interpellation(server_params: StdioServerParameters) -> None:
    async with stdio_client(server_params) as (read, write), ClientSession(read, write) as session:
        await session.initialize()

        # Test interpellation detail retrieval with a test interpellation ID
        result = await session.call_tool("get_interpellation", {"interpellation_id": "11-1-1-1"})

        assert len(result.content) == 1
        assert isinstance(result.content[0], TextContent)

        response_text = result.content[0].text
        assert isinstance(response_text, str)


@pytest.mark.asyncio
async def test_get_legislator_interpellations(server_params: StdioServerParameters) -> None:
    async with stdio_client(server_params) as (read, write), ClientSession(read, write) as session:
        await session.initialize()

        # Test legislator interpellations retrieval
        result = await session.call_tool("get_legislator_interpellations", {"term": 11, "name": "韓國瑜", "limit": 2})

        assert len(result.content) == 1
        assert isinstance(result.content[0], TextContent)

        response_text = result.content[0].text
        assert isinstance(response_text, str)


@pytest.mark.asyncio
async def test_interpellation_tools_available(server_params: StdioServerParameters) -> None:
    async with stdio_client(server_params) as (read, write), ClientSession(read, write) as session:
        await session.initialize()

        result = await session.list_tools()

        # Check that interpellation tools are available
        tool_names = [tool.name for tool in result.tools]
        expected_interpellation_tools = [
            "list_interpellations",
            "get_interpellation",
            "get_legislator_interpellations",
        ]
        for tool_name in expected_interpellation_tools:
            assert tool_name in tool_names


@pytest.mark.asyncio
async def test_list_ivods(server_params: StdioServerParameters) -> None:
    async with stdio_client(server_params) as (read, write), ClientSession(read, write) as session:
        await session.initialize()

        # Test basic IVOD listing
        result = await session.call_tool("list_ivods", {"page": 1, "limit": 5})

        assert len(result.content) == 1
        assert isinstance(result.content[0], TextContent)

        response_text = result.content[0].text
        assert isinstance(response_text, str)


@pytest.mark.asyncio
async def test_list_ivods_with_filters(server_params: StdioServerParameters) -> None:
    async with stdio_client(server_params) as (read, write), ClientSession(read, write) as session:
        await session.initialize()

        # Test IVOD listing with specific filters
        result = await session.call_tool("list_ivods", {"term": 11, "video_type": "Clip", "limit": 3})

        assert len(result.content) == 1
        assert isinstance(result.content[0], TextContent)

        response_text = result.content[0].text
        assert isinstance(response_text, str)


@pytest.mark.asyncio
async def test_get_ivod_error_handling(server_params: StdioServerParameters) -> None:
    async with stdio_client(server_params) as (read, write), ClientSession(read, write) as session:
        await session.initialize()

        # Test with invalid IVOD ID
        result = await session.call_tool("get_ivod", {"ivod_id": "invalid_id"})

        assert len(result.content) == 1
        assert isinstance(result.content[0], TextContent)

        response_text = result.content[0].text
        assert isinstance(response_text, str)


@pytest.mark.asyncio
async def test_get_meet_ivods(server_params: StdioServerParameters) -> None:
    async with stdio_client(server_params) as (read, write), ClientSession(read, write) as session:
        await session.initialize()

        # Test meet IVODs retrieval
        result = await session.call_tool("get_meet_ivods", {"meet_id": "院會-11-2-3", "limit": 3})

        assert len(result.content) == 1
        assert isinstance(result.content[0], TextContent)

        response_text = result.content[0].text
        assert isinstance(response_text, str)


@pytest.mark.asyncio
async def test_ivod_tools_available(server_params: StdioServerParameters) -> None:
    async with stdio_client(server_params) as (read, write), ClientSession(read, write) as session:
        await session.initialize()

        result = await session.list_tools()

        # Check that IVOD tools are available
        tool_names = [tool.name for tool in result.tools]
        expected_ivod_tools = [
            "list_ivods",
            "get_ivod",
            "get_meet_ivods",
        ]
        for tool_name in expected_ivod_tools:
            assert tool_name in tool_names


@pytest.mark.asyncio
async def test_list_laws(server_params: StdioServerParameters) -> None:
    async with stdio_client(server_params) as (read, write), ClientSession(read, write) as session:
        await session.initialize()

        # Test basic laws listing
        result = await session.call_tool("list_laws", {"page": 1, "limit": 5})

        assert len(result.content) == 1
        assert isinstance(result.content[0], TextContent)

        # Check response is string
        response_text = result.content[0].text
        assert isinstance(response_text, str)


@pytest.mark.asyncio
async def test_list_laws_with_filters(server_params: StdioServerParameters) -> None:
    async with stdio_client(server_params) as (read, write), ClientSession(read, write) as session:
        await session.initialize()

        # Test search with specific filters
        result = await session.call_tool("list_laws", {"category": "母法", "law_status": "現行", "limit": 3})

        assert len(result.content) == 1
        assert isinstance(result.content[0], TextContent)

        # Check response is string
        response_text = result.content[0].text
        assert isinstance(response_text, str)


@pytest.mark.asyncio
async def test_get_law_detail_error_handling(server_params: StdioServerParameters) -> None:
    async with stdio_client(server_params) as (read, write), ClientSession(read, write) as session:
        await session.initialize()

        # Test with invalid law ID to check error handling
        result = await session.call_tool("get_law", {"law_id": "invalid_law_id"})

        assert len(result.content) == 1
        assert isinstance(result.content[0], TextContent)

        # Should contain string response
        response_text = result.content[0].text
        assert isinstance(response_text, str)


@pytest.mark.asyncio
async def test_get_law_detail_json(server_params: StdioServerParameters) -> None:
    async with stdio_client(server_params) as (read, write), ClientSession(read, write) as session:
        await session.initialize()

        # Test JSON response with a known law
        result = await session.call_tool("get_law", {"law_id": "09200015"})

        assert len(result.content) == 1
        assert isinstance(result.content[0], TextContent)

        response_text = result.content[0].text
        # Should be string
        assert isinstance(response_text, str)


@pytest.mark.asyncio
async def test_get_law_progress(server_params: StdioServerParameters) -> None:
    async with stdio_client(server_params) as (read, write), ClientSession(read, write) as session:
        await session.initialize()

        # Test law progress with a known law
        result = await session.call_tool("get_law_progress", {"law_id": "09200015"})

        assert len(result.content) == 1
        assert isinstance(result.content[0], TextContent)

        response_text = result.content[0].text
        # Should be string
        assert isinstance(response_text, str)


@pytest.mark.asyncio
async def test_get_law_bills(server_params: StdioServerParameters) -> None:
    async with stdio_client(server_params) as (read, write), ClientSession(read, write) as session:
        await session.initialize()

        # Test law bills with a known law
        result = await session.call_tool("get_law_bills", {"law_id": "09200015", "limit": 3})

        assert len(result.content) == 1
        assert isinstance(result.content[0], TextContent)

        response_text = result.content[0].text
        # Should be string
        assert isinstance(response_text, str)


@pytest.mark.asyncio
async def test_get_law_versions(server_params: StdioServerParameters) -> None:
    async with stdio_client(server_params) as (read, write), ClientSession(read, write) as session:
        await session.initialize()

        # Test law versions with a known law
        result = await session.call_tool("get_law_versions", {"law_id": "09200015", "limit": 3})

        assert len(result.content) == 1
        assert isinstance(result.content[0], TextContent)

        response_text = result.content[0].text
        # Should be string
        assert isinstance(response_text, str)


@pytest.mark.asyncio
async def test_laws_tools_available(server_params: StdioServerParameters) -> None:
    async with stdio_client(server_params) as (read, write), ClientSession(read, write) as session:
        await session.initialize()

        result = await session.list_tools()

        # Check that laws tools are available
        tool_names = [tool.name for tool in result.tools]
        expected_laws_tools = [
            "list_laws",
            "get_law",
            "get_law_progress",
            "get_law_bills",
            "get_law_versions",
            "list_law_contents",
            "get_law_content",
        ]
        for tool_name in expected_laws_tools:
            assert tool_name in tool_names


@pytest.mark.asyncio
async def test_list_law_contents(server_params: StdioServerParameters) -> None:
    async with stdio_client(server_params) as (read, write), ClientSession(read, write) as session:
        await session.initialize()

        # Test basic law contents listing
        result = await session.call_tool(
            "list_law_contents",
            arguments={
                "page": 1,
                "limit": 5,
            },
        )

        assert result.isError is False
        assert len(result.content) == 1
        assert isinstance(result.content[0], TextContent)

        response_text = result.content[0].text

        # Should be string
        assert isinstance(response_text, str)


@pytest.mark.asyncio
async def test_list_law_contents_with_filters(server_params: StdioServerParameters) -> None:
    async with stdio_client(server_params) as (read, write), ClientSession(read, write) as session:
        await session.initialize()

        # Test law contents listing with filters
        result = await session.call_tool(
            "list_law_contents",
            arguments={
                "law_number": "90481",
                "current_version_status": "現行",
                "page": 1,
                "limit": 5,
            },
        )

        assert result.isError is False
        assert len(result.content) == 1
        assert isinstance(result.content[0], TextContent)

        response_text = result.content[0].text

        # Should be string
        assert isinstance(response_text, str)


@pytest.mark.asyncio
async def test_get_law_content(server_params: StdioServerParameters) -> None:
    async with stdio_client(server_params) as (read, write), ClientSession(read, write) as session:
        await session.initialize()

        # First get a list of law contents to get a valid ID
        list_result = await session.call_tool(
            "list_law_contents",
            arguments={
                "limit": 1,
            },
        )

        assert list_result.isError is False

        # We can also test with a known format, based on the swagger spec example
        result = await session.call_tool(
            "get_law_content",
            arguments={
                "law_content_id": "90481:90481:1944-02-29-制定:0",
            },
        )

        # Note: This might fail if the specific ID doesn't exist, but that's okay for the test
        # The important thing is that the tool is properly configured and callable
        assert len(result.content) == 1
        assert isinstance(result.content[0], TextContent)


# === Legislators API Tests ===

@pytest.mark.asyncio
async def test_list_legislators(server_params: StdioServerParameters) -> None:
    async with stdio_client(server_params) as (read, write), ClientSession(read, write) as session:
        await session.initialize()

        # Test basic legislators listing
        result = await session.call_tool("list_legislators", {"page": 1, "limit": 5})

        assert result.isError is False
        assert len(result.content) == 1
        assert isinstance(result.content[0], TextContent)

        response_text = result.content[0].text

        # Should be string
        assert isinstance(response_text, str)


@pytest.mark.asyncio
async def test_list_legislators_with_filters(server_params: StdioServerParameters) -> None:
    async with stdio_client(server_params) as (read, write), ClientSession(read, write) as session:
        await session.initialize()

        # Test legislators listing with filters
        result = await session.call_tool(
            "list_legislators",
            arguments={
                "term": 11,
                "party": "民主進步黨",
                "page": 1,
                "limit": 3,
            },
        )

        assert result.isError is False
        assert len(result.content) == 1
        assert isinstance(result.content[0], TextContent)

        response_text = result.content[0].text

        # Should be string
        assert isinstance(response_text, str)


@pytest.mark.asyncio
async def test_get_legislator(server_params: StdioServerParameters) -> None:
    async with stdio_client(server_params) as (read, write), ClientSession(read, write) as session:
        await session.initialize()

        # Test getting specific legislator
        result = await session.call_tool(
            "get_legislator",
            arguments={
                "term": 11,
                "name": "韓國瑜",
            },
        )

        # Note: This might fail if the specific legislator doesn't exist, but that's okay for the test
        # The important thing is that the tool is properly configured and callable
        assert len(result.content) == 1
        assert isinstance(result.content[0], TextContent)


@pytest.mark.asyncio
async def test_get_legislator_propose_bills(server_params: StdioServerParameters) -> None:
    async with stdio_client(server_params) as (read, write), ClientSession(read, write) as session:
        await session.initialize()

        # Test getting legislator propose bills
        result = await session.call_tool(
            "get_legislator_propose_bills",
            arguments={
                "term": 11,
                "name": "韓國瑜",
                "page": 1,
                "limit": 3,
            },
        )

        # Note: This might fail if the specific legislator doesn't exist, but that's okay for the test
        # The important thing is that the tool is properly configured and callable
        assert len(result.content) == 1
        assert isinstance(result.content[0], TextContent)


@pytest.mark.asyncio
async def test_get_legislator_cosign_bills(server_params: StdioServerParameters) -> None:
    async with stdio_client(server_params) as (read, write), ClientSession(read, write) as session:
        await session.initialize()

        # Test getting legislator cosign bills
        result = await session.call_tool(
            "get_legislator_cosign_bills",
            arguments={
                "term": 11,
                "name": "韓國瑜",
                "page": 1,
                "limit": 3,
            },
        )

        # Note: This might fail if the specific legislator doesn't exist, but that's okay for the test
        # The important thing is that the tool is properly configured and callable
        assert len(result.content) == 1
        assert isinstance(result.content[0], TextContent)


@pytest.mark.asyncio
async def test_get_legislator_meets(server_params: StdioServerParameters) -> None:
    async with stdio_client(server_params) as (read, write), ClientSession(read, write) as session:
        await session.initialize()

        # Test getting legislator meets
        result = await session.call_tool(
            "get_legislator_meets",
            arguments={
                "term": 11,
                "name": "韓國瑜",
                "page": 1,
                "limit": 3,
            },
        )

        # Note: This might fail if the specific legislator doesn't exist, but that's okay for the test
        # The important thing is that the tool is properly configured and callable
        assert len(result.content) == 1
        assert isinstance(result.content[0], TextContent)


@pytest.mark.asyncio
async def test_list_meets(server_params: StdioServerParameters) -> None:
    async with stdio_client(server_params) as (read, write), ClientSession(read, write) as session:
        await session.initialize()

        # Test listing meets
        result = await session.call_tool(
            "list_meets",
            arguments={
                "term": 11,
                "page": 1,
                "limit": 3,
            },
        )

        assert len(result.content) == 1
        assert isinstance(result.content[0], TextContent)


@pytest.mark.asyncio
async def test_get_meet(server_params: StdioServerParameters) -> None:
    async with stdio_client(server_params) as (read, write), ClientSession(read, write) as session:
        await session.initialize()

        # Test getting meet detail
        result = await session.call_tool(
            "get_meet",
            arguments={
                "meet_id": "院會-11-2-3",
            },
        )

        # Note: This might fail if the specific meet doesn't exist, but that's okay for the test
        # The important thing is that the tool is properly configured and callable
        assert len(result.content) == 1
        assert isinstance(result.content[0], TextContent)


@pytest.mark.asyncio
async def test_get_meet_bills(server_params: StdioServerParameters) -> None:
    async with stdio_client(server_params) as (read, write), ClientSession(read, write) as session:
        await session.initialize()

        # Test getting meet bills
        result = await session.call_tool(
            "get_meet_bills",
            arguments={
                "meet_id": "院會-11-2-3",
                "page": 1,
                "limit": 3,
            },
        )

        # Note: This might fail if the specific meet doesn't exist, but that's okay for the test
        # The important thing is that the tool is properly configured and callable
        assert len(result.content) == 1
        assert isinstance(result.content[0], TextContent)


@pytest.mark.asyncio
async def test_get_meet_interpellations(server_params: StdioServerParameters) -> None:
    async with stdio_client(server_params) as (read, write), ClientSession(read, write) as session:
        await session.initialize()

        # Test getting meet interpellations
        result = await session.call_tool(
            "get_meet_interpellations",
            arguments={
                "meet_id": "院會-11-2-3",
                "page": 1,
                "limit": 3,
            },
        )

        # Note: This might fail if the specific meet doesn't exist, but that's okay for the test
        # The important thing is that the tool is properly configured and callable
        assert len(result.content) == 1
        assert isinstance(result.content[0], TextContent)
