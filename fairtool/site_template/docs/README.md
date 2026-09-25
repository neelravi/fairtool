# FAIR Tool - Computational Materials Data made FAIR


<p align="center">
    <img src="./assets/images/fairtool.png" alt="FAIR Tool Wider Logo" style="max-width:100%; height:auto;" />
</p>

**Project Lead: [Dr. Ravindra Shinde](https://www.ravindrashinde.com)**

Email : r.l.shinde@utwente.nl

**Contributor: Konstantinos Kontogiannis**

Email : k.kontogiannis@student.utwente.nl


License: [MIT License](https://opensource.org/licenses/MIT)

This repository contains the code for an effective **Data Management** for computational research. 

Fairtool is a command-line interface for processing, analyzing, and visualizing computational materials data.
It is designed to work with various calculation output files and provides a streamlined workflow.

This code follows the FAIR principles for data management: data should be Findable, Accessible, Interoperable, and Reusable. The generated data is organized into the following sections:

## Organization of the data

This following sections showcase how a complex computational materials science calculation output be converted into simpler reusable formats and can be quickly visualized using the built-in tools provided with this code. 


## Funding: 4TU Research Data Fund 4th Edition



## Installing fairtool with uv

This guide explains how to install the `fairtool` package and its dependencies using [uv](https://github.com/astral-sh/uv), a fast Python package installer and resolver.

## Prerequisites
- **Python 3.11 – 3.14** (Python 3.10 and earlier are no longer supported)
- **libmagic**, a system library that `fair parse` uses to detect file types:
    - macOS: `brew install libmagic` ([Homebrew](https://brew.sh)), or `sudo port install file` ([MacPorts](https://www.macports.org))
    - Debian/Ubuntu: the `libmagic1` package, usually already installed (if not, `sudo apt install libmagic1`)
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

## Troubleshooting
- Ensure you are using Python 3.11 or later (3.11 through 3.14) for best compatibility.
- If `fair parse` fails with `ImportError: failed to find libmagic`, install libmagic (see [Prerequisites](#prerequisites)).
- If you see `ModuleNotFoundError: No module named 'fairtool'`, make sure your `PYTHONPATH` includes the project root.
- If `uv` is not found, ensure `~/.local/bin` is in your `PATH`.

## References
- [uv documentation](https://github.com/astral-sh/uv)
- [fairtool repository](https://github.com/neelravi/fairtool)
