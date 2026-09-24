# fairtool/analyze.py

"""Handles the analysis of parsed calculation data."""

import json
import logging
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd  # Example: for creating summary tables
import yaml  # For config file

from .parse import ELEMENTARY_CHARGE_VALUE, PARSED_JSON_GLOB

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
    Extracts the key results of the final calculation in a parsed archive.

    `fair parse` keeps NOMAD's legacy `run` section, which holds these values in SI units
    and is also what summarize.py reads. For VASP runs, the `results.properties` section of
    NOMAD 1.4 has no total energy, band gap or convergence flag, so it is not used.

    Args:
        data: The loaded JSON data from the parser.
        config: The analysis configuration dictionary.
        identifier: A unique identifier for this calculation (e.g., filename stem).

    Returns:
        A dictionary with the identifier, `total_energy_eV`, `band_gap_eV` and `converged`.
        A value is None when the archive lacks the data it is derived from.
    """
    log.debug(f"Performing analysis for identifier: {identifier}")

    # The last calculation is the final one, e.g. the last ionic step of a relaxation
    run = _get(data, "run", 0)
    calculation = _get(run, "calculation", -1)

    results = {
        "identifier": identifier,
        "total_energy_eV": _joule_to_ev(_get(calculation, "energy", "total", "value")),
        "band_gap_eV": _band_gap_ev(calculation),
        "converged": _scf_converged(calculation, _get(run, "method", -1, "scf", "threshold_energy_change")),
    }

    # Add more analysis based on `config` if needed
    # if config.get("calculate_dos_features"):
    #     dos_features = calculate_dos(...)
    #     results.update(dos_features)

    log.info(
        f"Analysis summary for {identifier}: Energy={results.get('total_energy_eV')}, Gap={results.get('band_gap_eV')}, Converged={results.get('converged')}"
    )
    return results


def _get(node, *path):
    """Follows dict keys and list indices into parsed JSON; returns None if a step is missing."""
    for step in path:
        try:
            node = node[step]
        except (KeyError, IndexError, TypeError):
            return None
    return node


def _joule_to_ev(value) -> Optional[float]:
    """Converts a NOMAD energy (joules) to eV; returns None if it is missing or not a number."""
    try:
        return float(value) / ELEMENTARY_CHARGE_VALUE
    except (TypeError, ValueError):
        return None


def _band_gap_ev(calculation) -> Optional[float]:
    """
    Derives the band gap (eV) of a calculation from its eigenvalues.

    NOMAD 1.4 stores no band gap value for these runs, only the eigenvalues: `eigenvalues`,
    or `band_structure_electronic[].segment` for a band-structure run. As in NOMAD's VASP
    parser, a state is occupied when its occupation is at least 0.5. A band crossing the
    Fermi level makes the number of occupied states differ between k-points; that is a
    metal, with a gap of 0. Otherwise the gap is the lowest unoccupied minus the highest
    occupied energy over all k-points and spin channels.
    """
    try:
        blocks = _get(calculation, "eigenvalues") or [
            segment
            for band_structure in _get(calculation, "band_structure_electronic") or []
            for segment in _get(band_structure, "segment") or []
        ]
        # Each block is shaped (spin channel, k-point, band); join them along the k-points
        energies = np.concatenate([np.asarray(block["energies"], dtype=float) for block in blocks], axis=1)
        occupations = np.concatenate([np.asarray(block["occupations"], dtype=float) for block in blocks], axis=1)
    except (KeyError, TypeError, ValueError):
        return None
    if energies.ndim != 3 or energies.shape != occupations.shape:
        return None

    occupied = occupations >= 0.5
    if occupied.all() or not occupied.any():
        return None
    n_occupied = occupied.sum(axis=2)  # per spin channel and k-point
    if (n_occupied != n_occupied[:, :1]).any():
        return 0.0
    gap = energies[~occupied].min() - energies[occupied].max()
    return max(float(gap), 0.0) / ELEMENTARY_CHARGE_VALUE


def _scf_converged(calculation, threshold) -> Optional[bool]:
    """
    Tells whether the SCF cycle of a calculation met its energy threshold.

    For a single-point run NOMAD records this as `workflow2.results.is_converged`, which
    `fair parse` drops, so it is recomputed here with NOMAD's rule: the last non-zero change
    between consecutive SCF iterations must not exceed the method's
    `scf.threshold_energy_change`. The change is taken in the free energy, the quantity VASP
    compares with EDIFF. NOMAD uses `energy.total` (for VASP, the energy without entropy),
    which can only give a different answer when the smearing entropy changes between the
    last iterations.
    """
    try:
        threshold = float(threshold)
        energies = [
            _get(iteration, "energy", "free", "value") for iteration in _get(calculation, "scf_iteration") or []
        ]
        changes = np.abs(np.diff([float(energy) for energy in energies if energy is not None]))
    except (TypeError, ValueError):
        return None
    if changes.size == 0:
        return None
    nonzero = changes[changes != 0]
    last_change = nonzero[-1] if nonzero.size else 0.0
    return bool(last_change <= threshold)
