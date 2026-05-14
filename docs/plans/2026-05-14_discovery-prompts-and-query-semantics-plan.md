## Goal

Improve MCP usability for common Legislative Yuan research tasks by adding discoverable guidance, reusable prompts/resources, and bounded query semantics for "latest", "scheduled", "occurred", law histories, and legislator activity. Success means users can ask common questions with less trial-and-error and get results whose date semantics are explicit.

## Context

Live MCP checks showed that default sorted results can include future scheduled bills and meetings. On 2026-05-14, `list_bills(term=11)` returned bills with proposal dates after the current date, and `list_meets(term=11)` returned meetings scheduled for future dates. This is valid source data, but natural-language prompts like "最近一次院會" need a clear distinction between latest known record, latest occurred meeting, and next scheduled meeting.

## Architecture

Keep raw list/detail tools available. Add guidance and optional helper surfaces on top:

- MCP prompts for common workflows.
- MCP resources or documentation snippets for filter fields and ID usage.
- Optional helper tools only if prompts/resources are insufficient.

## Non-Goals

- Do not build a separate analytics engine in this phase.
- Do not guarantee legal interpretation or official status beyond the source API data.
- Do not remove access to future scheduled records.

## Unknowns

- Resolved: the pinned FastMCP version supports `@mcp.prompt` and `@mcp.resource`, verified by in-repo prompt/resource registration tests.
- Resolved for this pass: prompt and resource guidance is sufficient. No helper tools were added because they would duplicate raw list/detail tools before a repeated failure justifies the extra API surface.

## Plan

- [x] Identify the top 5 user workflows from README examples and live research findings: latest plenary meeting bills, law amendment history, legislator proposal record, legislator interpellations, and committee meeting lookup; verify by mapping each workflow to existing tools and required IDs.
- [x] Document date semantics for `latest known`, `latest occurred`, and `next scheduled` queries, including the current-date comparison rule; verify with examples using fixed dates in tests or docs.
- [x] Add MCP prompts for the top workflows if supported by the current FastMCP version; verify by listing prompts through an MCP client or an in-repo prompt registration test.
- [x] Add MCP resources or a compact reference document for supported filter fields, ID fields, and example `output_fields`; verify by matching it against live response metadata such as `supported_filter_fields`.
- [x] Add representative README examples that avoid ambiguous "latest" wording or explicitly say whether scheduled records count; verify with live smoke runs through the configured MCP server.
- [x] Evaluate whether helper tools are needed for common date-bounded queries, such as latest occurred meeting before `today`; verify by comparing prompt-only usability against documented prompt/resource guidance.
- [x] Add smoke-test prompts for the documented workflows using stable low-volume queries and record expected output shape; verify with prompt/resource registration tests and representative live MCP smoke calls.

## Risks

- Prompts/resources may be supported differently across MCP clients, so README examples remain important.
- Date semantics can be sensitive to timezone; use Asia/Taipei dates when comparing Legislative Yuan records.
- Helper tools can duplicate API features and increase maintenance cost; prefer prompts/resources until a concrete repeated failure justifies a helper.

## Completion Checklist

- [x] Common workflows are documented as executable MCP prompts or README examples, verified by a reviewer running at least two examples.
- [x] "Latest" query semantics distinguish occurred and scheduled records, verified by docs or tests using fixed dates.
- [x] Filter and ID discovery is available without reading raw code, verified by MCP resources or README/developer docs.
- [x] Any helper tools added for date-bounded queries have tests and clear non-overlap with raw list tools. No helper tools were added in this pass.
