install:
	poetry install

test:
	poetry run pytest

build: check
	poetry build

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install --user dist/*.whl

lint:
	poetry run flake8 gendiff

selfcheck:
	poetry check

check: selfcheck test lint

test-coverage:
	poetry run pytest --cov=page_loader --cov-report xml

.PHONY: install test lint selfcheck check build
