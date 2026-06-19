.PHONY: run test coverage lint format install

install:
	pip install -r requirements.txt

run:
	uvicorn app.main:app --reload

test:
	pytest -v

coverage:
	pytest --cov=app --cov-report=term-missing

lint:
	flake8 app tests

format:
	black .
	isort .