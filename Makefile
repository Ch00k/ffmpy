.PHONY: lint test release-patch release-minor release-major

lint:
	uv run ruff format .
	uv run ruff check --fix .
	uv run mypy --config-file pyproject.toml ffmpy/ tests/

test:
	uv run pytest -s -vvv --cov --cov-branch --cov-report=xml tests/

release-patch:
	./release.sh patch

release-minor:
	./release.sh minor

release-major:
	./release.sh major
