# Repository Guidelines

## Project Structure & Module Organization

- `src/lymcp/api.py` contains request models and HTTP calls to `https://ly.govapi.tw/v2`.
- `src/lymcp/server.py` registers FastMCP tools, prompts, and resources.
- `src/lymcp/translate.py` maps internal parameter names to upstream Chinese query fields.
- `tests/test_api_mock.py` and `tests/test_server_mock.py` are default offline tests.
- `tests/test_api.py` and `tests/test_server.py` are live tests marked `@pytest.mark.live`.
- `tests/data/` stores checked-in JSON fixtures for deterministic tests.
- `docs/` contains endpoint audits and archived implementation plans.

## Build, Test, and Development Commands

- `uv sync` installs project and development dependencies.
- `just lint` runs Ruff checks.
- `just type` runs `ty` type checking.
- `just test` runs the offline pytest suite with coverage.
- `just test-live` runs live tests against the Legislative Yuan API.
- `just dev` starts the MCP Inspector for `src/lymcp/server.py`.
- `uv run lymcp` runs the MCP server locally.

## Coding Style & Naming Conventions

Write Python with 4-space indentation and type annotations for public or shared code. Name request classes by action and endpoint, for example `ListBillRequest` or `GetLawVersionRequest`. Keep MCP tool functions snake_case and aligned with endpoint intent, for example `list_bills`.

Ruff enforces a 120-character line length and single-line imports via isort settings. Prefer small local helpers over new dependencies unless they solve a current problem.

## Testing Guidelines

Default tests must be deterministic and offline. Add fixture-backed tests when changing request serialization, server tool wiring, response contracts, prompts, or resources. Name tests by behavior, for example `test_make_api_request_wraps_timeout`.

Use `@pytest.mark.live` only for tests that call the real API or subprocess MCP paths that may call it. Refresh `tests/data/*.json` intentionally when upstream response shape changes.

## Commit & Pull Request Guidelines

Follow the existing Conventional Commit style: `feat(api): ...`, `fix: ...`, `test: ...`, or `docs(plans): ...`. Keep commits focused and avoid mixing unrelated docs, tests, and runtime changes.

Pull requests should include a short summary, verification commands, and notes for any live API behavior. Run at least `just lint`, `just type`, and `just test` before requesting review. Use `just test-live` when the change depends on real upstream API behavior.

## Agent-Specific Instructions

Do not use blanket staging such as `git add -A`; stage only intended paths. Keep edits bounded to this repository and preserve archived plan history unless explicitly asked to rewrite it.
