## Goal

Move live Legislative Yuan API tests out of the default CI path and add offline mock tests backed by checked-in JSON samples under `tests/data`. Success means pull requests can run lint, type check, and deterministic mock tests without network dependency, while default pytest runs skip `live` tests unless `-m live` is specified.

## Context

The current `CI` workflow runs `uv run pytest -v -s --cov=src --cov-report=xml tests` on `push`, `pull_request`, and `workflow_dispatch`. Before this migration, the existing API and MCP server tests called the real `https://ly.govapi.tw/v2` service during normal test runs, which made CI depend on external data shape, network availability, and API latency.

## Non-Goals

- Do not remove live API tests; keep them available for explicit manual validation.
- Do not make broad production API changes only for tests unless the mock strategy cannot cover the server path without it.
- Do not try to capture every endpoint before the first mock-test PR; start with representative samples and expand by category.

## Assumptions

- JSON fixture files in `tests/data` are acceptable in the repository if they are small, deterministic, and named by endpoint or tool intent.
- Mock tests can validate request serialization, response handling, and MCP tool output shape without requiring the live API on every PR.
- Live tests can be selected by pytest markers instead of maintaining a separate test suite with duplicated assertions.

## Unknowns

- Resolved: existing subprocess MCP server tests remain marked `live`, and the default offline suite uses in-process server wrapper tests with monkeypatched request classes.

## Plan

- [x] Audit all existing tests in `tests/test_api.py` and `tests/test_server.py` to classify each test as offline-safe, live-only, or convertible to fixture-backed mock; verified by marking existing real API tests as `live` and adding separate `tests/test_api_mock.py` and `tests/test_server_mock.py`.
- [x] Add a `live` pytest marker and collection hook so live tests are skipped by default and selected explicitly with `-m live`; verified with `uv run pytest tests` and `uv run pytest -m live --collect-only tests`.
- [x] Create `tests/data/` with representative JSON samples captured from stable, low-volume calls such as `stat`, `bills?term=11&limit=1`, one bill detail, one gazette list/detail, one legislator list/detail, one law detail, and one meeting lookup; verified with `python -m json.tool` over `tests/data/*.json`.
- [x] Add a fixture-loading helper, for example `tests/fixtures.py` or `tests/conftest.py`, to load JSON by logical sample name and fail clearly when a fixture is missing; verified by passing mock tests that load `tests/data` through `tests/fixtures.py`.
- [x] Convert API request tests to use monkeypatched `lymcp.api.make_api_request` responses from `tests/data`, preserving assertions about request parameters and response shape; verified with `uv run pytest tests/test_api_mock.py`.
- [x] Mark real network API tests as `@pytest.mark.live` and keep their current behavior for manual validation; verified with `just test-live`.
- [x] Keep existing subprocess server tests marked as `live`, then add fixture-backed in-process server tool tests for the default offline suite; verified with `uv run pytest tests/test_server_mock.py`.
- [x] Update `.github/workflows/ci.yml` so push and pull request jobs run the default offline suite with coverage, for example `uv run pytest -v -s --cov=src --cov-report=xml tests`; verified by reviewing `.github/workflows/ci.yml`.
- [x] Add or adjust a manual workflow path for live tests using `workflow_dispatch`, either by adding a separate `live-tests` job or a separate workflow file that runs `uv run pytest -v -s -m live tests`; verified by `.github/workflows/live-tests.yml`.
- [x] Document the local commands in `README.md` or a short testing section: default offline tests, manual live tests, and how to refresh fixtures; verified by README testing section updates.
- [x] Run the full local validation set after implementation: `just lint`, `just type`, `uv run pytest -v -s --cov=src tests`, and one explicit `uv run pytest -v -s -m live tests` run before finalizing the PR; verified by `just lint`, `just type`, `just test`, and `just test-live`.

## Risks

- Checked-in samples can drift from the live API, so fixture refresh must be a deliberate maintenance task rather than a hidden CI dependency.
- Mocking only `make_api_request` can miss integration bugs in URL construction if tests do not assert the requested URL and params.
- Server subprocess tests are harder to mock than API class tests; forcing them offline may require a small test seam or a different test strategy.

## Completion Checklist

- [x] Default CI no longer depends on live `ly.govapi.tw` calls, verified by the pytest collection hook skipping `live` tests and `.github/workflows/ci.yml` running normal `pytest` on pull requests.
- [x] Live API tests remain manually runnable, verified by `.github/workflows/live-tests.yml` and local `just test-live`.
- [x] `tests/data` contains valid JSON fixtures for the first converted endpoint set, verified by JSON parser output and fixture-backed tests.
- [x] Mock tests cover the converted request classes without network access, verified by `just test` passing with `73 passed, 81 skipped` and total coverage at 83%.
- [x] Repository quality gates pass after the migration, verified by `just lint`, `just type`, and `just test`.
