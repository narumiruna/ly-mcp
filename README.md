# ly-mcp

[![PyPI version](https://img.shields.io/pypi/v/lymcp)](https://pypi.org/project/lymcp/)
[![Python](https://img.shields.io/pypi/pyversions/lymcp)](https://pypi.org/project/lymcp/)
[![CI](https://github.com/narumiruna/ly-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/narumiruna/ly-mcp/actions/workflows/ci.yml)
[![Docker](https://github.com/narumiruna/ly-mcp/actions/workflows/docker.yml/badge.svg)](https://github.com/narumiruna/ly-mcp/actions/workflows/docker.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Model Context Protocol (MCP) server for Taiwan's Legislative Yuan API v2, providing comprehensive access to bills, committees, gazettes, meeting records, and related documents.

## Features

This MCP server provides 39 tools across 9 categories:

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

### Interpellations (質詢)
- **list_interpellations**: List interpellations with optional filters by member, term, session, and meeting code
- **get_interpellation**: Get detailed information about specific interpellations
- **get_legislator_interpellations**: Get interpellations where a specific legislator is the questioning member

### IVODs (網路電視)
- **list_ivods**: List IVOD (Internet Video On Demand) recordings with optional filters by term, session, committee, member, and video type
- **get_ivod**: Get detailed information about specific IVOD recordings, including video URLs, transcripts, and gazette content
- **get_meet_ivods**: Get IVOD recordings related to specific meetings

### Laws (法律)
- **list_laws**: List laws with optional filters by law number, category (母法/子法), parent law number, status, and authority
- **get_law**: Get comprehensive information about specific laws including basic data, articles, and version information
- **get_law_progress**: Get undecided progress list for specific laws
- **get_law_bills**: Get bills related to specific laws with optional filters
- **get_law_versions**: Get historical version records for specific laws including changes, proposers, and progress
- **list_law_versions**: List law versions across laws with optional filters by law number, version number, date, action, progress, and current version status
- **get_law_version**: Get detailed information about a specific law version by version ID
- **get_law_version_contents**: Get law article contents included in a specific law version
- **list_law_contents**: List law articles/contents with optional filters by law number, version ID, article number, current version status, and version tracking
- **get_law_content**: Get detailed information about specific law articles/contents using law content ID

### Meets (會議)
- **list_meets**: List Legislative Yuan meetings with optional filters by term, session, meeting type, attendees, date, committee code, and meeting ID
- **get_meet**: Get detailed information about specific meetings using meeting ID/code
- **get_meet_ivods**: Get IVOD (Internet Video On Demand) recordings related to specific meetings with optional filters
- **get_meet_bills**: Get bills discussed in specific meetings with optional filters by bill criteria
- **get_meet_interpellations**: Get interpellations that occurred in specific meetings with optional filters

### Legislators (立法委員)
- **list_legislators**: List legislators with optional filters by term, party, district name, legislator ID, and name
- **get_legislator**: Get detailed information about specific legislators by term and name
- **get_legislator_propose_bills**: Get bills proposed by a specific legislator with optional filters by bill criteria
- **get_legislator_cosign_bills**: Get bills co-signed by a specific legislator with optional filters by bill criteria
- **get_legislator_meets**: Get meetings attended by a specific legislator with optional filters by meeting criteria
- **get_legislator_interpellations**: Get interpellations made by a specific legislator with optional filters

## API Source

This MCP server uses the [Legislative Yuan API v2](https://ly.govapi.tw/v2) as its data source, providing information about Taiwan's Legislative Yuan bills and proceedings.

## Tool Response Contract

Successful MCP tool calls return the raw JSON payload from the Legislative Yuan
API. Failed tool calls return a machine-checkable JSON error envelope:

```json
{
  "ok": false,
  "error": {
    "type": "http_status",
    "message": "Upstream API returned HTTP 404 for https://ly.govapi.tw/v2/bills/invalid_bill_number",
    "url": "https://ly.govapi.tw/v2/bills/invalid_bill_number",
    "status_code": 404,
    "response_excerpt": "not found"
  }
}
```

Current error `type` values include `http_status`, `timeout`,
`network_error`, `invalid_json`, and `unexpected_error`.

## Installation & Usage

### Quick Start

Install and run the server using `uvx`:

```bash
uvx lymcp@latest
```

### MCP Client Configuration

Add the server to your MCP client configuration (e.g., Claude Desktop):

#### PyPI

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

#### GitHub

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

#### Local Development

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

#### Docker

```json
{
  "mcpServers": {
    "lymcp": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "narumi/ly-mcp:latest"
      ]
    }
  }
}
```

## Example Prompts

Once connected to the MCP server, you can ask your LLM questions like:

- "列出第11屆的所有法律提案" (List all bills from the 11th term)
- "查詢立法委員王美花的提案紀錄" (Look up legislator Wang Mei-hua's proposed bills)
- "以今天的台北日期為準，最近已發生的院會討論了哪些議案？" (Using today's Taipei date, what bills were discussed in the latest occurred plenary meeting?)
- "下一場已排程的院會是什麼時候？" (When is the next scheduled plenary meeting?)
- "查詢勞動基準法的修法歷程" (Look up the amendment history of the Labor Standards Act)
- "第11屆第1會期有哪些委員會會議？" (What committee meetings were held in the 1st session of the 11th term?)

For date-sensitive questions, distinguish:

- `latest known`: use the upstream default sort, including future scheduled records.
- `latest occurred`: only consider records whose relevant date is on or before the reference date.
- `next scheduled`: only consider records whose relevant date is after the reference date.

The server also exposes MCP prompts for common workflows:
`latest_plenary_meeting_bills`, `law_amendment_history`,
`legislator_proposal_record`, `legislator_interpellations`, and
`committee_meeting_lookup`. Read `lymcp://query-semantics` and
`lymcp://workflow-reference` for compact guidance on date semantics, filters,
ID fields, and workflow steps.

## Development

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager
- [just](https://github.com/casey/just) command runner

### Setup

```bash
git clone https://github.com/narumiruna/ly-mcp
cd ly-mcp
uv sync
```

### Using Codex CLI

This repository includes `.codex/config.toml` for local Codex CLI development.
When you start Codex CLI from the repository root, it can use the configured
`lymcp` MCP server via `uv run lymcp`.

### Running the MCP Inspector

```bash
just dev
```

### Running Tests

```bash
# Run the default offline test suite with coverage
just test

# Run the default offline test suite directly
uv run pytest -v -s

# Run live tests against the Legislative Yuan API manually
just test-live
```

The default pytest configuration excludes tests marked `live`, so CI and normal
local runs use fixture-backed samples from `tests/data`. Refresh those JSON
samples intentionally when the live API shape changes.

### Code Quality

```bash
# Run linter
just lint

# Run type checker
just type
```

## License

MIT
