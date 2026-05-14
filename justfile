lint:
    uv run ruff check .

type:
    uv run ty check .

test:
    uv run pytest -v -s --cov=src tests

test-live:
    uv run pytest -v -s -m live tests

dev:
    uv run mcp dev src/lymcp/server.py

publish:
    uv build -f wheel
    uv publish
