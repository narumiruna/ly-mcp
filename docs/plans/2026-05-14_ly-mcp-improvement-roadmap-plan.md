## Goal

Define the improvement roadmap for the current `lymcp` MCP server gaps found through repository review, OpenAPI comparison, and live MCP tool usage. Success means every identified gap is assigned to an executable plan with clear verification evidence.

## Status

Completed. All linked implementation plans have landed on `main`; this roadmap
is retained as the closeout record for the improvement pass.

## Context

At planning time, the server wrapped the Legislative Yuan API v2 as MCP tools with broad endpoint coverage, but review found missing Law Version tools, weak contract testing, plain-string error handling, incomplete tool discoverability, no reusable MCP prompts/resources, and ambiguity around "latest" queries that include future scheduled records.

The `roadmap-completion` follow-up marked the linked implementation plans done.

## Non-Goals

- Do not implement the fixes in this planning step.
- Do not archive the existing `manual-live-and-mock-tests` plan automatically.
- Do not introduce new runtime dependencies unless a downstream implementation plan proves they are needed.

## Assumptions

- `swagger.yaml` remains the local source of truth for supported API endpoints and query parameters.
- The MCP server can keep returning text content when needed, but response and error semantics should become easier for clients and tests to validate.
- Improvements can be split across focused PRs without requiring a large rewrite of the server.

## Plan

- [x] Complete the API coverage work described in `docs/plans/2026-05-14_api-coverage-and-tool-schema-plan.md` to align MCP tools with `swagger.yaml`; verified with `docs/api-endpoint-tool-audit.md`, 39 `@mcp.tool()` registrations, and MCP tool tests.
- [x] Complete the test-contract work described in `docs/plans/2026-05-14_test-contract-and-ci-verification-plan.md` to make default tests deterministic and meaningful; verified with `just test`, `just lint`, and `just type`.
- [x] Complete the structured error and response work described in `docs/plans/2026-05-14_structured-errors-and-responses-plan.md` to make failures and result payloads machine-checkable; verified with unit tests for HTTP errors, JSON parse errors, timeout handling, and MCP tool error output.
- [x] Complete the discovery and query semantics work described in `docs/plans/2026-05-14_discovery-prompts-and-query-semantics-plan.md` to improve common natural-language tasks such as latest meetings, law histories, and legislator activity lookups; verified with registered MCP prompts/resources and representative live smoke checks.
- [x] Update `README.md` after the implementation plans land so feature lists, test commands, and example prompts match actual behavior; verified by reviewing README sections against current `list_tools`, `justfile`, pytest marker behavior, response contract, and discovery prompts/resources.

## Risks

- The live Legislative Yuan API can return future schedule records, changing what "latest" means depending on user intent.
- Tool schema changes can break existing users if parameter names are renamed instead of added compatibly.
- Large raw JSON responses can remain token-heavy even after structured errors are improved.

## Completion Checklist

- [x] Every gap from the research pass is represented by one linked plan, verified by comparing this roadmap against the completed linked implementation plans.
- [x] The roadmap remains bounded to planning/status work, verified by this follow-up changing only the roadmap document.
- [x] Each linked plan has `Goal`, `Plan`, and `Completion Checklist` sections with executable verification methods.
- [x] The user accepts the plan split or requests a different grouping, verified by explicit requests to continue picking and implementing plans.
