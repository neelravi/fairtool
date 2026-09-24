# Contributing to FAIRTool

Thank you for your interest in contributing to **FAIRTool**! We welcome contributions that improve features, documentation, tests, and reproducibility for computational materials science data.

## Development Setup

1. **Fork and clone the repository:**
   ```bash
   git clone https://github.com/neelravi/fairtool.git
   cd fairtool
   ```

2. **Set up a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. **Install the package in editable mode with development and test dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -e .[dev]
   ```

4. **Set up pre-commit hooks:**
   ```bash
   pre-commit install
   ```

## Running Tests and Checking Coverage

We use `pytest` and `pytest-cov` to ensure software reliability and sustainability:

```bash
# Run test suite
pytest

# Run tests with code coverage report
pytest --cov=fairtool --cov-report=term-missing
```

Ensure all existing and new tests pass before submitting a pull request.

## Code Quality & Formatting

We use [Ruff](https://astral.sh/ruff) for linting and formatting:

```bash
# Check linting
ruff check .

# Automatically apply safe fixes
ruff check --fix .

# Check formatting
ruff format --check .
```

## Documentation

Documentation is built with `mkdocs-material`:

```bash
# Build and serve the documentation locally
fair visualize tests/VASP/ --serve
```

The site template that `fair visualize` uses (`mkdocs.yml`, `macros.py`, theme overrides, hooks and static assets) lives in `fairtool/site_template/`. It ships inside the package as package data, so edits there apply to both source checkouts and installed wheels.

## Pull Request Guidelines

1. Create a feature branch with a descriptive name: `git checkout -b feature/my-feature`.
2. Write unit tests for new logic and bug fixes in the `tests/` directory.
3. Keep pull requests focused on a single change.
4. Verify that linting and tests pass locally before opening a pull request.
