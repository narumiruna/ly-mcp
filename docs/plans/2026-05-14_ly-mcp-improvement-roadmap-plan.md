## Goal

Define the improvement roadmap for the current `lymcp` MCP server gaps found through repository review, OpenAPI comparison, and live MCP tool usage. Success means every identified gap is assigned to an executable plan with clear verification evidence.

## Context

The current server wraps the Legislative Yuan API v2 as MCP tools. Review found broad endpoint coverage, but also missing Law Version tools, weak contract testing, plain-string error handling, incomplete tool discoverability, no reusable MCP prompts/resources, and ambiguity around "latest" queries that include future scheduled records.

## Non-Goals

- Do not implement the fixes in this planning step.
- Do not archive the existing `manual-live-and-mock-tests` plan automatically.
- Do not introduce new runtime dependencies unless a downstream implementation plan proves they are needed.

## Assumptions

- `swagger.yaml` remains the local source of truth for supported API endpoints and query parameters.
- The MCP server can keep returning text content when needed, but response and error semantics should become easier for clients and tests to validate.
- Improvements can be split across focused PRs without requiring a large rewrite of the server.

## Plan

- [ ] Complete the API coverage work described in `docs/plans/2026-05-14_api-coverage-and-tool-schema-plan.md` to align MCP tools with `swagger.yaml`; verify with an endpoint-to-tool audit and MCP `list_tools` coverage.
- [ ] Complete the test-contract work described in `docs/plans/2026-05-14_test-contract-and-ci-verification-plan.md` to make default tests deterministic and meaningful; verify with `just test`, `just lint`, and `just type`.
- [ ] Complete the structured error and response work described in `docs/plans/2026-05-14_structured-errors-and-responses-plan.md` to make failures and result payloads machine-checkable; verify with unit tests for HTTP errors, JSON parse errors, and successful MCP tool output.
- [ ] Complete the discovery and query semantics work described in `docs/plans/2026-05-14_discovery-prompts-and-query-semantics-plan.md` to improve common natural-language tasks such as latest meetings, law histories, and legislator activity lookups; verify with documented MCP prompts/resources and representative live smoke checks.
- [ ] Update `README.md` after the implementation plans land so feature lists, test commands, and example prompts match actual behavior; verify by reviewing README sections against current `list_tools`, `justfile`, and pytest marker behavior.

## Risks

- The live Legislative Yuan API can return future schedule records, changing what "latest" means depending on user intent.
- Tool schema changes can break existing users if parameter names are renamed instead of added compatibly.
- Large raw JSON responses can remain token-heavy even after structured errors are improved.

## Completion Checklist

- [ ] Every gap from the research pass is represented by one linked plan, verified by comparing this roadmap against the issue list in the final research summary.
- [ ] The roadmap remains bounded to planning work, verified by no production code changes in this PR or commit.
- [ ] Each linked plan has `Goal`, `Plan`, and `Completion Checklist` sections with executable verification methods.
- [ ] The user accepts the plan split or requests a different grouping, verified by explicit user acceptance or a follow-up edit request.
