lint:
	uv run ruff check .

type:
	uv run mypy --install-types --non-interactive .

test:
	uv run pytest -v -s --cov=src tests

dev:
	uv run mcp dev src/lymcp/server.py

publish:
	uv build -f wheel
	uv publish

.PHONY: lint test publish
