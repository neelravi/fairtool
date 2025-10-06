# fairtool/cli.py

"""Main CLI entry point for the FAIR tool."""

import typer
from typing_extensions import Annotated
from pathlib import Path
import logging
import rich
import sys
from rich.logging import RichHandler
# Import subcommand functions
from . import parse as parse_module
from . import analyze as analyze_module
from . import summarize as summarize_module
from . import visualize as visualize_module
from . import export as export_module
from . import __version__

console = rich.console.Console()

# Configure logging
logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(show_path=False, rich_tracebacks=True, markup=True, keywords=["error", "failed", "success", "warning"], tracebacks_suppress=[typer])]
)
log = logging.getLogger("fairtool")

# Create the Typer application
app = typer.Typer(
    name="fair",
    help="Process, Analyze, Visualize, and Export Computational Materials Data.",
    add_completion=True,
    no_args_is_help=True,
    callback=None,
)


# --- Typer Command Definitions ---
@app.command()
def about():
    """
    Information about the FAIR Tool and its creators.
    """
    console.print("")
    console.print("")
    console.rule()
    console.print("FAIR Tool - Computational Materials Data Processing made FAIR", style="bold magenta")
    console.print(r"""
  █████▒ ▄▄▄       ██▓ ██▀███  ▄▄▄█████▓ ▒█████   ▒█████   ██▓
▓██   ▒ ▒████▄    ▓██▒▓██ ▒ ██▒▓  ██▒ ▓▒▒██▒  ██▒▒██▒  ██▒▓██▒
▒████ ░ ▒██  ▀█▄  ▒██▒▓██ ░▄█ ▒▒ ▓██░ ▒░▒██░  ██▒▒██░  ██▒▒██░
░▓█▒  ░ ░██▄▄▄▄██ ░██░▒██▀▀█▄  ░ ▓██▓ ░ ▒██   ██░▒██   ██░▒██░
░▒█░     ▓█   ▓██▒░██░░██▓ ▒██▒  ▒██▒ ░ ░ ████▓▒░░ ████▓▒░░██████▒
 ▒ ░     ▒▒   ▓▒█░░▓  ░ ▒▓ ░▒▓░  ▒ ░░   ░ ▒░▒░▒░ ░ ▒░▒░▒░ ░ ▒░▓  ░
 ░        ▒   ▒▒ ░ ▒ ░  ░▒ ░ ▒░    ░      ░ ▒ ▒░   ░ ▒ ▒░ ░ ░ ▒  ░
 ░ ░      ░   ▒    ▒ ░  ░░   ░   ░      ░ ░ ░ ▒  ░ ░ ░ ▒    ░ ░
              ░  ░ ░     ░                  ░ ░      ░ ░      ░  ░
    """, style="dark_orange")
    console.print("FAIR Tool is a command-line interface for processing, analyzing, and visualizing computational materials data.", style="cyan")
    console.print("It is designed to work with various calculation output files and provides a streamlined workflow.", style="cyan")
    console.print("The tool is built on top of electronic-parsers and other libraries to facilitate data handling.", style="cyan")
    console.print("")
    console.print("Version: " + str(__version__), style="orange1")
    console.print("")
    console.print("Author: Dr. Ravindra Shinde", style="orange1")
    console.print("Email : r.l.shinde@utwente.nl", style="orange1")
    console.print("")
    console.print("")
    console.print("Funding: " + "4TU Research Data Fund 2024", style="orange1")
    console.print("")
    console.rule()
    console.print("")



# --- Helper Functions ---

def _find_calc_files(path: Path) -> list[Path]:
    """Finds relevant calculation files in a directory or returns the file itself."""
    files_to_process = []
    if not path.exists():
        log.error(f"Error: Input path does not exist: {path}")
        raise typer.Exit(code=1)

    if path.is_file():
        # TODO: Add more sophisticated file type checking if needed
        files_to_process.append(path)
    elif path.is_dir():
        # TODO: Implement logic to find relevant files (e.g., VASP OUTCAR, QE output)
        # This is a placeholder - customize based on expected file names/extensions
        log.info(f"Searching for calculation files in directory: {path}")
        # Example: find all files named 'OUTCAR' or ending with '.out'
        potential_files = list(path.rglob("OUTCAR")) + list(path.rglob("*.out"))
        if not potential_files:
             log.warning(f"No potential calculation files found in {path}")
        files_to_process.extend(potential_files)
        # Add more specific file finding logic here based on electronic-parsers capabilities
    else:
        log.error(f"Error: Input path is neither a file nor a directory: {path}")
        raise typer.Exit(code=1)

    if not files_to_process:
         log.warning(f"No files identified for processing at path: {path}")

    return files_to_process

def version_callback(value: bool):
    """Prints the version and exits."""
    if value:
        rich.print(f"FAIR Tool Version: {__version__}")
        raise typer.Exit()



@app.command()
def parse(
    input_path: Annotated[Path, typer.Argument(
        help="Path to a calculation output file or a directory containing them.",
        exists=True, # Typer checks if it exists, but we double-check type later
        file_okay=True,
        dir_okay=True,
        resolve_path=True, # Converts to absolute path
    )],
    output_dir: Annotated[Path, typer.Option(
        "--output", "-o",
        help="Directory to save parsed JSON and Markdown files.",
        resolve_path=True,
    )] = Path("./fair"),
    force: Annotated[bool, typer.Option(
        "--force", "-f",
        help="Overwrite existing output files."
    )] = True,
):
    """
    Parse calculation output files into structured JSON and Markdown.
    Uses electronic-parsers.
    """
    log.info(f"Starting parsing process for: {input_path}")
    output_dir.mkdir(parents=True, exist_ok=True)
    log.info(f"Output will be saved to: {output_dir}")

    files_to_process = _find_calc_files(input_path)
    if not files_to_process:
        log.warning("No files found to parse.")
        return # Exit gracefully

    for file in files_to_process:
        log.info(f"Parsing file: {file}")
        try:
            parse_module.run_parser(file, output_dir, force)
        except Exception as e:
            log.error(f"Failed to parse {file}: {e}", exc_info=True)
            # Optionally continue to next file or exit
            # raise typer.Exit(code=1)

    log.info("Parsing finished.")


@app.command()
def analyze(
    input_path: Annotated[Path, typer.Argument(
        help="Path to a parsed JSON file or a directory containing them (usually from 'fair parse').",
        exists=True,
        file_okay=True,
        dir_okay=True,
        resolve_path=True,
    )],
     output_dir: Annotated[Path, typer.Option(
        "--output", "-o",
        help="Directory to save analysis results (e.g., plots, summary tables).",
        resolve_path=True,
    )] = Path("./fair_output/analyzed"),
     config: Annotated[Path, typer.Option(
        "--config", "-c",
        help="Path to an optional analysis configuration file (e.g., YAML).",
        exists=True,
        file_okay=True,
        dir_okay=False,
        resolve_path=True,
    )] = None,
):
    """
    Perform analysis on parsed calculation data.
    (Example: Calculate band gap, density of states features, etc.)
    """
    log.info(f"Starting analysis process for: {input_path}")
    output_dir.mkdir(parents=True, exist_ok=True)
    log.info(f"Analysis output will be saved to: {output_dir}")
    if config:
        log.info(f"Using analysis configuration: {config}")

    # TODO: Implement logic to find relevant JSON files if input_path is a directory
    # Similar to _find_calc_files but looking for *.json or specific names

    # Placeholder for actual analysis
    try:
        log.info("Analysis started.")
        analyze_module.run_analysis(input_path, output_dir, config)
    except Exception as e:
        log.error(f"Analysis failed for {input_path}: {e}", exc_info=True)
        raise typer.Exit(code=1)

    log.info("Analysis finished.")


@app.command()
def summarize(
    input_path: Annotated[Path, typer.Argument(
        help="Path to parsed/analyzed data (JSON/directory) to summarize.",
         exists=True,
        file_okay=True,
        dir_okay=True,
        resolve_path=True,
    )],
    output_dir: Annotated[Path, typer.Option(
        "--output", "-o",
        help="Directory to save summary files (e.g., Markdown reports).",
        resolve_path=True,
    )] = Path("./fair_output/summarized"),
    template: Annotated[str, typer.Option(
        "--template", "-t",
        help="Optional template for generating the summary report."
    )] = None,
):
    """
    Generate human-readable summaries from parsed or analyzed data.
    (Example: Create a Markdown report with key findings).
    """
    log.info(f"Starting summarization process for: {input_path}")
    output_dir.mkdir(parents=True, exist_ok=True)
    log.info(f"Summary output will be saved to: {output_dir}")
    if template:
        log.info(f"Using summary template: {template}")

    # TODO: Implement logic to find relevant input files if input_path is a directory

    try:
        log.info("Summarization started.")
        summarize_module.run_summarization(input_path, output_dir, template)
    except Exception as e:
        log.error(f"Summarization failed for {input_path}: {e}", exc_info=True)
        raise typer.Exit(code=1)

    log.info("Summarization finished.")


@app.command()
def visualize(
    input_path: Annotated[Path, typer.Argument(
        help="Path to parsed data (JSON/directory) containing structures, BZ, etc.",
         exists=True,
        file_okay=True,
        dir_okay=True,
        resolve_path=True,
    )],
    output_dir: Annotated[Path, typer.Option(
        "--output", "-o",
        help="Directory to save visualization data (e.g., JSON for React components) and potentially Markdown snippets.",
        resolve_path=True,
    )] = Path("./fair_output/visualized"),
    embed: Annotated[bool, typer.Option(
        "--embed", "-e",
        help="Generate Markdown snippets for embedding visualizations in mkdocs.",
    )] = False,
):
    """
    Generate data for visualizations (structures, BZ, DOS, bands).
    Optionally creates Markdown snippets for mkdocs embedding.
    """

    log.info(f"Starting visualization data generation for: {input_path}")
    output_dir.mkdir(parents=True, exist_ok=True)
    log.info(f"Visualization data will be saved to: {output_dir}")
    if embed:
        log.info("Will generate Markdown embedding snippets.")

    # TODO: Implement logic to find relevant input files if input_path is a directory

    try:
        log.info("Visualization data generation started.")
        visualize_module.run_visualization(input_path, output_dir, embed)
    except Exception as e:
        log.error(f"Visualization data generation failed for {input_path}: {e}", exc_info=True)
        raise typer.Exit(code=1)

    log.info("Visualization data generation finished.")


@app.command()
def export(
    input_path: Annotated[Path, typer.Argument(
        help="Path to parsed/analyzed data (JSON/directory) to export.",
         exists=True,
        file_okay=True,
        dir_okay=True,
        resolve_path=True,
    )],
    output_dir: Annotated[Path, typer.Option(
        "--output", "-o",
        help="Directory to save exported files.",
        resolve_path=True,
    )] = Path("./fair_output/exported"),
    format: Annotated[str, typer.Option(
        "--format", "-fmt",
        help="Export format (e.g., 'csv', 'json_summary', 'yaml').",
    )] = "csv",
):
    """
    Export processed data into different file formats.
    """
    log.info(f"Starting export process for: {input_path}")
    output_dir.mkdir(parents=True, exist_ok=True)
    log.info(f"Exported files will be saved to: {output_dir} in format '{format}'")

    # TODO: Implement logic to find relevant input files if input_path is a directory

    try:
        log.info("Export started.")
        export_module.run_export(input_path, output_dir, format)
    except Exception as e:
        log.error(f"Export failed for {input_path} (format: {format}): {e}", exc_info=True)
        raise typer.Exit(code=1)

    log.info("Export finished.")


# --- Version Callback ---

@app.callback()
def main_callback(
    version: Annotated[
        bool, typer.Option("--version", "-v", callback=version_callback, is_eager=True, help="Show version and exit.")
    ] = False,
):
    """
    FAIR Tool main command group.
    """
    # This callback runs before any command.
    # We use it mainly for the --version flag.
    pass


if __name__ == "__main__":
    # This allows running the script directly for debugging,
    # although `python -m fairtool` or the installed `fair` command is preferred.
    app()

