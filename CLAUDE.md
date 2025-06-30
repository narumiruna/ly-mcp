# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an MCP (Model Context Protocol) server for accessing Taiwan Legislative Yuan API v2. The project provides tools to search and retrieve information about legislative bills, meetings, and related documents through the ly.govapi.tw API.

## Architecture

- **Entry point**: `src/lymcp/server.py` - Main server implementation using FastMCP
- **Core MCP server**: Built on `mcp.server.fastmcp.FastMCP` framework
- **API integration**: Uses httpx for async HTTP requests to ly.govapi.tw/v2
- **Tools**: MCP tools for searching bills, getting bill details, related bills, documents, and meetings
- **Package management**: Uses `uv` for dependency management and virtual environments
- **Testing**: pytest-based test suite with MCP client integration tests

## Key Development Commands

### Testing
```bash
make test              # Run full test suite with coverage
uv run pytest -v -s   # Run tests with verbose output
```

### Code Quality
```bash
make lint              # Run ruff linter
make type              # Run mypy type checking
uv run ruff check .    # Direct ruff usage
uv run mypy .          # Direct mypy usage
```

### Development Server
```bash
uv run lymcp           # Run the Legislative Yuan MCP server locally
```

### Building and Publishing
```bash
make publish           # Build wheel and publish to PyPI
uv build -f wheel      # Build wheel only
```

## MCP Integration

The server can be integrated into Claude Desktop or other MCP clients using these configurations:

- **GitHub**: Uses `uvx --from git+https://github.com/narumiruna/ly-mcp lymcp`
- **PyPI**: Uses `uvx lymcp@latest`
- **Local development**: Uses `uv run --directory <path> lymcp`

## Available MCP Tools

The server provides the following tools for accessing Legislative Yuan data:

1. **search_bills**: Search legislative bills by term, session, category, proposer, etc.
2. **get_bill_detail**: Get detailed information for a specific bill by bill number
3. **get_bill_related_bills**: Get related bills for a specific bill
4. **get_bill_doc_html**: Get HTML document content for a specific bill
5. **get_bill_meets**: Get meeting records related to a specific bill

## Tool Development

MCP tools are implemented as decorated functions in `server.py`:
- Use `@mcp.tool()` decorator
- Use Pydantic `Field` for parameter descriptions with Chinese descriptions
- All tools return strings (JSON formatted for structured data)
- Include comprehensive error handling with Chinese error messages
- Support both structured and raw JSON response formats

## API Response Handling

The server uses a unified `APIResponse` model for consistent error handling:
- All API calls go through `make_api_request()` function
- Handles HTTP errors (404, 429, 500, etc.) with user-friendly Chinese messages
- Includes timeout and connection error handling
- Supports pagination information extraction

## Testing MCP Tools

Tests use the MCP client SDK to integration test tools:
- Set up `StdioServerParameters` with `uv run lymcp`
- Use `stdio_client` and `ClientSession` for testing
- Test both tool listing and tool execution
- Test error scenarios and edge cases
