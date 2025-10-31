"""Main CLI entry point for the FAIR tool."""
import typer
from typing_extensions import Annotated
from pathlib import Path
from typing import Optional
import logging
import rich
import subprocess
from rich.logging import RichHandler
import tempfile

import shutil  # Import shutil for copying
import yaml  # <-- Re-import yaml
import os  # <-- Import OS for environment variables
from importlib.resources import files  # <-- Use this for package data
import importlib # <-- Import for checking dependencies
import sys # <-- Import sys to get executable path


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
    suggest_commands=True,
    rich_markup_mode="rich"
)

# --- YAML LOADER FIX ---
# We need these again so yaml.UnsafeLoader can find the modules
try:
    import material.extensions.emoji
    import pymdownx.superfences
    import pymdownx.slugs
    import pymdownx.tabbed
except ImportError as e:
    log.warning(f"Could not pre-import mkdocs plugin modules: {e}")
    log.warning("This might be okay if 'mkdocs-material' is not installed,")
    log.warning("but loading the config might fail if it uses these modules.")
# --- END YAML LOADER FIX ---


# --- Typer Command Definitions ---
@app.command(rich_help_panel="Information and Help", epilog="Made with :heart: in [blue]The Netherlands[/blue]")
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
            list(search_method("*vasprun.xml"))
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



@app.command(rich_help_panel="Processing")
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
    log.info(f"[yellow]Skipped: {count_skip}[/yellow]")
    log.info(f"[red]Failed:  {count_fail}[/red]")


@app.command(rich_help_panel="Processing")
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
    Perform analysis on parsed calculation data. Get derived properties.
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


@app.command(rich_help_panel="Processing")
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
    log.info(f"[yellow]Skipped: {count_skip}[/yellow]")
    log.info(f"[red]Failed:  {count_fail}[/red]")


@app.command(rich_help_panel="Processing")
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


# @app.command(rich_help_panel="Processing")
# def visualize(
#     input_path: Annotated[Path, typer.Argument(
#         help="Path to parsed data (JSON/directory) containing structures, BZ, etc.",
#          exists=True,
#         file_okay=True,
#         dir_okay=True,
#         resolve_path=True,
#     )],
#     output_dir: Annotated[Path, typer.Option(
#         "--output", "-o",
#         help="Directory to save visualization data (e.g., JSON for React components) and potentially Markdown snippets.",
#         resolve_path=True,
#     )] = Path("."),
#     embed: Annotated[bool, typer.Option(
#         "--embed", "-e",
#         help="Generate Markdown snippets for embedding visualizations in mkdocs.",
#     )] = False,
# ):
#     """
#     Generate a complete visualization of the processed data (metadata, structures, BZ, DOS, bands)
#     """

#     log.info(f"Starting visualization data generation for: {input_path}")
#     output_dir.mkdir(parents=True, exist_ok=True)
#     log.info(f"Visualization data will be saved to: {output_dir}")
#     if embed:
#         log.info("Will generate Markdown embedding snippets.")

#     # TODO: Assumes run_visualization can handle a directory.
#     # If not, add _find_json_files and loop like in summarize.

#     try:
#         log.info("Visualization data generation started.")
#         visualize_module.run_visualization(input_path, output_dir, embed)
#     except Exception as e:
#         log.error(f"Visualization data generation failed for {input_path}: {e}", exc_info=True)
#         raise typer.Exit(code=1)

#     log.info("Visualization data generation finished.")

@app.command(rich_help_panel="Processing")
def visualize(
    input_path: Annotated[Path, typer.Argument(
        help="Path containing FAIR-generated Markdown summaries.",
        exists=True,
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
    )],
    port: Annotated[int, typer.Option(
        "--port", "-p",
        help="Port for FAIR live server (default: 8000).",
    )] = 8000,
):
    """
    Serve FAIR-generated Markdown files as a browsable website with search enabled.
    """
    
    # --- Dependency Check REMOVED ---
    # We will rely on 'mkdocs' to report if plugins are missing.

    log.info(f"Serving FAIR data from: {input_path}")

    try:
        # 1. Find the source 'documentation' package
        pkg_root = files("documentation")
    except Exception as e:
        log.error(f"Failed to find 'documentation' package data. Is it installed correctly (e.g., 'pip install -e .')? {e}", exc_info=True)
        raise typer.Exit(code=1)

    # 2. Use TemporaryDirectory for automatic creation and cleanup
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_project_path = Path(temp_dir)
            
            # 3. Create a namespaced directory for our custom python files
            scripts_dir = temp_project_path / "_scripts"
            scripts_dir.mkdir()
            (scripts_dir / "__init__.py").touch() # Make it a package

            original_hook_path_str = "material/overrides/hooks/shortcodes.py"
            # This path is now relative to temp_project_path, which will be in PYTHONPATH
            new_hook_name_relative = "_scripts/hooks_shortcodes.py" 
            
            try:
                # --- Files to copy ---
                # Copy mkdocs.yml to root
                shutil.copy(pkg_root / "mkdocs.yml", temp_project_path / "mkdocs.yml")
                
                # Copy macros.py into _scripts
                if (pkg_root / "macros.py").exists():
                    shutil.copy(pkg_root / "macros.py", scripts_dir / "macros.py")
                
                # Copy hook file into _scripts
                original_hook_path = pkg_root / original_hook_path_str
                if original_hook_path.exists():
                    shutil.copy(original_hook_path, scripts_dir / "hooks_shortcodes.py")

                log.debug(f"Copied project files to {temp_project_path} and namespaced scripts to {scripts_dir}")

            except Exception as e:
                log.error(f"Failed to copy/namespace files to temp dir: {e}", exc_info=True)
                raise typer.Exit(code=1)

            # 4. Load, Modify, and Overwrite the temporary mkdocs.yml
            temp_config_path = temp_project_path / "mkdocs.yml"
            try:
                # Load the config
                with temp_config_path.open("r", encoding="utf-8") as f:
                    mkdocs_data = yaml.load(f, Loader=yaml.UnsafeLoader)
                
                # --- Modify paths ---
                
                # 5a. Set user's docs_dir (absolute)
                mkdocs_data["docs_dir"] = str(input_path.resolve())

                # 5b. Fix theme.custom_dir (absolute)
                if "theme" in mkdocs_data and "custom_dir" in mkdocs_data["theme"]:
                    original_custom_dir = mkdocs_data["theme"]["custom_dir"]
                    mkdocs_data["theme"]["custom_dir"] = str((pkg_root / original_custom_dir).resolve())

                # 5c. Fix 'extra_css' (absolute)
                if "extra_css" in mkdocs_data:
                    new_extra_css = []
                    for css in mkdocs_data["extra_css"]:
                        if not (css.startswith("http") or css.startswith("/")):
                            new_extra_css.append(str((pkg_root / "docs" / css).resolve()))
                        else:
                            new_extra_css.append(css)
                    mkdocs_data["extra_css"] = new_extra_css

                # 5d. Fix 'extra_javascript' (absolute)
                if "extra_javascript" in mkdocs_data:
                    new_extra_js = []
                    for js in mkdocs_data["extra_javascript"]:
                        if not (js.startswith("http") or js.startswith("/")):
                            new_extra_js.append(str((pkg_root / "docs" / js).resolve()))
                        else:
                            new_extra_js.append(js)
                    mkdocs_data["extra_javascript"] = new_extra_js

                # 5e. Fix logo/favicon (absolute)
                if "theme" in mkdocs_data and "icon" in mkdocs_data["theme"]:
                    if "logo" in mkdocs_data["theme"]["icon"]:
                        logo_path = mkdocs_data["theme"]["icon"]["logo"]
                        mkdocs_data["theme"]["icon"]["logo"] = str((pkg_root / "docs" / logo_path).resolve())
                if "theme" in mkdocs_data and "favicon" in mkdocs_data["theme"]:
                    favicon_path = mkdocs_data["theme"]["favicon"]
                    mkdocs_data["theme"]["favicon"] = str((pkg_root / "docs" / favicon_path).resolve())
                if "theme" in mkdocs_data and "logo" in mkdocs_data["theme"]:
                    logo_path = mkdocs_data["theme"]["logo"]
                    mkdocs_data["theme"]["logo"] = str((pkg_root / "docs" / logo_path).resolve())
                
                # 5f. Fix 'hooks' path (relative to new PYTHONPATH)
                if "hooks" in mkdocs_data:
                    new_hooks = []
                    for hook in mkdocs_data["hooks"]:
                        if hook == original_hook_path_str:
                            new_hooks.append(new_hook_name_relative) # Point to _scripts/
                        else:
                            new_hooks.append(hook)
                    mkdocs_data["hooks"] = new_hooks

                # 5g. Fix 'macros' module_name (to point to package)
                if "plugins" in mkdocs_data:
                    for plugin in mkdocs_data["plugins"]:
                        if isinstance(plugin, dict) and "macros" in plugin:
                            if plugin["macros"].get("module_name") == "macros":
                                plugin["macros"]["module_name"] = "_scripts.macros"
                                log.debug("Remapped macros module_name to _scripts.macros")
                                break

                # 6. Overwrite the config *in the temp dir*
                with temp_config_path.open("w", encoding="utf-8") as f:
                    yaml.dump(mkdocs_data, f)
                
                log.debug(f"Modified temp config at {temp_config_path} with absolute paths and namespaced scripts")

            except Exception as e:
                log.error(f"Failed to read/modify/write temp mkdocs.yml: {e}", exc_info=True)
                raise typer.Exit(code=1)

            # 7. Define the command to run
            command = [
                sys.executable, "-m", "mkdocs", "serve",
                "--config-file", str(temp_config_path.resolve()), # <-- Use absolute path to config
                "--dev-addr", f"127.0.0.1:{port}"
            ]
            
            # 8. Set up the environment for the subprocess
            # This is the crucial part. We *prepend* our temp dir to
            # PYTHONPATH, ensuring the rest of the venv's paths are kept.
            env = os.environ.copy()
            python_path = env.get("PYTHONPATH", "")
            if python_path:
                env["PYTHONPATH"] = f"{temp_project_path}{os.pathsep}{python_path}"
            else:
                env["PYTHONPATH"] = str(temp_project_path)
            
            log.info(f"Serving website on http://127.0.0.1:{port} ...")
            log.info(f"Using config from: {temp_config_path}")
            log.info(f"Serving Markdown from: {input_path.resolve()}")
            log.debug(f"Running command: {' '.join(command)}")
            log.debug(f"Setting PYTHONPATH for subprocess to: {env['PYTHONPATH']}")


            # 9. Launch MkDocs
            try:
                subprocess.run(
                    command,
                    check=True,
                    # cwd=temp_project_path, # <-- DO NOT SET CWD
                    env=env, # <-- Pass in modified environment
                )
            except KeyboardInterrupt:
                log.info("Server stopped by user.")
            except subprocess.CalledProcessError as e:
                log.error(f"MkDocs serve failed: {e}")
                if e.returncode == 1:
                    log.error("This often means a plugin is missing or the config is invalid.")
            except FileNotFoundError:
                log.error(f"Error: '{sys.executable}' not found or 'mkdocs' module missing.")
                log.error("Please ensure MkDocs is installed in your environment: pip install mkdocs-material")
                raise typer.Exit(code=1)

    except Exception as e:
        log.error(f"Failed to create/use temporary project directory: {e}", exc_info=True)
        raise typer.Exit(code=1)

    # 10. Cleanup is automatic when 'with' block exits
    log.info("Server shut down and temporary files cleaned up.")

@app.command(rich_help_panel="Automated Workflow")
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