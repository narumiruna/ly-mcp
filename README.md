# ly-mcp

A Model Context Protocol (MCP) server for Taiwan's Legislative Yuan API v2, providing bill search, detailed information, related documents, and meeting records.

## Features

This MCP server provides the following tools:

- **search_bills**: Search bills by term, session, category, proposer, and other criteria
- **get_bill_detail**: Get comprehensive information about specific bills
- **get_bill_related_bills**: Query related bills and their associations
- **get_bill_doc_html**: Retrieve HTML-formatted bill documents
- **get_bill_meets**: Access bill deliberation records from various meetings

## API Source

This MCP server uses the [Legislative Yuan API v2](https://ly.govapi.tw/v2) as its data source, providing information about Taiwan's Legislative Yuan bills and proceedings.

## Installation & Usage

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

### Local

```json
{
  "mcpServers": {
    "lymcp": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/home/<user>/workspace/ly-mcp",
        "lymcp"
      ]
    }
  }
}
```
