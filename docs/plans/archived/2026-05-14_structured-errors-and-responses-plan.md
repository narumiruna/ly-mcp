## Goal

Improve response and error semantics so MCP clients and tests can distinguish successful data, empty results, invalid parameters, upstream HTTP failures, timeouts, and non-JSON responses. Success means tool failures are returned in a consistent, machine-checkable shape instead of arbitrary plain strings.

## Status

Completed. Successful tool output remains the raw upstream payload, while
failures now return a consistent JSON error envelope.

## Context

At planning time, the API helper called `resp.raise_for_status()` and `resp.json()` directly. Server tools caught all exceptions and returned strings like `Failed to list bills, got: ...`. That kept the MCP server from crashing, but it made errors hard for clients, tests, and users to interpret.

## Architecture

Keep `httpx` and the request model layer. Introduce a small local response/error helper rather than a new dependency:

- API layer normalizes upstream HTTP and JSON failures.
- Server layer serializes a consistent success or error envelope.
- Tests assert the envelope and error categories.

## Non-Goals

- Do not redesign the transport or replace FastMCP.
- Do not hide the original Legislative Yuan API payload on successful calls.
- Do not invent domain-specific summaries for every endpoint in this phase.

## Assumptions

- Returning JSON text content is acceptable for MCP compatibility, as long as the JSON shape is consistent.
- Existing users can tolerate additional metadata fields if the original payload remains present.
- Successful tool output remains the raw upstream API payload in this pass. Structured envelopes are applied to errors only, preserving existing successful-client behavior while making failures machine-checkable.

## Plan

- [x] Define a minimal response contract for tool output, using raw upstream payloads for success and `{ "ok": false, "error": { "type": "...", "message": "...", "status_code": ... } }` for failures; verify by documenting the contract in README.
- [x] Add local exception classes or result helpers in `src/lymcp/api.py` for HTTP status errors, timeout/network errors, and JSON parse errors; verify with unit tests using monkeypatched `httpx.AsyncClient`.
- [x] Update server tool wrappers to serialize structured errors consistently while preserving successful raw payloads; verify with representative MCP tool tests for success and failure.
- [x] Preserve enough upstream detail for debugging, including endpoint URL path, status code, and response excerpt when safe; verify with tests that assert structured error fields instead of traceback-only messages.
- [x] Add tests for invalid bill ID, invalid law version ID, timeout, and non-JSON upstream response; verify with deterministic tests that do not call the live API.
- [x] Update README or developer docs to explain how MCP clients should interpret error `ok` and `error`; verify by matching docs to tests.

## Risks

- Changing the success envelope may be a breaking change for clients that expect the raw API object at the top level.
- Including upstream response excerpts can leak noisy or overly large data; cap excerpts and avoid full HTML bodies.
- Too much abstraction in error handling could make this small wrapper harder to read; keep helper APIs minimal.

## Rollback / Recovery

- If the success envelope is too disruptive, keep raw successful payloads unchanged and apply the structured envelope only to errors.
- If downstream clients rely on exact text errors, release the change with a minor-version note and examples.

## Completion Checklist

- [x] MCP tool errors are consistently machine-checkable, verified by tests for HTTP 404, timeout, and non-JSON responses.
- [x] Successful responses remain usable by existing clients or have documented migration notes, verified by README examples and tests.
- [x] Error messages include actionable endpoint/status context without raw tracebacks, verified by failure-path tests.
- [x] Quality gates pass after the change, verified by `just lint`, `just type`, and `just test`.
