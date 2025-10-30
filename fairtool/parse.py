# fairtool/parse.py

"""Handles the parsing of calculation files."""

import json
import logging
import pint
from pathlib import Path
import subprocess
import time
import numpy as np
from typing import Optional  
from pymatgen.core import Structure, Lattice 
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer

import os
# from electronic_parsers import auto
ELEMENTARY_CHARGE_VALUE = 1.602176634e-19  # Elementary charge in Coulombs, used for energy conversion if needed


log = logging.getLogger(__name__)
u = pint.UnitRegistry()

def _create_structure_json(full_data: dict, output_dir: Path, base_name: str):
    """
    Save only the conventional cell to fair-structure.json in a format compatible
    with the existing viewer: lattice.matrix = 3 Cartesian vectors (Å),
    sites[].xyz = Cartesian coordinates (Å). Also include frac_coords for reference.
    """
    structure = None

    # 1) Try to get conventional structure from NOMAD topology
    try:
        topology = full_data.get("results", {}).get("material", {}).get("topology", [])
        for entry in topology:
            if entry.get("label") == "conventional cell" and "atoms" in entry:
                structure = _nomad_atoms_to_pymatgen(entry["atoms"])
                if structure:
                    log.info(f"Using conventional cell from NOMAD for {base_name}.")
                break
    except Exception as e:
        log.warning(f"Could not extract conventional structure directly from NOMAD: {e}")

    # 2) Fallback: derive conventional structure from primitive
    if structure is None:
        try:
            primitive_atoms = full_data["run"][0]["system"][0]["atoms"]
            primitive_structure = _nomad_atoms_to_pymatgen(primitive_atoms)
            if primitive_structure:
                analyzer = SpacegroupAnalyzer(primitive_structure, symprec=1e-3)
                structure = analyzer.get_conventional_standard_structure()
                log.info(f"Generated conventional structure for {base_name}.")
        except Exception as e:
            log.warning(f"Failed to derive conventional structure: {e}")

    if structure is None:
        log.info(f"No structure found for {base_name}; skipping fair-structure.json.")
        return

    # 3) Prepare JSON-friendly output: lattice as 3 vectors, sites with xyz (Cartesian)
    lattice_matrix = np.array(structure.lattice.matrix).tolist()  # [[ax,ay,az],[bx,by,bz],[cx,cy,cz]]

    sites_out = []
    for site in structure.sites:
        # site.coords is Cartesian coords in Å
        cart_xyz = np.array(site.coords).tolist()
        frac = np.array(site.frac_coords).tolist()
        sites_out.append({
            "element": str(site.specie),
            "xyz": cart_xyz,
            "frac_coords": frac
        })

    data = {
        "lattice": {"matrix": lattice_matrix},
        "sites": sites_out,
        "formula": structure.composition.reduced_formula
    }

    # 4) Save file
    output_path = output_dir / "fair-structure.json"
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        log.info(f"Saved conventional structure JSON: {output_path.name}")
    except Exception as e:
        log.error(f"Failed to save {output_path.name}: {e}", exc_info=True)
        raise


def _nomad_atoms_to_pymatgen(atoms_block: dict) -> Optional[Structure]:
    """
    Converts a NOMAD 'atoms' block (using meters) into a pymatgen Structure (using Angstroms).
    
    Args:
        atoms_block: A dictionary corresponding to the 'atoms' block from the NOMAD archive.
    
    Returns:
        A pymatgen.core.Structure object, or None if conversion fails.
    """
    try:
        # Extract data
        # NOMAD provides vectors and positions in meters.
        # Pymatgen expects Angstroms. 1 m = 1e10 A.
        lattice_matrix_m = atoms_block["lattice_vectors"]
        cart_coords_m = atoms_block["positions"]
        species = atoms_block["labels"]

        # Convert from meters to Angstroms
        lattice_matrix_A = [[v * 1e10 for v in vec] for vec in lattice_matrix_m]
        cart_coords_A = [[v * 1e10 for v in vec] for vec in cart_coords_m]

        # Create pymatgen Structure object
        structure = Structure(
            lattice=lattice_matrix_A,
            species=species,
            coords=cart_coords_A,
            coords_are_cartesian=True
        )
        return structure
    except Exception as e:
        log.error(f"Failed to create pymatgen structure from atoms block: {e}", exc_info=True)
        return None


def run_parser(input_file: Path, output_dir: Path, force: bool) -> bool:
    """
    Parses a single calculation file using electronic-parsers.

    Args:
        input_file: Path to the calculation output file.
        output_dir: Directory to save the parsed JSON and Markdown.
        force: Whether to overwrite existing output files.
        
    Returns:
        bool: True if parsing was skipped, False otherwise.
    """
    # Define output file paths
    base_name = input_file.stem
    json_output_path = output_dir / f"fair_parsed_{base_name}.json"
    
    # Unused variable removed
    # md_output_path = output_dir / f"fair_summarized_{base_name}.md"

    log.info(f"Preparing to parse {input_file.name} -> {json_output_path.name}")

    # If not forcing, check existing parsed JSON metadata to decide whether to skip
    if not force and json_output_path.exists():
        try:
            with open(json_output_path, 'r', encoding='utf-8') as jf:
                existing = json.load(jf)
            fair_time = None
            if isinstance(existing, dict):
                md = existing.get('metadata')
                if isinstance(md, dict):
                    fair_time = md.get('fair_parse_time')
            try:
                file_mtime = input_file.stat().st_mtime
            except Exception:
                file_mtime = None

            if fair_time is not None and file_mtime is not None:
                try:
                    if float(fair_time) >= float(file_mtime):
                        log.info(f"Skipping parse for {input_file.name} — unchanged since last parse.")
                        return True # Return True to indicate skipped
                except Exception:
                    log.debug(f"Could not compare times; will re-parse.")
        except Exception:
            log.debug(f"Could not read existing parsed JSON {json_output_path}; will re-parse.")

    log.info(f"Attempting to parse {input_file.name} ...")

    # The command to run, broken into a list for subprocess
    command = [
        "nomad", "parse",
        "--show-archive",
        "--show-metadata",
        str(input_file)
    ]

    try:
        # Run the NOMAD parser command
        process = subprocess.run(
            command,
            capture_output=True,
            text=True,  # To get stdout/stderr as strings
            check=True, # To raise CalledProcessError on non-zero exit codes
            encoding='utf-8'
        )

        raw_json_output = process.stdout
        if not raw_json_output:
            log.warning(f"Parser returned no data for {input_file.name}.")
            return False

        # Parse the full JSON output into a Python dictionary
        decoder = json.JSONDecoder()
        pos = 0
        full_data = {}
        raw_json_output = raw_json_output.strip()
        while pos < len(raw_json_output):
            obj, pos = decoder.raw_decode(raw_json_output, pos)
            full_data.update(obj)

        # --- Filter for necessary fields (using safe .pop()) ---
        if "run" in full_data and isinstance(full_data["run"], list):
            for run_item in full_data["run"]:
                if "method" in run_item and isinstance(run_item["method"], list):
                    for method_item in run_item["method"]:
                        if "k_mesh" in method_item and isinstance(method_item["k_mesh"], dict):
                            if "points" in method_item["k_mesh"] and isinstance(method_item["k_mesh"]["points"], dict):
                                method_item["k_mesh"]["points"].pop("im", None) # Safe pop
                
                if "calculation" in run_item and isinstance(run_item["calculation"], list):
                    for calc_item in run_item["calculation"]:
                        calc_item.pop("dos_electronic", None) # Safe pop
                        calc_item.pop("eigenvalues", None) # Safe pop

        # Safe-pop top-level keys
        full_data.pop("entry_name", None)
        full_data.pop("entry_type", None)
        full_data.pop("mainfile", None)
        full_data.pop("domain", None)
        full_data.pop("n_quantities", None)
        full_data.pop("quantities", None)
        full_data.pop("optimade", None)
        full_data.pop("sections", None)
        full_data.pop("section_defs", None)
        full_data.pop("workflow2", None)

        if "metadata" in full_data and isinstance(full_data["metadata"], dict):
            full_data["metadata"].pop("n_quantities", None)
            full_data["metadata"].pop("quantities", None)
            full_data["metadata"].pop("sections", None)
            full_data["metadata"].pop("section_defs", None)

        log.info(f"Saving filtered parsed data to {json_output_path}")
        try:
            # Add fair_parse_time *after* filtering
            if "metadata" not in full_data or not isinstance(full_data.get('metadata'), dict):
                full_data["metadata"] = {}
            full_data["metadata"]["fair_parse_time"] = time.time()
            
            with open(json_output_path, 'w', encoding='utf-8') as f:
                json.dump(full_data, f, indent=2,ensure_ascii=False)
            log.info(f"Successfully saved JSON: {json_output_path.name}")

            # Also create structure JSON
            _create_structure_json(full_data, output_dir, base_name)

        except Exception as json_err:
            log.error(f"Failed to save JSON for {input_file.name}: {json_err}")
            if json_output_path.exists():
                json_output_path.unlink()
            raise

    except FileNotFoundError:
        log.error("`nomad` command not found. Is NOMAD installed and in your system's PATH?")
        raise
    except subprocess.CalledProcessError as e:
            log.error(f"NOMAD parsing command failed for {input_file.name} with exit code {e.returncode}: {e.stderr}", exc_info=False)
            raise
    except json.JSONDecodeError as e:
        log.error(f"Failed to decode JSON output from NOMAD parser for {input_file.name}: {e}")
        log.error(f"Problematic output snippet: {raw_json_output[e.pos:e.pos+200]}...")
        raise
    except Exception as e:
        log.error(f"An unexpected error occurred during parsing of {input_file.name}: {e}", exc_info=True)
        raise

    return False # Return False to indicate parsing was attempted