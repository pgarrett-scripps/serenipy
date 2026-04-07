# Default target
default:
    @just --list

# Install dependencies (with dev group)
install:
    uv sync

# Install without dev dependencies
install-prod:
    uv sync --no-dev

# Alias for install
sync:
    uv sync

# Run tests
test:
    uv run pytest tests/ -v

# Run linter
lint:
    uv run ruff check src/ tests/

# Format code (import sort, unused-import fix, then format)
format:
    uv run ruff check --select I --fix src/ tests/
    uv run ruff check --select F401 --fix src/ tests/
    uv run ruff format src/ tests/

# Type-check with ty
ty:
    uv run ty check src/

# Run lint, type check, and tests
check:
    just lint
    just ty
    just test

# Build the package
build:
    uv build

# Clean build artifacts and caches
clean:
    rm -rf build/ dist/ *.egg-info src/*.egg-info
    rm -rf .pytest_cache .ruff_cache .ty_cache .mypy_cache
    rm -rf htmlcov/ .coverage coverage.xml
    find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
    find . -type f -name "*.pyc" -delete
