# fairtool/analyze.py

"""Handles the analysis of parsed calculation data."""

import json
import logging
from pathlib import Path
from typing import Optional

import pandas as pd  # Example: for creating summary tables
import yaml  # For config file

from .parse import PARSED_JSON_GLOB

# Optional: Import pymatgen or other analysis libraries
# from pymatgen.core import Structure
# from pymatgen.electronic_structure.dos import CompleteDos
# from pymatgen.electronic_structure.bandstructure import BandStructureSymmLine

log = logging.getLogger("fairtool")


def run_analysis(input_path: Path, output_dir: Path, config_path: Optional[Path]):
    """
    Performs analysis on parsed data (JSON file or directory of JSON files).

    Args:
        input_path: Path to a parsed JSON file, or a directory searched recursively for
            the `fair_parsed_*.json` files written by `fair parse`.
        output_dir: Directory to save analysis results.
        config_path: Optional path to a YAML configuration file for analysis tasks.
    """
    config = {}
    if config_path:
        log.info(f"Loading analysis configuration from: {config_path}")
        try:
            with open(config_path, "r") as f:
                config = yaml.safe_load(f)
        except Exception as e:
            log.error(f"Failed to load config file {config_path}: {e}")
            # Decide if analysis can proceed without config or should exit
            # return

    # --- Find input files ---
    if input_path.is_file() and input_path.suffix == ".json":
        files_to_analyze = [input_path]
    elif input_path.is_dir():
        log.info(f"Searching for parsed JSON files ({PARSED_JSON_GLOB}) in: {input_path}")
        files_to_analyze = sorted(list(input_path.rglob(PARSED_JSON_GLOB)))
        if not files_to_analyze:
            log.warning(f"No '{PARSED_JSON_GLOB}' files found in {input_path}")
            return
    else:
        log.error(f"Input path must be a JSON file or a directory containing them: {input_path}")
        return

    log.info(f"Found {len(files_to_analyze)} JSON file(s) to analyze.")

    analysis_results = []  # Store results from each file if creating a summary

    for file in files_to_analyze:
        log.info(f"Analyzing data from: {file.name}")
        try:
            with open(file, "r") as f:
                parsed_data = json.load(f)

            # --- Perform Analysis ---
            # This is where you add your specific analysis logic.
            # Examples:
            # 1. Extract key properties (energy, band gap, forces)
            # 2. Check convergence
            # 3. Calculate derived quantities (e.g., formation energy if multiple calcs)
            # 4. Generate data for plots (DOS, band structure) - often done in visualize step too

            result = perform_single_file_analysis(parsed_data, config, file.stem)
            analysis_results.append(result)

            # --- Save individual results (optional) ---
            # Example: Save a small summary YAML for this specific file
            individual_output_path = output_dir / f"{file.stem}_analysis.yaml"
            log.debug(f"Saving individual analysis summary to {individual_output_path}")
            with open(individual_output_path, "w") as f:
                yaml.dump(result, f, default_flow_style=False)

        except json.JSONDecodeError:
            log.error(f"Failed to decode JSON from {file.name}. Skipping.")
            continue
        except Exception as e:
            log.error(f"Error analyzing {file.name}: {e}", exc_info=True)
            # Decide whether to continue with other files or stop

    # --- Save Aggregate Results (optional) ---
    if analysis_results:
        log.info("Aggregating analysis results...")
        try:
            # Example: Create a Pandas DataFrame and save as CSV
            df = pd.DataFrame(analysis_results)
            aggregate_csv_path = output_dir / "analysis_summary.csv"
            df.to_csv(aggregate_csv_path, index=False)
            log.info(f"Saved aggregate analysis summary to {aggregate_csv_path}")
        except Exception as e:
            log.error(f"Failed to save aggregate analysis results: {e}")

    log.info("Analysis process completed.")


def perform_single_file_analysis(data: dict, config: dict, identifier: str) -> dict:
    """
    Placeholder function for analyzing data from a single parsed file.

    Args:
        data: The loaded JSON data from the parser.
        config: The analysis configuration dictionary.
        identifier: A unique identifier for this calculation (e.g., filename stem).

    Returns:
        A dictionary containing key analysis results.
    """
    log.debug(f"Performing analysis for identifier: {identifier}")
    results = {"identifier": identifier}

    # --- Example Analysis Tasks ---

    # Extract Total Energy (adjust path based on parser output structure)
    try:
        # This path is hypothetical - check electronic-parsers output format
        energy = data.get("results", {}).get("properties", {}).get("energy", {}).get("total", {}).get("value")
        results["total_energy_eV"] = energy
    except (AttributeError, TypeError, KeyError):
        log.debug(f"Could not extract total energy for {identifier}")
        results["total_energy_eV"] = None

    # Extract Band Gap (adjust path based on parser output structure)
    try:
        # Hypothetical path
        band_gap = (
            data.get("results", {})
            .get("properties", {})
            .get("electronic", {})
            .get("band_structure", {})
            .get("band_gap", [{}])[0]
            .get("value")
        )
        results["band_gap_eV"] = band_gap
    except (AttributeError, TypeError, KeyError, IndexError):
        log.debug(f"Could not extract band gap for {identifier}")
        results["band_gap_eV"] = None

    # Check for convergence (adjust path based on parser output structure)
    try:
        # Hypothetical path
        converged = data.get("results", {}).get("workflow", [{}])[0].get("calculation_converged")
        results["converged"] = converged
    except (AttributeError, TypeError, KeyError, IndexError):
        log.debug(f"Could not determine convergence status for {identifier}")
        results["converged"] = None

    # Add more analysis based on `config` if needed
    # if config.get("calculate_dos_features"):
    #     dos_features = calculate_dos(...)
    #     results.update(dos_features)

    log.info(
        f"Analysis summary for {identifier}: Energy={results.get('total_energy_eV')}, Gap={results.get('band_gap_eV')}, Converged={results.get('converged')}"
    )
    return results
