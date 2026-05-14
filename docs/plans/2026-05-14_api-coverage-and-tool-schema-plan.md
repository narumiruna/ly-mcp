## Goal

Bring the MCP tool surface into alignment with `swagger.yaml` and make query parameters easier to discover and use. Success means every Legislative Yuan API v2 endpoint in `swagger.yaml` has an intentional MCP representation, and supported filters are either exposed as tool parameters or explicitly documented as intentionally raw.

## Context

The current server exposes 36 MCP tools, while `swagger.yaml` lists 39 endpoints. The missing endpoint group is the top-level Law Version API:

- `/law_versions`
- `/law_versions/{id}`
- `/law_versions/{id}/contents`

Live `list_bills` responses also report `supported_filter_fields` that are not all represented in the MCP tool schema, such as `提案單位/提案委員`.

## Architecture

The current code has a direct two-layer wrapper:

- `src/lymcp/api.py` defines Pydantic request models and API calls.
- `src/lymcp/server.py` exposes FastMCP tools that construct request models and JSON-dump responses.
- `src/lymcp/translate.py` maps English internal parameter names to Legislative Yuan API query-field names.

This plan keeps that architecture and adds only the missing request classes, translation keys, server tools, and tests.

## Non-Goals

- Do not redesign all tools or replace the current wrapper architecture.
- Do not remove existing parameter names such as `cosigner`; add compatible aliases only if needed.
- Do not add generated OpenAPI client code in this phase.

## Unknowns

- Whether `/law_versions/{id}/contents` uses the same content ID shape as `law_contents`; resolve by running one live query from a known version ID before implementing tests.
- Whether all `supported_filter_fields` should become first-class MCP parameters or stay accessible through a generic raw filter mechanism; resolve by auditing repeated fields across endpoint categories.

## Plan

- [ ] Build an endpoint-to-tool audit table from `swagger.yaml` and current `@mcp.tool()` definitions to identify missing and intentionally unsupported endpoints; verify with a checked-in note or test fixture listing all endpoint paths and tool names.
- [ ] Add translation keys for Law Version filters and IDs in `src/lymcp/translate.py` to support `/law_versions` and `/law_versions/{id}/contents`; verify with unit tests asserting serialized query parameter names.
- [ ] Add `ListLawVersionsRequest`, `GetLawVersionRequest`, and `GetLawVersionContentsRequest` in `src/lymcp/api.py` to call `/law_versions`, `/law_versions/{id}`, and `/law_versions/{id}/contents`; verify with monkeypatched API tests that assert URL and params.
- [ ] Add `list_law_versions`, `get_law_version`, and `get_law_version_contents` tools in `src/lymcp/server.py` with clear Traditional Chinese parameter descriptions; verify with MCP `list_tools` tests and fixture-backed tool call tests.
- [ ] Compare API `supported_filter_fields` against tool parameters for bills, laws, law versions, meetings, IVODs, and legislators; verify with an audit output that marks each field as `first-class parameter`, `output_fields only`, or `deferred`.
- [ ] Add first-class parameters for high-value missing filters, starting with bill `提案單位/提案委員` if confirmed by `swagger.yaml` or live responses; verify with request serialization tests and one live smoke query.
- [ ] Update `README.md` feature lists and examples to include Law Version tools only after the tools and tests exist; verify by matching README tool names against MCP `list_tools`.

## Risks

- Some query fields appear only in live `supported_filter_fields` but not in `swagger.yaml`, so adding them blindly could create unstable behavior.
- Law version IDs include colons and Chinese action names, so URL encoding and examples must be tested.
- Adding many first-class parameters can make tool schemas noisy; prioritize high-value filters first.

## Completion Checklist

- [ ] All 39 `swagger.yaml` endpoints are intentionally represented or documented as out of scope, verified by the endpoint-to-tool audit.
- [ ] The three Law Version MCP tools are available in `list_tools`, verified by a server test.
- [ ] Law Version request classes serialize URLs and params correctly, verified by monkeypatched API unit tests.
- [ ] README feature counts and tool lists match the actual server, verified by manual review against `rg "@mcp.tool" src/lymcp/server.py`.
