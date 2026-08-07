# Swagger Query Parameter Alignment Plan

## Goal

Expose every query parameter currently documented by `swagger.yaml` through the LYMCP request, MCP tool, CLI, and bundled `ly` skill surfaces. Completion means all 42 endpoints remain covered, all 298 endpoint/query-parameter slots are represented and serialized, and agent-facing command guidance matches the implemented CLI.

## Context

The refreshed contract has no missing endpoint implementation: `swagger.yaml`, the MCP server, and the CLI each expose 42 endpoint operations. A stricter serialization audit found 8 query-parameter gaps across two operations:

- `/bills/{billNo}/meets` lacks `會議代碼`, `會議資料.出席委員`, `委員會代號`, `會議資料.會議編號`, `議事網資料.關係文書.議案.議案編號`, `議事網資料.關係文書.議案.法律編號`, and `output_fields`.
- `/gazettes/{id}/agendas` lacks the query-form `公報編號`; its path `{id}` is already implemented, but the separately documented query field is not.

`tests/test_swagger_coverage.py` currently verifies only endpoint, MCP tool, and CLI command inventories, so it passes without detecting query-parameter drift. The bundled `skills/ly/SKILL.md` also predates the Vote commands: its trigger description, command map, workflow domains, and examples do not mention `ly votes`.

## Architecture

The alignment path is `swagger.yaml` → Pydantic request serialization in `src/lymcp/api.py` → MCP functions in `src/lymcp/tools/` → Typer commands in `src/lymcp/commands/`.

To avoid collisions between path identifiers and query filters:

- Keep the required bill path argument as `bill_no`; expose the nested meeting filter as `related_bill_no`, serialized with `translate["bill_no_nested"]`.
- Keep the required gazette path argument as `gazette_id`; expose the optional query filter as `gazette_number`, serialized with `translate["gazette_id"]`. `GetGazetteAgendasRequest.do()` must continue excluding only the path field so the query value is emitted.
- Reuse the existing meeting filter vocabulary (`meeting_code`, `member`, `committee_code`, `meet_id`, and `law_number`) used by other meeting-relation requests.

PyYAML should be added only to the development dependency group so tests can parse the OpenAPI contract robustly without adding a runtime dependency.

## Non-Goals

- Adding new endpoints or changing response payloads.
- Promoting response-only fields that Swagger does not declare as query parameters.
- Removing existing extra parameters such as pagination on `/bills/{billNo}/related_bills`; unsupported-output cleanup should be handled separately.

## Plan

- [x] Add PyYAML to the development dependencies in `pyproject.toml` and `uv.lock`; verified PyYAML 6.0.3 imports and `uv lock --check` reports a current lockfile.
- [x] Extend `tests/test_swagger_coverage.py` with an explicit endpoint-to-request-model mapping and a mocked request-serialization audit that parses each operation's query parameters from `swagger.yaml`; verified the red test covers all 42 mappings and reports the 8 documented gaps on the two affected endpoints.
- [x] Add focused request tests in `tests/test_api_mock.py` for all seven `/bills/{billNo}/meets` fields and the distinct path/query gazette identifiers; verified the red run fails on the exact serialized parameter mismatches for both requests.
- [x] Add focused MCP and CLI forwarding tests in `tests/test_server_mock.py` and `tests/test_cli_mock.py` for the new meeting filters, `output_fields`/`--fields`, and `gazette_number`/`--gazette-number`; verified the red runs reject `meeting_code` at the MCP boundary and `--meeting-code` at the CLI boundary.
- [x] Expand `GetBillMeetsRequest` in `src/lymcp/api.py` with `meeting_code`, `member`, `committee_code`, `meet_id`, `related_bill_no`, `law_number`, and `output_fields`, preserving exclusion of the path `bill_no`; verified the focused API serialization case passes with every corresponding Swagger key.
- [x] Expand `GetGazetteAgendasRequest` in `src/lymcp/api.py` with optional `gazette_number` while retaining required path `gazette_id`; verified the focused API case keeps `1137701` in the path and serializes query value `1137702` as `公報編號`.
- [x] Extend `get_bill_meets` and `get_gazette_agendas` in `src/lymcp/tools/bills.py` and `src/lymcp/tools/gazettes.py` with typed, documented parameters and request forwarding; verified 40 focused server cases pass and MCP schemas expose all new fields.
- [x] Extend `ly bills meets` and `ly gazettes agendas` in `src/lymcp/commands/bills.py` and `src/lymcp/commands/gazettes.py` with matching options, including `--related-bill-no`, `--fields`, and `--gazette-number`; verified CLI forwarding tests pass and both commands' `--help` output lists the aligned options.
- [x] Update `skills/ly/SKILL.md` so its trigger description, command map, query workflow, and examples cover `votes list|get|meets` plus the newly aligned bill-meeting and gazette-agenda filters; verified the frontmatter and all newly documented commands and options against `ly ... --help`.
- [x] Update `README.md` and `docs/api-endpoint-tool-audit.md` to document the completed filters and query-parameter coverage; verified the documented CLI options exist and the parsed contract contains 42 endpoints and 298 query-parameter slots.
- [x] Add or extend targeted `@pytest.mark.live` smoke coverage in `tests/test_api.py` for the two affected endpoint requests; verified both focused live tests pass against the upstream API (`2 passed`).
- [x] Run `just lint`, `just type`, and `just test`; verified Ruff and ty pass, Swagger coverage reports no gaps, and the offline suite passes with 115 tests, 89 live skips, and 91% coverage.

## Risks

- The gazette path identifier and `公報編號` query filter may be redundant upstream. Keeping distinct internal names prevents accidental path substitution and follows the published contract without changing existing behavior.
- A generic serialization audit must observe the actual `params` passed to `make_api_request`; comparing only Pydantic aliases would incorrectly count excluded path fields as implemented query fields.
- Live API verification may be rate-limited. Deterministic serialization, MCP, CLI, and contract tests remain the completion authority; any live 429 must be documented rather than treated as functional evidence.

## Completion Checklist

- [x] All 42 Swagger endpoints still map one-to-one to MCP tools and CLI commands.
- [x] All 298 Swagger endpoint/query-parameter slots are present in serialized requests.
- [x] The 8 previously missing parameters are exposed through API models, MCP tools, and CLI commands.
- [x] Path identifiers remain distinct from same-name or nested query filters.
- [x] README, endpoint audit documentation, and `skills/ly/SKILL.md` match the implemented contract and CLI.
- [x] Targeted live behavior is verified by two passing upstream tests.
- [x] `just lint`, `just type`, and `just test` pass.
