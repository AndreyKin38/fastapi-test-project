.DEFAULT_GOAL := help

HOST ?= 0.0.0.0
PORT ?= 8000

run:
	uvicorn app.main:app --host $(HOST) --port $(PORT) --reload --env-file $(ENV)

install:
	poetry add $(LIBRARY)

uninstall:
	poetry remove $(LIBRARY)

migrate-create:
	alembic revision --autogenerate -m $(MIGRATION)

migrate-apply:
	alembic upgrade head

migrate-downgrade:
	alembic downgrade base
