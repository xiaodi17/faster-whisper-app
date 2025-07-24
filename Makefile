.PHONY: help install dev start test lint format clean build

# Default target
help: ## Show this help message
	@echo "🚀 Faster-Whisper App - Development Commands"
	@echo "=============================================="
	@echo ""
	@echo "Setup Commands:"
	@echo "  install     Install the project in development mode"
	@echo "  install-uv  Install using uv (modern, recommended)"
	@echo ""
	@echo "Development Commands:"
	@echo "  start       Start the application"
	@echo "  dev         Run full development workflow (format + lint + test + start)"
	@echo "  test        Run all tests"
	@echo "  test-fast   Run tests until first failure"
	@echo ""
	@echo "Code Quality:"
	@echo "  format      Format code with black, isort, ruff"
	@echo "  lint        Lint code with ruff and mypy"
	@echo "  fix         Auto-fix linting issues"
	@echo ""
	@echo "Utilities:"
	@echo "  clean       Clean build artifacts and cache"
	@echo "  build       Build distributable package"
	@echo "  config      Show current configuration"
	@echo ""
	@echo "uv Commands (if uv is installed):"
	@echo "  uv-start    Start with uv"
	@echo "  uv-dev      Full dev workflow with uv"
	@echo "  uv-test     Run tests with uv"

# Installation commands
install: ## Install the project in development mode with pip
	pip install -e ".[dev]"
	@echo "✅ Project installed in development mode"

install-uv: ## Install the project using uv (recommended)
	@if command -v uv >/dev/null 2>&1; then \
		uv sync; \
		echo "✅ Project installed with uv"; \
	else \
		echo "❌ uv not found. Install it with: curl -LsSf https://astral.sh/uv/install.sh | sh"; \
		exit 1; \
	fi

# Development commands
start: ## Start the application
	@if command -v uv >/dev/null 2>&1; then \
		uv run faster-whisper-app run; \
	elif command -v faster-whisper-app >/dev/null 2>&1; then \
		faster-whisper-app run; \
	else \
		python -m faster_whisper_app; \
	fi

dev: format lint test start ## Run full development workflow

# Testing commands
test: ## Run all tests
	@if command -v uv >/dev/null 2>&1; then \
		uv run pytest tests/ -v; \
	else \
		pytest tests/ -v; \
	fi

test-fast: ## Run tests until first failure
	pytest tests/ -x

test-cov: ## Run tests with coverage report
	pytest tests/ --cov=faster_whisper_app --cov-report=html
	@echo "📊 Coverage report generated in htmlcov/"

# Code quality commands
format: ## Format code with black, isort, and ruff
	@if command -v uv >/dev/null 2>&1; then \
		uv run black src/ tests/; \
		uv run isort src/ tests/; \
		uv run ruff format src/ tests/; \
	else \
		black src/ tests/; \
		isort src/ tests/; \
		ruff format src/ tests/; \
	fi
	@echo "✨ Code formatted"

lint: ## Lint code with ruff and mypy
	@if command -v uv >/dev/null 2>&1; then \
		uv run ruff check src/ tests/; \
		uv run mypy src/; \
	else \
		ruff check src/ tests/; \
		mypy src/; \
	fi
	@echo "🔍 Linting complete"

fix: ## Auto-fix linting issues
	ruff check src/ tests/ --fix
	black src/ tests/
	isort src/ tests/
	@echo "🔧 Auto-fixes applied"

# Build and clean commands
clean: ## Clean build artifacts and cache
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf *.spec
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	rm -rf htmlcov/
	find . -type d -name __pycache__ -delete
	@echo "🧹 Cleaned build artifacts"

build: ## Build distributable package
	python -m build
	@echo "📦 Package built in dist/"

build-exe: ## Build standalone executable with PyInstaller
	@if command -v uv >/dev/null 2>&1; then \
		uv run python build.py; \
	else \
		python build.py; \
	fi

clean-build: ## Clean PyInstaller build artifacts
	@if command -v uv >/dev/null 2>&1; then \
		uv run python build.py clean; \
	else \
		python build.py clean; \
	fi

# Configuration and info
config: ## Show current configuration
	@if command -v faster-whisper-app >/dev/null 2>&1; then \
		faster-whisper-app config; \
	else \
		python -m faster_whisper_app.cli config; \
	fi

info: ## Show project information
	@echo "🎙️ Faster-Whisper App"
	@echo "===================="
	@echo "Python version: $$(python --version)"
	@echo "Project root: $$(pwd)"
	@echo "Virtual env: $$(echo $$VIRTUAL_ENV)"
	@echo ""
	@echo "Dependencies status:"
	@python -c "import sys; print('✅ Python OK')" 2>/dev/null || echo "❌ Python issue"
	@python -c "import faster_whisper; print('✅ faster-whisper OK')" 2>/dev/null || echo "❌ faster-whisper not found"
	@python -c "import pyaudio; print('✅ PyAudio OK')" 2>/dev/null || echo "❌ PyAudio not found"
	@python -c "import keyboard; print('✅ keyboard OK')" 2>/dev/null || echo "❌ keyboard not found"

# uv-specific commands (if uv is available)
uv-start: ## Start the application with uv
	uv run start

uv-dev: ## Run full development workflow with uv
	uv run dev

uv-test: ## Run tests with uv
	uv run test

uv-format: ## Format code with uv
	uv run format

uv-lint: ## Lint code with uv
	uv run lint

# Component testing
test-transcriber: ## Test transcriber component
	python src/faster_whisper_app/core/transcriber.py

test-recorder: ## Test recorder component
	python src/faster_whisper_app/core/recorder.py

test-cli: ## Test CLI component
	python src/faster_whisper_app/cli.py test

# Quick setup for new developers
setup: ## One-command setup for new developers
	@echo "🚀 Setting up Faster-Whisper App..."
	@if command -v uv >/dev/null 2>&1; then \
		echo "📦 Using uv for setup..."; \
		uv sync; \
		echo "✅ Setup complete with uv!"; \
		echo "🎯 Run 'make uv-start' or 'uv run start' to begin"; \
	else \
		echo "📦 Using pip for setup..."; \
		pip install -e ".[dev]"; \
		echo "✅ Setup complete with pip!"; \
		echo "🎯 Run 'make start' or 'faster-whisper-app' to begin"; \
	fi