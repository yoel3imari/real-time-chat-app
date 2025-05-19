# ---- CONFIG ----
VENV := .venv
PYTHON := $(VENV)/bin/python
UV := uv
UVICORN := $(VENV)/bin/uvicorn
APP := main:app
HOST := 0.0.0.0
PORT := 8000

# ---- TARGETS ----

.PHONY: help
help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Available targets:"
	@echo "  venv         Create virtual environment using uv"
	@echo "  install      Install dependencies from pyproject.toml"
	@echo "  dev          Run FastAPI dev server with reload"
	@echo "  lint         Run ruff linter"
	@echo "  fmt          Format code with black"
	@echo "  clean        Remove virtual environment"

venv:
	$(UV) venv $(VENV)

source:
	source $(VENV)/bin/activate

install:
	$(UV) pip install

dev:
	$(UVICORN) $(APP) --reload --host $(HOST) --port $(PORT)

lint:
	$(VENV)/bin/ruff check .

fmt:
	$(VENV)/bin/black .

clean:
	rm -rf $(VENV)
