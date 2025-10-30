"""Main CLI entry point for the FAIR tool."""
import os
import typer
from typing_extensions import Annotated
from pathlib import Path
from typing import Optional
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
    console.print("Project Lead: Dr. Ravindra Shinde", style="orange1")
    console.print("Email : r.l.shinde@utwente.nl", style="orange1")
    console.print("")
    console.print("Contributor: Konstantinos Kontogiannis", style="orange1")
    console.print("Email : k.kontogiannis@student.utwente.nl", style="orange1")
    console.print("")
    console.print("Funding: " + "4TU Research Data Fund 4th Edition", style="orange1")
    console.print("")
    console.rule()
    console.print("")



# --- Helper Functions ---

def _find_calc_files(path: Path, recursive: bool = True, assume_yes: bool = False) -> list[Path]:
    """
    Finds relevant calculation files for parsing.

    Args:
        path (Path): The root path or file to inspect.
        recursive (bool): If True, search all subdirectories. If False, only the given directory.
        assume_yes (bool): If True, skip interactive confirmation.

    Returns:
        list[Path]: List of calculation files to process.
    """
    files_to_process = []
    if not path.exists():
        log.error(f"Error: Input path does not exist: {path}")
        raise typer.Exit(code=1)

    if path.is_file():
        # TODO: Add more sophisticated file type checking if needed
        files_to_process.append(path)
        if not assume_yes:
            interactive = sys.stdin.isatty()
            if not interactive:
                log.info("Non-interactive environment detected; proceeding without confirmation.")
            elif not typer.confirm(f"Proceed to process the file {path}? :: "):
                log.info("Aborting file processing as per user request.")
                raise typer.Exit(code=0)

    elif path.is_dir():
        search_method = path.rglob if recursive else path.glob
        potential_files = (
            list(search_method("vasprun.xml")) +
            list(search_method("OUTCAR")) +
            list(search_method("*.XML")) +
            list(search_method("*.xml"))
        )

        # Filter out any files we might have double-counted (e.g., vasprun.xml is also *.xml)
        potential_files = sorted(list(set(potential_files)))


        if not potential_files:
             log.warning(f"No potential calculation files (e.g., vasprun.xml) found in {path}")
        else:
            log.info(f"Found {len(potential_files)} potential calculation files.")
            
            unique_dirs = sorted(set(f.parent for f in potential_files))
            log.info("\n Detected directories with calculation files:")
            
            for d in unique_dirs:
                log.info(f" - {d}")
                for f in potential_files:
                    if f.parent == d:
                        log.info(f"    - {f.name}")

            if not assume_yes:
                interactive = sys.stdin.isatty()
                if not interactive:
                    log.info("Non-interactive environment detected; proceeding without confirmation.")
                elif not typer.confirm(f"Proceed to process all {len(potential_files)} file(s)? :: "):
                    log.info("Aborting file processing as per user request.")
                    raise typer.Exit(code=0)
        
            files_to_process.extend(potential_files)
        
    else:
        log.error(f"Error: Input path is neither a file nor a directory: {path}")
        raise typer.Exit(code=1)

    if not files_to_process:
         log.warning(f"No files identified for processing at path: {path}")

    return files_to_process

def _find_json_files(path: Path, recursive: bool = True) -> list[Path]:
    """
    Finds relevant parsed JSON files (fair_parsed_*.json) for subsequent steps.

    Args:
        path (Path): The root path or file to inspect.
        recursive (bool): If True, search all subdirectories.

    Returns:
        list[Path]: List of JSON files to process.
    """
    files_to_process = []
    if not path.exists():
        log.error(f"Error: Input path does not exist: {path}")
        raise typer.Exit(code=1)

    if path.is_file():
        if path.name.startswith("fair_parsed_") and path.suffix == ".json":
            files_to_process.append(path)
        else:
            log.warning(f"Input file {path} is not a 'fair_parsed_*.json' file. Skipping.")
    
    elif path.is_dir():
        search_method = path.rglob if recursive else path.glob
        potential_files = list(search_method("fair_parsed_*.json"))
        
        if not potential_files:
            log.warning(f"No 'fair_parsed_*.json' files found in {path}")
        else:
            log.info(f"Found {len(potential_files)} parsed JSON files for processing.")
            files_to_process.extend(sorted(potential_files))
    
    return files_to_process


def version_callback(value: bool):
    """Prints the version and exits."""
    if value:
        rich.print(f"FAIR Tool Version: {__version__}")
        raise typer.Exit()



@app.command()
def parse(
    input_path: Annotated[Path, typer.Argument(
        help="Path to a calculation file or directory to search.",
        exists=True,
        file_okay=True,
        dir_okay=True,
        resolve_path=True,
    )] = Path.cwd(), # Default to current working directory

    recursive: Annotated[bool, typer.Option(
        "--recursive", "-r",
        help="Search and parse files recursively through subdirectories."
    )] = False,

    output_dir: Annotated[Optional[Path], typer.Option(
        "--output", "-o",
        help="Directory to save parsed JSON files. "
             "If not given, files are saved next to their originals.",
        resolve_path=True,
    )] = None,

    force: Annotated[bool, typer.Option(
        "--force", "-f",
        help="Overwrite existing output files."
    )] = False, # Default changed to False

    yes: Annotated[bool, typer.Option(
        "--yes", "-y",
        help="Assume yes for all interactive prompts (non-interactive/batch mode)."
    )] = False,
):
    """
    Parse calculation output files (e.g., vasprun.xml) into structured JSON.
    """
    log.info(f"Starting parsing process for: {input_path}")
    log.info(f"Recursive search: {recursive}")

    files_to_process = _find_calc_files(input_path, recursive=recursive, assume_yes=yes)
    if not files_to_process:
        log.warning("No files found to parse.")
        return # Exit gracefully

    count_success = 0
    count_fail = 0
    count_skip = 0

    for file in files_to_process:
        try:
            # If no --output given, use file’s directory
            target_dir = output_dir if output_dir else file.parent
            target_dir.mkdir(parents=True, exist_ok=True)
            
            # The logic to check for existing files and mtime is now
            # handled *inside* parse_module.run_parser.
            # We call it directly.
            
            log.info(f"Parsing file: {file}")
            # run_parser will return True if skipped, False if parsed/failed
            skipped = parse_module.run_parser(file, target_dir, force)
            
            if skipped:
                count_skip += 1
            else:
                count_success += 1
                
        except Exception as e:
            log.error(f"Failed to parse {file}: {e}", exc_info=False) # exc_info=False to reduce noise, parser logs it
            count_fail += 1

    log.info("--- Parsing Finished ---")
    log.info(f"[green]Success: {count_success}[/green]")
    log.warning(f"[yellow]Skipped: {count_skip}[/yellow]")
    log.info(f"[red]Failed:  {count_fail}[/red]")


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
    )] = Path("."),
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
    # For now, we assume run_analysis can handle a directory.
    # json_files = _find_json_files(input_path, recursive=True) # If run_analysis can't handle dirs
    
    try:
        log.info("Analysis started.")
        # We assume run_analysis can handle a directory input_path
        analyze_module.run_analysis(input_path, output_dir, config)
    except Exception as e:
        log.error(f"Analysis failed for {input_path}: {e}", exc_info=True)
        raise typer.Exit(code=1)

    log.info("Analysis finished.")


@app.command()
def summarize(
    input_path: Annotated[Path, typer.Argument(
        help="Path to parsed 'fair_parsed_*.json' data (file or directory).",
         exists=True,
        file_okay=True,
        dir_okay=True,
        resolve_path=True,
    )],
    output_dir: Annotated[Path, typer.Option(
        "--output", "-o",
        help="Directory to save summary files (e.g., Markdown reports). "
             "If not given, files are saved next to their JSON files.",
        resolve_path=True,
    )] = None,
    recursive: Annotated[bool, typer.Option(
        "--recursive", "-r",
        help="Search recursively for JSON files if input_path is a directory."
    )] = True,
    template: Annotated[str, typer.Option(
        "--template", "-t",
        help="Optional template for generating the summary report."
    )] = None,
    force: Annotated[bool, typer.Option(
        "--force", "-f",
        help="Overwrite existing summary files."
    )] = False, # Added force option
):
    """
    Generate human-readable summaries from parsed data.
    """
    log.info(f"Starting summarization process for: {input_path}")
    if template:
        log.info(f"Using summary template: {template}")

    json_files = _find_json_files(input_path, recursive=recursive)
    if not json_files:
        log.warning("No 'fair_parsed_*.json' files found to summarize.")
        return

    log.info(f"Found {len(json_files)} JSON files to summarize.")
    
    count_success = 0
    count_fail = 0
    count_skip = 0

    for json_file in json_files:
        try:
            # If no --output given, use JSON file's directory
            target_dir = output_dir if output_dir else json_file.parent
            target_dir.mkdir(parents=True, exist_ok=True)
            
            # --- Prepare output path ---
            base_name = json_file.stem # e.g., "fair_parsed_my_calc"
            summary_base_name = base_name.replace("fair_parsed_", "fair_summarized_")
            md_output_path = target_dir / f"{summary_base_name}.md"

            if not force and md_output_path.exists():
                log.info(f"Skipping summary for {json_file.name}; output already exists.")
                count_skip += 1
                continue

            log.info(f"Summarizing {json_file.name} -> {md_output_path.name}")
            summarize_module.run_summarization(json_file, target_dir, template)
            count_success += 1

        except Exception as e:
            log.error(f"Summarization failed for {json_file.name}: {e}", exc_info=True)
            count_fail += 1

    log.info("--- Summarization Finished ---")
    log.info(f"[green]Success: {count_success}[/green]")
    log.warning(f"[yellow]Skipped: {count_skip}[/yellow]")
    log.error(f"[red]Failed:  {count_fail}[/red]")


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
    )] = Path("."),
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

    # TODO: Assumes run_export can handle a directory.
    # If not, add _find_json_files and loop like in summarize.

    try:
        log.info("Export started.")
        export_module.run_export(input_path, output_dir, format)
    except Exception as e:
        log.error(f"Export failed for {input_path} (format: {format}): {e}", exc_info=True)
        raise typer.Exit(code=1)

    log.info("Export finished.")


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
    )] = Path("."),
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

    # TODO: Assumes run_visualization can handle a directory.
    # If not, add _find_json_files and loop like in summarize.

    try:
        log.info("Visualization data generation started.")
        visualize_module.run_visualization(input_path, output_dir, embed)
    except Exception as e:
        log.error(f"Visualization data generation failed for {input_path}: {e}", exc_info=True)
        raise typer.Exit(code=1)

    log.info("Visualization data generation finished.")


@app.command()
def all(
    input_path: Annotated[Path, typer.Argument(
        help="Path to a calculation file or directory to process.",
        exists=True,
        file_okay=True,
        dir_okay=True,
        resolve_path=True,
    )] = Path.cwd(), # Default to current working directory
    output_dir: Annotated[Path, typer.Option(
        "--output", "-o",
        help="Directory to save all generated outputs.",
        resolve_path=True,
    )] = Path("./"), 
    recursive: Annotated[bool, typer.Option(
        "--recursive", "-r",
        help="Search recursively for input calculation files."
    )] = False,
    force: Annotated[bool, typer.Option(
        "--force", "-f",
        help="Force re-generation of outputs (passed to parse and summarize).",
    )] = False, 
    yes: Annotated[bool, typer.Option(
        "--yes", "-y",
        help="Assume yes for all interactive prompts (non-interactive/batch mode)."
    )] = False,
    config: Annotated[Path, typer.Option(
        "--config", "-c",
        help="Optional analysis configuration file (passed to analyze).",
        exists=True,
        file_okay=True,
        dir_okay=False,
        resolve_path=True,
    )] = None,
    template: Annotated[str, typer.Option(
        "--template", "-t",
        help="Optional summary template (passed to summarize).",
    )] = None,
    export_format: Annotated[str, typer.Option(
        "--format", "-fmt",
        help="Export format for the export step (e.g., csv, yaml, json_summary).",
    )] = "csv",
    embed: Annotated[bool, typer.Option(
        "--embed", "-e",
        help="Generate Markdown embedding snippets during visualization.",
    )] = False,
):
    """
    Run the full FAIR workflow: parse -> analyze -> summarize -> export -> visualize.
    """
    log.info("--- Starting Full FAIR Workflow (all steps) ---")
    log.info(f"Input path: {input_path}")
    log.info(f"Output directory: {output_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)

    # --- Step 1: Parse ---
    log.info("--- STEP 1/5: Parse ---")
    
    # This logic is duplicated from the 'parse' command to ensure
    # the 'all' command correctly finds and processes files.
    files_to_process = _find_calc_files(input_path, recursive=recursive, assume_yes=yes)
    if not files_to_process:
        log.warning("No files found to parse. Aborting workflow.")
        return

    parse_success = 0
    parse_fail = 0
    for file in files_to_process:
        try:
            # The 'all' command *requires* an output_dir, so we use it.
            log.info(f"Parsing file: {file}")
            parse_module.run_parser(file, output_dir, force)
            parse_success += 1
        except Exception as e:
            log.error(f"Failed to parse {file}: {e}", exc_info=False)
            parse_fail += 1
    
    if parse_success == 0:
        log.error("No files were successfully parsed. Aborting workflow.")
        raise typer.Exit(code=1)
    log.info(f"Parsing complete. Success: {parse_success}, Failed: {parse_fail}")


    # Subsequent steps operate on the output_dir
    # We pass 'output_dir' as the 'input_path' for all subsequent steps.
    
    # --- Step 2: Analyze ---
    try:
        log.info("--- STEP 2/5: Analyze ---")
        analyze_module.run_analysis(output_dir, output_dir, config)
    except Exception as e:
        log.error(f"Analysis step failed: {e}", exc_info=True)
        raise typer.Exit(code=1)

    # --- Step 3: Summarize ---
    try:
        log.info("--- STEP 3/5: Summarize ---")
        # We must call the 'summarize' *command's logic* here, not the module directly,
        # to ensure it loops over files correctly.
        # We find JSON files in the output_dir
        json_files = _find_json_files(output_dir, recursive=True)
        if not json_files:
            log.warning("No parsed JSON files found in output directory to summarize.")
        else:
            for json_file in json_files:
                try:
                    summary_base_name = json_file.stem.replace("fair_parsed_", "fair_summarized_")
                    md_output_path = output_dir / f"{summary_base_name}.md"
                    
                    if not force and md_output_path.exists():
                        log.info(f"Skipping summary for {json_file.name}; output exists.")
                        continue
                        
                    summarize_module.run_summarization(json_file, output_dir, template)
                except Exception as e:
                    log.error(f"Summarization failed for {json_file.name}: {e}", exc_info=False)
    except Exception as e:
        log.error(f"Summarization step failed: {e}", exc_info=True)
        raise typer.Exit(code=1)

    # --- Step 4: Export ---
    try:
        log.info("--- STEP 4/5: Export ---")
        export_module.run_export(output_dir, output_dir, export_format)
    except Exception as e:
        log.error(f"Export step failed: {e}", exc_info=True)
        raise typer.Exit(code=1)

    # --- Step 5: Visualize ---
    try:
        log.info("--- STEP 5/5: Visualize ---")
        visualize_module.run_visualization(output_dir, output_dir, embed)
    except Exception as e:
        log.error(f"Visualization step failed: {e}", exc_info=True)
        raise typer.Exit(code=1)

    log.info("--- Full FAIR Workflow Completed Successfully ---")


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
    app()