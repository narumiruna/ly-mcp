# Swagger and Vote API Alignment Plan

## Goal

Align LYMCP with the refreshed Legislative Yuan API v2 contract: expose all 42 Swagger endpoints through the API, MCP, and CLI surfaces; add the newly documented bill and gazette filters; and keep endpoint coverage deterministic and auditable offline.

## Context

The refreshed `swagger.yaml` adds 310 lines without removing existing contract entries:

- Three Vote endpoints: `GET /votes`, `GET /votes/{id}`, and `GET /votes/{id}/meets`.
- `提案單位/提案委員` on five bill-listing endpoints: `/bills`, `/laws/{id}/bills`, both legislator bill relations, and `/meets/{id}/bills`.
- `期` and `冊別` on `/gazettes/{id}/agendas` and `/gazette_agendas`.

Current coverage is partial:

- `proposal_unit_or_member` already works for `/bills`, but not the other four bill-listing request/tool/CLI paths.
- Gazette agenda models and tools do not expose `期` or `冊別`.
- Vote request models, MCP tools, CLI commands, fixtures, and audit entries do not exist.
- The endpoint audit and CLI inventory still assert 39 endpoints/tools/commands rather than 42.

Live read-only probes confirmed that all three Vote endpoints return JSON, the Vote list advertises all nine documented filters, `投票委員` filtering works, Vote-to-meeting relations work, and gazette agenda `期`/`冊別` filters are accepted.

## Architecture

Preserve the existing data flow: English public parameters map through `src/lymcp/translate.py`, Pydantic request models in `src/lymcp/api.py` serialize upstream query fields, and MCP/CLI adapters call those models without reshaping upstream JSON.

Before adding the Vote adapters, split the oversized `src/lymcp/server.py` and `src/lymcp/cli.py` by API domain. Keep those files as composition roots and preserve existing imports/registrations so the refactor is behavior-neutral. Put shared MCP error handling and CLI output/runtime state in small support modules rather than introducing duplicate domain logic.

## Non-Goals

- Do not normalize or redesign the upstream Vote response schema.
- Do not infer enums for `表決型態` or `會議種類`; Swagger still models them as strings.
- Do not add write operations, caching, persistence, or analytics aggregation.
- Do not generate clients from Swagger or add a YAML parser dependency solely for coverage checks.

## Plan

### 1. Align newly documented filters

- [x] Adopt the refreshed `swagger.yaml` as the local contract baseline; verify its diff contains 42 paths, three added Vote endpoints, the documented filter additions, and no removed paths before committing it.
- [x] Extend `GetLawBillsRequest`, `GetLegislatorProposeBillsRequest`, `GetLegislatorCosignBillsRequest`, and `GetMeetBillsRequest` in `src/lymcp/api.py` with `proposal_unit_or_member`; verify each serializes to `提案單位/提案委員` in parameterized cases in `tests/test_api_mock.py`.
- [x] Extend both gazette agenda request models with English parameters `issue` (`期`) and `booklet` (`冊別`), adding aliases in `src/lymcp/translate.py`; verify URL parameter serialization for both endpoints in `tests/test_api_mock.py`.
- [x] Expose the four bill and two gazette filters through their existing MCP tools and CLI commands, including help text and shared keyword helpers; verify request-constructor wiring in `tests/test_server_mock.py` and Typer option behavior in `tests/test_cli_mock.py`.

### 2. Establish maintainable domain boundaries

- [x] Split MCP tools from `src/lymcp/server.py` into domain modules under `src/lymcp/tools/`, leaving server construction, resources, prompts, registration, and `main()` in the composition root; verify the pre-Vote set remains exactly 39 tools with unchanged names and schemas using `tests/test_server_mock.py`.
- [x] Split Typer domain groups from `src/lymcp/cli.py` into modules under `src/lymcp/commands/`, moving shared output/error execution into a support module and leaving root callback/registration in `cli.py`; verify all existing 39 command paths and global `--compact`/`--output` behavior with `tests/test_cli_mock.py`.
- [x] Confirm no resulting source module exceeds 1,000 lines and run `just lint`, `just type`, and `just test` before adding Vote behavior.

### 3. Implement Vote API requests

- [x] Add translation aliases for `vote_type`, `vote_time`, `voting_member`, `agreeing_member`, `opposing_member`, `abstaining_member`, and `gazette_document_id` in `src/lymcp/translate.py`; verify aliases match the nine Swagger query fields through request serialization tests.
- [x] Add `ListVotesRequest`, `GetVoteRequest`, and `GetVoteMeetsRequest` in `src/lymcp/api.py`, reusing the established meeting filter vocabulary for the relation endpoint; verify exact URLs, path exclusion from query parameters, pagination, `output_fields`, and all documented aliases in `tests/test_api_mock.py`.
- [x] Capture minimal sanitized fixtures for a Vote list, Vote detail, and Vote meetings under `tests/data/`; verify fixtures contain stable response-contract keys rather than assertions tied to transient totals or ordering.

### 4. Expose Vote through MCP and CLI

- [x] Add `list_votes`, `get_vote`, and `get_vote_meets` in the Vote MCP domain module with descriptive Pydantic annotations and existing structured error serialization; verify registration, request wiring, list response contract, and 404 behavior in `tests/test_server_mock.py`.
- [x] Add a `votes` Typer group with `list`, `get`, and `meets` commands, including `--fields` and all documented filters; verify help discovery, option-to-request mapping, JSON output, and error exit behavior in `tests/test_cli_mock.py`.
- [x] Increase the MCP and CLI inventories from 39 to 42 and add an offline endpoint-to-tool coverage test that extracts top-level path lines from `swagger.yaml` and compares them with one explicit endpoint/tool map; verify future Swagger additions fail with an actionable missing mapping.

### 5. Improve discovery and documentation

- [x] Update `lymcp://workflow-reference` and add a Vote-focused prompt for common questions such as a legislator's voting record or a Vote's related meeting; verify prompt/resource registration and references to `list_votes`, `get_vote`, and `get_vote_meets` in `tests/test_server_mock.py`.
- [x] Update `docs/api-endpoint-tool-audit.md` to list 42 covered endpoints and record the new bill, gazette, and Vote filter decisions; verify documented counts match the automated endpoint/tool coverage test.
- [x] Document the new `ly votes` commands and MCP tools in `README.md`; verify every shown command appears in `COMMAND_INVENTORY` and uses actual option names from Typer help.

### 6. Verify upstream compatibility and release readiness

- [x] Add `@pytest.mark.live` smoke cases for the three Vote request classes and the newly documented nested bill/gazette filters without asserting unstable totals; verify with targeted `uv run pytest -m live` cases.
- [x] Run `just lint`, `just type`, and `just test`, then run `just test-live`; record any upstream instability separately rather than weakening deterministic offline assertions.

## Risks

- Vote data and totals change frequently, so checked-in fixtures must test shape and wiring rather than current counts or first-record identity.
- `表決時間` is an upstream localized string, not an ISO timestamp; keep it as `str` and avoid local date parsing in this scope.
- `GetVoteMeetsRequest` duplicates the meeting filter surface; shared helpers may reduce adapter duplication, but request models should remain explicit so aliases and path exclusions are testable.
- Moving existing MCP and CLI functions can create registration or import-cycle regressions; complete and verify the behavior-neutral split before introducing Vote registrations.

## Completion Checklist

- [x] All 42 Swagger paths map to 42 MCP tools and 42 CLI command paths where applicable, with automated offline coverage evidence.
- [x] All newly documented bill and gazette filters serialize correctly and are reachable from MCP and CLI.
- [x] Vote list, detail, and meeting-relation flows work through API models, MCP tools, and CLI commands.
- [x] `docs/api-endpoint-tool-audit.md`, `README.md`, MCP discovery content, and runtime inventories agree.
- [x] `just lint`, `just type`, `just test`, and `just test-live` pass, or any live-only upstream failure is explicitly documented with offline gates still passing.

## Execution Evidence

- `tests/test_swagger_coverage.py` proves the refreshed contract, 42 registered MCP tools, and 42 CLI command paths agree.
- `find src/lymcp -name '*.py' ... wc -l` reports the largest module, `src/lymcp/api.py`, at 851 lines.
- `just lint`, `just type`, and `just test` passed; the offline suite reported 113 passed and 88 live tests skipped.
- The targeted new live suite passed all four Vote and filter smoke cases.
- `just test-live` reached the upstream service but was rate-limited: 55 tests passed and 33 later tests failed only with HTTP 429 responses. The deterministic offline gates and targeted new live coverage remain green; no assertions were weakened to hide the upstream limit.
