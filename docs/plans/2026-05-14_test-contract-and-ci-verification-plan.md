## Goal

Make test and CI behavior match the documented offline/live split, and strengthen MCP contract tests so broken tools fail deterministically. Success means default validation does not require network access, live tests remain explicitly runnable, and tests assert JSON structure, request serialization, and error semantics instead of only checking for strings.

## Status

Completed. Default validation is offline, live tests remain explicit, and mock
server tests assert parsed JSON contracts plus tool-to-request wiring.

## Context

An existing completed plan, `docs/plans/2026-05-14_manual-live-and-mock-tests-plan.md`, already described a live/mock test migration. At planning time, the repository still needed a follow-up verification pass because the research review found mismatch risks between README claims, `justfile`, pytest marker behavior, and tests that asserted only `isinstance(response_text, str)`.

## Non-Goals

- Do not delete live tests.
- Do not require live Legislative Yuan API access in default CI.
- Do not broaden test fixtures to every endpoint before the first contract-hardening pass.

## Unknowns

- Resolved: the completed live/mock split is reflected in `tests/conftest.py`, README testing docs, `justfile`, and GitHub Actions workflows. Default collection includes live tests but marks them skipped unless `-m live` is requested.

## Plan

- [x] Audit current test files, `pyproject.toml`, `justfile`, README testing docs, and CI workflows to verify the actual offline/live split; verify with `uv run pytest --collect-only tests` and `uv run pytest -m live --collect-only tests`.
- [x] If default pytest still collects live tests, add or repair marker filtering so live tests are skipped by default; verify with `just test` running without network access.
- [x] Replace MCP tests that only assert `TextContent` and `str` with assertions that parse JSON and validate top-level keys such as `total`, `page`, `limit`, result collection keys, and `supported_filter_fields`; verify with `uv run pytest tests/test_server*.py`.
- [x] Add request serialization tests for representative filters across bills, meetings, laws, law versions, IVODs, and legislators; verify by monkeypatching `make_api_request` and asserting URL plus params.
- [x] Add error-path tests for invalid IDs, HTTP 404, timeout, and non-JSON responses after structured error handling is implemented; verify with deterministic unit tests that do not call the live API.
- [x] Ensure `just test`, `just test-live`, README testing instructions, and CI workflow commands describe the same behavior; verify by reviewing all four places in one commit.
- [x] Run the final quality gates: `just lint`, `just type`, `just test`, and one explicit `just test-live` before release or PR merge; verify by recording command output in the PR or final implementation summary.

## Risks

- Live API shape changes can make fixture refresh necessary even when production code is correct.
- Subprocess MCP tests are harder to isolate than API class tests; in-process server tests may be needed for deterministic coverage.
- Tests that assert too much of the live payload can become brittle; focus on stable contracts and representative fields.

## Completion Checklist

- [x] Default test execution is offline, verified by `just test` passing with live tests skipped and no network dependency.
- [x] Live tests remain available, verified by `just test-live`.
- [x] MCP server tests validate parsed JSON shape instead of only string type, verified by updated assertions in `tests/test_server_mock.py`.
- [x] Request classes have serialization coverage for high-value filters, verified by unit tests that assert URLs and params.
- [x] README, `justfile`, pytest config, and CI workflow agree on test commands, verified by manual review and passing commands.
