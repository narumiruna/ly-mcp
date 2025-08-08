# copilot-instructions.md

This file provides guidance to GitHub Copilot when working with code in this repository, based on the actual codebase and project structure.

## Project Overview

This repository implements an MCP (Model Context Protocol) server for accessing the Taiwan Legislative Yuan API v2. It provides tools to search and retrieve information about legislative bills, meetings, and related documents via the ly.govapi.tw API.

## Architecture & Key Files

- **Entry point:** `src/lymcp/server.py` (main FastMCP server, tool definitions)
- **API integration:** `src/lymcp/api.py` (Pydantic models, async httpx API calls)
- **Tool implementation:** All MCP tools are decorated with `@mcp.tool()` in `server.py` and use Pydantic `Field` for parameter descriptions (in Chinese)
- **Testing:** `tests/test_server.py` (pytest + MCP client integration tests)
- **Dependency management:** [uv](https://docs.astral.sh/uv/) (see `pyproject.toml`)
- **CI:** GitHub Actions workflows in `.github/workflows/`

## MCP Tools (see `src/lymcp/server.py`)

- `list_bills`: Search bills with multiple filters
- `get_bill_detail`: Get detailed information for a specific bill
- `get_bill_related_bills`: Query related bills
- `get_bill_meets`: Query bill-related meeting records
- `get_bill_doc_html`: Get bill-related HTML documents

All tools:

- Parameters have Chinese descriptions
- Return JSON string (`json.dumps(..., ensure_ascii=False, indent=2)`)
- Exception handling always returns a Chinese error message

## API Calls

- Source API specification is defined in `swagger.yaml`. Follow the same naming conventions as in the API spec
- Use `httpx.AsyncClient(timeout=30.0)` for API requests
- API requests and data models are defined in `src/lymcp/api.py`, each tool has a corresponding request model

## Testing

- Use pytest + MCP client for integration tests (`tests/test_server.py`)
- Tests cover tool listing, tool invocation, and error handling
- To start the MCP server for tests: `uv run lymcp`

## Common Development Commands

### Install/Sync dependencies

```bash
uv sync
```

### Start local server

```bash
uv run lymcp
```

### Run tests

```bash
make test
# or
uv run pytest -v -s
```

### Lint & Type Check

```bash
make lint
make type
uv run ruff check .
uv run mypy .
```

### Build & Publish

```bash
make publish
uv build -f wheel
uv publish
```

## MCP Client Integration

- PyPI: `uvx lymcp@latest`
- GitHub: `uvx --from git+https://github.com/narumiruna/ly-mcp lymcp`
- Local: `uv run --directory <path> lymcp`

## CI/CD

- `.github/workflows/python.yml`: Lint/type/test/coverage
- `.github/workflows/publish.yml`: PyPI publish
- `.github/workflows/docker.yml`: Docker build/push
- `.github/workflows/bump-version.yml`: Auto version bump

## Other

- Project is MIT licensed
- Main language: Python 3.12+
