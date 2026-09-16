# fairtool/export.py

"""Handles exporting processed data into various formats."""

import json
import logging
from pathlib import Path

import pandas as pd  # For CSV export
import yaml  # For YAML export

log = logging.getLogger("fairtool")


def run_export(input_path: Path, output_dir: Path, export_format: str):
    """
    Exports parsed or analyzed data into the specified format.

    Args:
        input_path: Path to the data source (e.g., analysis_summary.csv, directory of JSON/YAML).
        output_dir: Directory to save the exported files.
        export_format: The desired output format (e.g., 'csv', 'yaml', 'json_summary').
    """
    # --- Determine Input Data ---
    # This logic assumes common scenarios, adjust as needed.
    data_to_export = None
    source_desc = ""

    analysis_summary_csv = input_path / "analysis_summary.csv" if input_path.is_dir() else None
    if analysis_summary_csv and analysis_summary_csv.is_file():
        log.info(f"Using analysis summary CSV as data source: {analysis_summary_csv}")
        try:
            data_to_export = pd.read_csv(analysis_summary_csv)
            source_desc = analysis_summary_csv.name
        except Exception as e:
            log.error(f"Failed to load {analysis_summary_csv}: {e}. Cannot export from this source.")
            return  # Or try other sources
    elif input_path.is_file() and input_path.suffix == ".csv":
        log.info(f"Using provided CSV as data source: {input_path}")
        try:
            data_to_export = pd.read_csv(input_path)
            source_desc = input_path.name
        except Exception as e:
            log.error(f"Failed to load {input_path}: {e}. Cannot export from this source.")
            return
    elif input_path.is_dir():
        # TODO: Implement logic to load data from multiple JSON or YAML files in the directory
        # Example: Load all *_analysis.yaml files into a list of dicts
        log.warning(
            "Directory input for export currently only checks for 'analysis_summary.csv'. Implement loading of other file types (JSON/YAML) if needed."
        )
        # yaml_files = sorted(list(input_path.rglob("*_analysis.yaml")))
        # if yaml_files: ... load and combine ...
        # data_to_export = list_of_loaded_dicts
        # source_desc = f"data from {input_path}"
        pass  # Placeholder

    if data_to_export is None:
        log.error(f"Could not find or load suitable data to export from: {input_path}")
        return

    log.info(f"Preparing to export data from '{source_desc}' to format '{export_format}'...")

    # --- Perform Export based on Format ---
    try:
        if export_format.lower() == "csv":
            if isinstance(data_to_export, pd.DataFrame):
                output_file = output_dir / "exported_data.csv"
                data_to_export.to_csv(output_file, index=False)
                log.info(f"Data exported successfully to: {output_file}")
            else:
                log.error("CSV export requires data loaded as a Pandas DataFrame (e.g., from analysis_summary.csv).")
                return

        elif export_format.lower() == "yaml":
            output_file = output_dir / "exported_data.yaml"
            export_payload = None
            if isinstance(data_to_export, pd.DataFrame):
                # Convert DataFrame to list of dictionaries for better YAML structure
                export_payload = data_to_export.to_dict(orient="records")
            elif isinstance(data_to_export, (list, dict)):
                export_payload = data_to_export
            else:
                log.error(f"Cannot convert data of type {type(data_to_export)} directly to YAML.")
                return

            with open(output_file, "w") as f:
                yaml.dump(export_payload, f, default_flow_style=False, sort_keys=False)
            log.info(f"Data exported successfully to: {output_file}")

        elif export_format.lower() == "json_summary":
            # Example: Export a simplified JSON summary
            output_file = output_dir / "exported_summary.json"
            export_payload = None
            if isinstance(data_to_export, pd.DataFrame):
                # Example: Convert DataFrame to dict {identifier: {col: value}}
                if "identifier" in data_to_export.columns:
                    export_payload = data_to_export.set_index("identifier").to_dict(orient="index")
                else:
                    # Fallback: list of records
                    export_payload = data_to_export.to_dict(orient="records")
            elif isinstance(data_to_export, (list, dict)):
                export_payload = data_to_export  # Assume it's already suitable
            else:
                log.error(f"Cannot convert data of type {type(data_to_export)} directly to JSON.")
                return

            with open(output_file, "w") as f:
                json.dump(export_payload, f, indent=2)
            log.info(f"Data exported successfully to: {output_file}")

        # Add more formats as needed (e.g., specific database formats, other text formats)
        # elif export_format.lower() == 'some_other_format':
        #     ...

        else:
            log.error(f"Unsupported export format: '{export_format}'. Supported formats: csv, yaml, json_summary.")
            return

    except Exception as e:
        log.error(f"An error occurred during export (format: {export_format}): {e}", exc_info=True)
        raise  # Re-raise to be caught by CLI

    log.info("Export process completed.")
