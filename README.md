
# fairtool - Computational Materials Data Processing made FAIR

[![Tests & Coverage](https://github.com/neelravi/fairtool/actions/workflows/python-app.yml/badge.svg)](https://github.com/neelravi/fairtool/actions/workflows/python-app.yml)
[![codecov](https://codecov.io/gh/neelravi/fairtool/branch/main/graph/badge.svg)](https://codecov.io/gh/neelravi/fairtool)
[![Python](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue.svg)](https://www.python.org/)
[![Lint and Code Quality](https://github.com/neelravi/fairtool/actions/workflows/lint.yml/badge.svg)](https://github.com/neelravi/fairtool/actions/workflows/lint.yml)
[![Code style: ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<img width="800" alt="Fairtool" src="./documentation/docs/assets/images/fairtool.png"/>

FAIR Tool is a command-line interface for processing, analyzing, and visualizing computational materials data.
It is designed to work with various calculation output files and provides a streamlined workflow.

#### Project Lead: Dr. Ravindra Shinde
#### Email : r.l.shinde@utwente.nl

#### Contributor: Konstantinos Kontogiannis
#### Email : k.kontogiannis@student.utwente.nl

## Funding: 4TU Research Data Fund 4th Edition

# Installing fairtool with uv

This guide explains how to install the `fairtool` package and its dependencies using [uv](https://github.com/astral-sh/uv), a fast Python package installer and resolver.

## Prerequisites
- **Python 3.11 – 3.14** (*Note: Python <= 3.10 is unsupported because modern upstream scientific dependencies such as `pymatgen` (2026+) and `numpy` require Python 3.11 or newer*)
- [uv](https://github.com/astral-sh/uv) installed (see below)
- Git (optional, for cloning the repository)

## 1. Clone the Repository (if needed)
```bash
git clone https://github.com/neelravi/fairtool.git
cd fairtool
```

## 2. Install uv
If you don't have `uv` installed, run:

```bash
curl -Ls https://astral.sh/uv/install.sh | sh
```

This will install `uv` to `~/.local/bin/uv` by default. Make sure this directory is in your `PATH`.

You may install Python using uv quickly with:

```bash
uv python install 3.11
```

## 3. Create a Virtual Environment with uv
It's recommended to use a virtual environment. You can create one using uv:

```bash
uv venv .venv
source .venv/bin/activate
```

## 4. Install Dependencies with uv
From the project root directory, run:

```bash
uv pip install -r requirements.txt
```

This will install all required dependencies quickly using uv's resolver.

## 5. Install fairtool (Editable/Development Mode)
To install the package in editable mode (recommended for development):

```bash
uv pip install -e .
```

## 6. Run the CLI
You can now run the CLI using:

```bash
fair
```

## Verification & Testing

Verify that your installation, test suite, and site generation pass:

### 1. Run the Test Suite with Coverage
```bash
# Run pytest with code coverage breakdown
pytest --cov=fairtool --cov-report=term-missing
```

### 2. Verify Code Quality with Ruff
```bash
# Check linting and formatting
ruff check fairtool tests
ruff format --check fairtool tests
```

### 3. Verify Static Documentation Build
```bash
# Test site build without launching dev server
fair visualize tests/VASP/ --build
```

## Troubleshooting
- Ensure you are using Python 3.11+ for best compatibility.
- If you see `ModuleNotFoundError: No module named 'fairtool'`, make sure your `PYTHONPATH` includes the project root.
- If `uv` is not found, ensure `~/.local/bin` is in your `PATH`.

## References
- [uv documentation](https://github.com/astral-sh/uv)
- [fairtool repository](https://github.com/neelravi/fairtool)

