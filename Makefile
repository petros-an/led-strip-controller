checks: format lint mypy tests
	echo "All checks passed"

format:
	ruff format

lint:
	ruff check --fix

mypy:
	mypy --ignore-missing-imports .

tests: FORCE
	pytest .

FORCE: ;