setup:
	uv sync --all-groups

run:
	uv run uvicorn app.main:app --reload

test:
	uv run pytest

fmt:
	uv run ruff check --fix .
	uv run ruff format .

db-reset:
	rm -f solo_table.db
