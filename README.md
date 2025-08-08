# ly-mcp

A Model Context Protocol (MCP) server for Taiwan's Legislative Yuan API v2, providing comprehensive access to bills, committees, gazettes, meeting records, and related documents.

## Features

This MCP server provides the following tools:

### Statistics
- **get_stat**: Get Legislative Yuan API statistics and overview information

### Bills (議案)
- **list_bills**: List bills with optional filters by term, session, category, proposer, and other criteria
- **get_bill**: Get comprehensive information about specific bills (returns complete JSON)
- **get_bill_related_bills**: Query related bills and their associations
- **get_bill_meets**: Access bill deliberation records from various meetings
- **get_bill_doc_html**: Retrieve HTML document content for specific bills

### Committees (委員會)
- **list_committees**: List Legislative Yuan committees with optional filters
- **get_committee**: Get detailed information about specific committees
- **get_committee_meets**: Access committee meeting records and proceedings

### Gazettes (公報)
- **list_gazettes**: List Legislative Yuan gazettes with optional filters by volume and gazette ID
- **get_gazette**: Get detailed information about specific gazettes
- **get_gazette_agendas**: Get agendas/contents from specific gazettes
- **list_gazette_agendas**: List all gazette agendas with optional filters by term, meeting date, etc.
- **get_gazette_agenda**: Get detailed information about specific gazette agenda items

## API Source

This MCP server uses the [Legislative Yuan API v2](https://ly.govapi.tw/v2) as its data source, providing information about Taiwan's Legislative Yuan bills and proceedings.

## Installation & Usage

### Quick Start

Install and run the server using `uvx`:

```bash
uvx lymcp@latest
```

### MCP Client Configuration

Add the server to your MCP client configuration (e.g., Claude Desktop):

### PyPI

```json
{
  "mcpServers": {
    "lymcp": {
      "command": "uvx",
      "args": ["lymcp@latest"]
    }
  }
}
```

### GitHub

```json
{
  "mcpServers": {
    "lymcp": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/narumiruna/ly-mcp",
        "lymcp"
      ]
    }
  }
}
```

### Local Development

```json
{
  "mcpServers": {
    "lymcp": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/path/to/ly-mcp",
        "lymcp"
      ]
    }
  }
}
```

## Development

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager

### Setup

```bash
git clone https://github.com/narumiruna/ly-mcp
cd ly-mcp
uv sync
```

### Running Tests

```bash
# Run full test suite with coverage
make test

# Run tests with verbose output
uv run pytest -v -s
```

### Code Quality

```bash
# Run linter
make lint

# Run type checker
make type

# Run both linter and type checker
uv run ruff check .
uv run mypy .
```

### To-Do List

- [x] Stat
- [x] Bill
- [x] Committee
- [x] Gazette
- [ ] Interpellation
- [ ] Ivod
- [ ] Law
- [ ] Legislator
- [ ] Meet

## License

MIT
