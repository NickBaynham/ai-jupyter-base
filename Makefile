.PHONY: help install update lock test test-unit lint format typecheck quality \
	run-jupyter stop-jupyter run-jupyter-docker stop-jupyter-docker build-docker clean

PY ?= python3
JUPYTER_PORT ?= 8888
# Set to a non-empty value to unset OPENAI_API_KEY for the Lab process (use with JUPYTER_BASE_OPENAI_KEY_FILE).
JUPYTER_STRIP_OPENAI_ENV ?=
COMPOSE ?= docker compose

help: ## Show available Make targets
	@grep -E '^[a-zA-Z0-9_.-]+:.*?##' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-22s\033[0m %s\n", $$1, $$2}'

install: ## Install locked dependencies (dev, test, notebook groups)
	pdm sync -G dev -G test -G notebook

update: ## Update dependencies and refresh the lock file
	pdm update

lock: ## Regenerate pdm.lock from pyproject.toml
	pdm lock

test: ## Run the full test suite
	pdm run pytest

test-unit: ## Run only unit tests
	pdm run pytest tests/unit

lint: ## Run Ruff linter
	pdm run ruff check src tests

format: ## Format code with Ruff
	pdm run ruff format src tests

typecheck: ## Run mypy on the backend package
	pdm run mypy src/jupyter_base

quality: lint format-check typecheck test ## Lint, verify formatting, typecheck, and test

format-check: ## Fail if Ruff would reformat files
	pdm run ruff format --check src tests

run-jupyter: ## Start JupyterLab locally (project env, notebooks/ as cwd)
	@if [ -n "$(JUPYTER_STRIP_OPENAI_ENV)" ]; then \
		env -u OPENAI_API_KEY JUPYTERLAB_SETTINGS_DIR="$(CURDIR)/jupyter/lab/user-settings" \
			pdm run jupyter lab --notebook-dir=notebooks --port=$(JUPYTER_PORT) --no-browser; \
	else \
		JUPYTERLAB_SETTINGS_DIR="$(CURDIR)/jupyter/lab/user-settings" \
			pdm run jupyter lab --notebook-dir=notebooks --port=$(JUPYTER_PORT) --no-browser; \
	fi

stop-jupyter: ## Stop local JupyterLab processes started for this repo
	-pkill -f "jupyter-lab.*--notebook-dir=notebooks" || true

run-jupyter-docker: ## Build (if needed) and start Jupyter in Docker (detached)
	$(COMPOSE) up -d --build jupyter

stop-jupyter-docker: ## Stop Jupyter Docker service
	$(COMPOSE) down

build-docker: ## Build the Jupyter Docker image
	$(COMPOSE) build jupyter

clean: ## Remove common build, cache, and coverage artifacts
	rm -rf .pytest_cache .mypy_cache .ruff_cache htmlcov .coverage dist build
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
