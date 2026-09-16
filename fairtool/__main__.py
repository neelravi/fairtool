# fairtool/__main__.py

"""
Allows running the CLI via `python -m fairtool`.
"""

from .cli import app

if __name__ == "__main__":
    app(prog_name="fairtool")  # Use 'fairtool' when run this way
