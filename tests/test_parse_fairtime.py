import json
import time
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest
from typer.testing import CliRunner

# Import the app for CLI runner tests
# Import parse_cmd (the typer command) and _find_calc_files from cli
# Import run_parser from parse
from fairtool.cli import app, parse as parse_cmd, _find_calc_files
from fairtool.parse import run_parser

runner = CliRunner()


def make_nomad_process(stdout_text: str):
    """Helper to create a mock subprocess.run result."""
    proc = MagicMock()
    proc.stdout = stdout_text
    proc.stderr = ""
    proc.returncode = 0
    return proc


def test_run_parser_writes_fair_parse_time_and_filters(tmp_path, monkeypatch):
    """
    Tests that run_parser (the core function) correctly:
    1. Runs the (mocked) nomad subprocess.
    2. Filters the resulting JSON (removes 'n_quantities', etc.).
    3. Adds the 'fair_parse_time' metadata.
    4. Safely removes keys using .pop().
    """
    # Create a dummy input file
    input_file = tmp_path / "vasprun.xml"
    input_file.write_text("dummy content")

    output_dir = tmp_path / "out"
    output_dir.mkdir()

    # This mock represents the *merged* object after the `while` loop
    fake_nomad_json = json.dumps({
        # --- Keys from the *first* JSON (metadata) ---
        "entry_name": "Test Entry",
        "entry_type": "Test Type",
        "domain": "dft",
        "optimade": {"elements": ["Ag", "Cl", "Cs", "Hg"]},
        "n_quantities": 42,
        "quantities": ["some_quantity"],
        "sections": ["some_section"],
        "section_defs": ["some_def"],

        # --- Keys from the *second* JSON (archive) ---
        "run": [
            {
                "program": {"name": "VASP", "version": "6.3.0"},
                "system": [
                     {"atoms": {
                        "lattice_vectors": [
                            [5.0e-10, 0, 0], [0, 5.0e-10, 0], [0, 0, 5.0e-10]
                        ],
                        "positions": [
                            [0, 0, 0]
                        ],
                        "labels": ["X"]
                    }}
                ],
                "calculation": [
                    {"energy": {"total": {"value": -4.8e-18}}}
                ]
            }
        ],
        "metadata": {
            "entry_name": "Test Entry", # This gets overwritten
            "entry_type": "Test Type",
        },
        "results": {
             "material": {"topology": []} # Added for structure gen
        }
    })

    fake_proc = make_nomad_process(fake_nomad_json)
    monkeypatch.setattr("subprocess.run", lambda *a, **k: fake_proc)

    # --- [FIX] Capture current time BEFORE running ---
    start_time = time.time()

    # Call run_parser directly, force=True to bypass skip logic
    skipped = run_parser(input_file, output_dir, force=True)

    # It should not have skipped
    assert not skipped

    json_file = output_dir / f"fair_parsed_{input_file.stem}.json"
    assert json_file.exists()

    data = json.loads(json_file.read_text(encoding='utf-8'))
    assert "metadata" in data
    assert "fair_parse_time" in data["metadata"]
    # Check that a key from the archive metadata is still there
    assert "entry_type" in data["metadata"]
    # Check that top-level keys were removed
    assert "n_quantities" not in data
    assert "optimade" not in data
    # Check that keys were safely .pop()ed from the *archive* metadata
    assert "n_quantities" not in data["metadata"]

    # --- [FIX] Test that parse time is close to the *current time* ---
    # not the file's mtime
    assert abs(data["metadata"]["fair_parse_time"] - start_time) < 2.0


# --- [FIXED TEST] Logic is now in run_parser ---
@patch("subprocess.run") # We don't want subprocess to run at all
def test_run_parser_skips_when_unchanged(mock_subprocess_run, tmp_path):
    """
    Tests that run_parser (the core function) *itself*
    correctly skips parsing when force=False and mtime is older.
    """
    # Create a dummy input file
    input_file = tmp_path / "vasprun2.xml"
    input_file.write_text("content")
    file_mtime = input_file.stat().st_mtime
    
    output_dir = tmp_path / "out2"
    output_dir.mkdir()

    # Create an existing parsed JSON with fair_parse_time >= file mtime
    json_file = output_dir / f"fair_parsed_{input_file.stem}.json"
    # Save a parse time that is *newer* than the file
    json_content = {"metadata": {"fair_parse_time": file_mtime + 10}}
    json_file.write_text(json.dumps(json_content), encoding='utf-8')

    # Call run_parser directly, with force=False
    skipped = run_parser(input_file, output_dir, force=False)

    # --- [FIX] Assert that run_parser *returned True* (indicating a skip) ---
    assert skipped
    
    # And double-check it didn't try to run nomad
    mock_subprocess_run.assert_not_called()


# --- [FIXED TEST] Logic is in run_parser, and CLI args changed ---
@patch('fairtool.cli.parse_module.run_parser') # [FIX] Patch the *correct path*
def test_cli_calls_parser_when_missing_fair_parse_time(mock_run_parser, tmp_path):
    """
    Tests that the `parse` command (parse_cmd) correctly
    finds the file and calls `run_parser`. The skip logic
    is no longer in the CLI, so this should *always* call the mock.
    """
    # Create a dummy input file
    input_file = tmp_path / "vasprun3.xml"
    input_file.write_text("content")

    output_dir = tmp_path / "out3"
    output_dir.mkdir()

    # Create an existing parsed JSON *without* fair_parse_time
    json_file = output_dir / f"fair_parsed_{input_file.stem}.json"
    json_content = {"metadata": {"some": "value"}}
    json_file.write_text(json.dumps(json_content), encoding='utf-8')

    # --- [FIX] Call parse_cmd with the new 'recursive' argument ---
    # The signature is: parse(input_path, recursive, output_dir, force, yes)
    parse_cmd(
        input_path=input_file,
        recursive=False, # Explicitly pass the new arg
        output_dir=output_dir,
        force=False, # This is the default
        yes=False    # This is the default
    )
    
    # The CLI's job is just to find files and call the parser.
    # The skip logic is inside run_parser, so the CLI *will* call it.
    # The `force` arg (False) is passed from the CLI to run_parser.
    mock_run_parser.assert_called_once_with(input_file, output_dir, False)

