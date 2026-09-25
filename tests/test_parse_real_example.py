import copy
import json
import subprocess
import time
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from fairtool.parse import run_parser


# --- [NEW] Session-scoped fixture to load the reference data once ---
@pytest.fixture(scope="session")
def reference_data():
    """Loads the shared reference JSON data from a file."""
    # Assumes the file is in the same directory as this test file
    ref_path = Path(__file__).parent / "reference_data.json"
    if not ref_path.exists():
        pytest.skip(f"Reference data file not found. Create: {ref_path}")
    with open(ref_path, "r", encoding="utf-8") as f:
        return json.load(f)


def test_parse_vasprun_example_matches_reference(tmp_path, monkeypatch, reference_data):  # <-- [MODIFIED]
    """
    Mock the `nomad parse` subprocess to return the provided reference JSON
    (now treated as the raw nomad output) and compare the final parsed file
    to this same reference, checking only for the addition of
    metadata.fair_parse_time.
    """
    # 1. Create a dummy input file
    input_file = tmp_path / "vasprun.xml"
    input_file.write_text("<scf>dummy vasprun content</scf>")

    # 2. Load the reference data
    # [MODIFIED] This now comes directly from the 'reference_data' fixture
    # The old 'reference_json_file' fixture and the json.loads() call are removed.

    # Create a deep copy to use as the mock output.
    # This mock represents the *final merged* object after the `while` loop in `run_parser`.
    mock_output_data = copy.deepcopy(reference_data)

    # 3. Mock the subprocess.run call to return the merged data structure
    #    that `run_parser` expects *before* it starts deleting keys.

    # Add top-level keys that `run_parser` expects to delete:
    mock_output_data["n_quantities"] = 99
    mock_output_data["quantities"] = ["dummy_q"]
    mock_output_data["sections"] = ["dummy_s"]
    mock_output_data["section_defs"] = ["dummy_sd"]
    mock_output_data["workflow2"] = {"name": "dummy_workflow"}
    # These keys are *also* present in the metadata, so we copy them
    # to the top level to simulate the *first* JSON object from nomad.
    mock_output_data["entry_name"] = reference_data["metadata"]["entry_name"]
    mock_output_data["entry_type"] = reference_data["metadata"]["entry_type"]
    mock_output_data["mainfile"] = reference_data["metadata"]["mainfile"]
    mock_output_data["domain"] = reference_data["metadata"]["domain"]
    mock_output_data["optimade"] = reference_data["metadata"]["optimade"]

    # Add keys to the *archive* metadata block that `run_parser`
    # expects to delete (to prevent KeyError):
    if "metadata" not in mock_output_data:
        mock_output_data["metadata"] = {}
    mock_output_data["metadata"]["n_quantities"] = 99
    mock_output_data["metadata"]["quantities"] = ["dummy_q"]
    mock_output_data["metadata"]["sections"] = ["dummy_s"]
    mock_output_data["metadata"]["section_defs"] = ["dummy_sd"]

    fake_proc = MagicMock()
    fake_proc.stdout = json.dumps(mock_output_data)
    monkeypatch.setattr("subprocess.run", lambda *a, **k: fake_proc)

    out_dir = tmp_path / "out"
    out_dir.mkdir()

    # 4. Run the parser
    # This will delete the extra keys we added to `mock_output_data`
    # and add `fair_parse_time`.
    run_parser(input_file, out_dir, force=True)

    # 5. Load the file produced by the parser
    produced_file = out_dir / f"fair_parsed_{input_file.stem}.json"
    assert produced_file.exists()
    produced_data = json.loads(produced_file.read_text(encoding="utf-8"))

    # 6. Check that fair_parse_time was added
    assert "metadata" in produced_data
    assert "fair_parse_time" in produced_data["metadata"]
    assert isinstance(produced_data["metadata"]["fair_parse_time"], float)

    # 7. Remove the generated fair_parse_time for comparison
    produced_data["metadata"].pop("fair_parse_time")

    # 8. Perform detailed field comparison
    # The `produced_data` should now match the *original* `reference_data`
    # since all the extra keys were removed by `run_parser`.

    # --- Check Metadata ---
    # The parser keeps the metadata block from the archive, but
    # `parse.py` *also* deletes keys from it.
    # We must compare against the *original* reference data *after*
    # simulating the same deletions.

    expected_metadata = copy.deepcopy(reference_data["metadata"])
    expected_metadata.pop("n_quantities", None)
    expected_metadata.pop("quantities", None)
    expected_metadata.pop("sections", None)
    expected_metadata.pop("section_defs", None)

    assert produced_data["metadata"] == expected_metadata

    # --- Check Run section ---
    assert produced_data["run"][0]["program"]["name"] == reference_data["run"][0]["program"]["name"]
    assert produced_data["run"][0]["program"]["version"] == reference_data["run"][0]["program"]["version"]

    # --- Check Method section ---
    assert (
        produced_data["run"][0]["method"][0]["dft"]["xc_functional"]["name"]
        == reference_data["run"][0]["method"][0]["dft"]["xc_functional"]["name"]
    )
    assert produced_data["run"][0]["method"][0]["electronic"]["method"] == "DFT"

    # --- Check System section ---
    assert (
        produced_data["run"][0]["system"][0]["chemical_composition_hill"]
        == reference_data["run"][0]["system"][0]["chemical_composition_hill"]
    )
    assert produced_data["run"][0]["system"][0]["atoms"]["periodic"] == [True, True, True]
    assert (
        produced_data["run"][0]["system"][0]["symmetry"][0]["crystal_system"]
        == reference_data["run"][0]["system"][0]["symmetry"][0]["crystal_system"]
    )

    # --- Check Calculation section ---
    assert (
        produced_data["run"][0]["calculation"][0]["energy"]["total"]["value"]
        == reference_data["run"][0]["calculation"][0]["energy"]["total"]["value"]
    )
    assert (
        produced_data["run"][0]["calculation"][0]["energy"]["fermi"]
        == reference_data["run"][0]["calculation"][0]["energy"]["fermi"]
    )
    # Check that scf_iteration list is present and has the correct number of items
    assert "scf_iteration" in produced_data["run"][0]["calculation"][0]
    assert len(produced_data["run"][0]["calculation"][0]["scf_iteration"]) == len(
        reference_data["run"][0]["calculation"][0]["scf_iteration"]
    )

    # --- Check Results section ---
    assert (
        produced_data["results"]["material"]["chemical_formula_descriptive"]
        == reference_data["results"]["material"]["chemical_formula_descriptive"]
    )
    assert (
        produced_data["results"]["material"]["symmetry"]["space_group_symbol"]
        == reference_data["results"]["material"]["symmetry"]["space_group_symbol"]
    )
    assert produced_data["results"]["material"]["topology"][0]["label"] == "original"
    assert produced_data["results"]["material"]["topology"][2]["label"] == "conventional cell"

    assert produced_data["results"]["method"]["method_name"] == reference_data["results"]["method"]["method_name"]
    assert (
        produced_data["results"]["method"]["simulation"]["program_name"]
        == reference_data["results"]["method"]["simulation"]["program_name"]
    )
    assert (
        produced_data["results"]["method"]["simulation"]["dft"]["jacobs_ladder"]
        == reference_data["results"]["method"]["simulation"]["dft"]["jacobs_ladder"]
    )

    assert (
        produced_data["results"]["properties"]["electronic"]["band_gap"][0]["value"]
        == reference_data["results"]["properties"]["electronic"]["band_gap"][0]["value"]
    )
    assert (
        produced_data["results"]["properties"]["electronic"]["dos_electronic"][0]["spin_polarized"]
        == reference_data["results"]["properties"]["electronic"]["dos_electronic"][0]["spin_polarized"]
    )

    # --- Final check: Compare the modified produced_data with the original reference_data ---
    # This ensures no *other* fields were accidentally dropped or modified

    expected_final_data = copy.deepcopy(reference_data)
    # Re-apply the metadata pops to the expected data for a final full comparison
    expected_final_data["metadata"].pop("n_quantities", None)
    expected_final_data["metadata"].pop("quantities", None)
    expected_final_data["metadata"].pop("sections", None)
    expected_final_data["metadata"].pop("section_defs", None)

    assert produced_data == expected_final_data


# --- [NEW TEST 0] ---
def test_parser_handles_parse_failure(tmp_path, monkeypatch, caplog):
    """
    Tests that run_parser correctly handles a failure
    from the subprocess.
    """
    # 1. Create a dummy input file
    input_file = tmp_path / "vasprun_bad.xml"
    input_file.write_text("<bad>content</bad>")

    # 2. Mock the subprocess.run to raise an error
    monkeypatch.setattr(
        "subprocess.run",
        MagicMock(
            side_effect=subprocess.CalledProcessError(returncode=1, cmd="nomad parse", stderr="File is not valid")
        ),
    )

    out_dir = tmp_path / "out"
    out_dir.mkdir()

    # 3. Run the parser and check that it raises the error
    with pytest.raises(subprocess.CalledProcessError):
        run_parser(input_file, out_dir, force=True)

    # 4. Check that the error was logged (optional)
    assert "NOMAD parsing command failed" in caplog.text
    # An unrelated failure gets no libmagic hint
    assert "brew install libmagic" not in caplog.text


def test_parser_hints_at_libmagic_when_nomad_cannot_load_it(tmp_path, monkeypatch, caplog):
    """
    `nomad parse` imports python-magic, which needs the system libmagic library. Without it, the cause
    is buried in NOMAD's traceback, so run_parser logs how to install libmagic.
    """
    input_file = tmp_path / "vasprun.xml"
    input_file.write_text("dummy")
    out_dir = tmp_path / "out"
    out_dir.mkdir()

    # Shortened stderr of `nomad parse` (nomad-lab 1.4.3) on a macOS runner without libmagic
    stderr = (
        "Traceback (most recent call last):\n"
        '  File ".../magic/loader.py", line 49, in load_lib\n'
        "    raise ImportError('failed to find libmagic.  Check your installation')\n"
        "ImportError: failed to find libmagic.  Check your installation\n"
        "\n"
        "During handling of the above exception, another exception occurred:\n"
        "\n"
        "Traceback (most recent call last):\n"
        '  File ".../nomad/cli/cli.py", line 81, in run_cli\n'
        "    if next(arg for arg in sys.argv if arg == '-v') is not None:\n"
        "StopIteration\n"
    )
    monkeypatch.setattr(
        "subprocess.run",
        MagicMock(side_effect=subprocess.CalledProcessError(returncode=1, cmd="nomad parse", stderr=stderr)),
    )

    with pytest.raises(subprocess.CalledProcessError):
        run_parser(input_file, out_dir, force=True)

    assert "NOMAD parsing command failed" in caplog.text
    assert "brew install libmagic" in caplog.text


# --- [NEW TEST 1] ---
@pytest.mark.parametrize("force_flag", [True, False])
def test_parser_handles_empty_nomad_output(tmp_path, monkeypatch, caplog, force_flag):
    """
    Tests that run_parser handles empty stdout from nomad,
    both with and without the --force flag.
    """
    input_file = tmp_path / "vasprun_empty.xml"
    input_file.write_text("dummy")

    out_dir = tmp_path / "out"
    out_dir.mkdir()

    # Mock subprocess.run to return an empty string
    fake_proc = MagicMock()
    fake_proc.stdout = ""
    fake_proc.stderr = ""
    fake_proc.returncode = 0
    monkeypatch.setattr("subprocess.run", lambda *a, **k: fake_proc)

    # Run parser
    skipped = run_parser(input_file, out_dir, force=force_flag)

    # It should not have skipped, but it also shouldn't crash
    assert not skipped
    assert "Parser returned no data" in caplog.text

    # It should not have created a file
    produced_file = out_dir / f"fair_parsed_{input_file.stem}.json"
    assert not produced_file.exists()


# --- [NEW TEST 2] ---
def test_parser_handles_invalid_json_output(tmp_path, monkeypatch, caplog):
    """
    Tests that run_parser raises JSONDecodeError if nomad
    returns non-JSON output.
    """
    input_file = tmp_path / "vasprun_bad_json.xml"
    input_file.write_text("dummy")

    out_dir = tmp_path / "out"
    out_dir.mkdir()

    # Mock subprocess.run to return invalid JSON
    fake_proc = MagicMock()
    fake_proc.stdout = "This is not JSON { not: valid }"
    fake_proc.stderr = ""
    fake_proc.returncode = 0
    monkeypatch.setattr("subprocess.run", lambda *a, **k: fake_proc)

    # Run parser and expect it to fail
    with pytest.raises(json.JSONDecodeError):
        run_parser(input_file, out_dir, force=True)

    # Check that the error was logged
    assert "Failed to decode JSON output" in caplog.text


# --- [NEW TEST 3] ---
@patch("subprocess.run")
def test_run_parser_skips_when_unchanged(mock_subprocess_run, tmp_path):
    """
    Tests that run_parser (the core function) *itself*
    correctly skips parsing when force=False and mtime is older.
    (Moved from test_parse_fairtime.py)
    """
    input_file = tmp_path / "vasprun_unchanged.xml"
    input_file.write_text("content")
    file_mtime = input_file.stat().st_mtime

    output_dir = tmp_path / "out"
    output_dir.mkdir()

    # Create an existing parsed JSON with fair_parse_time >= file mtime
    json_file = output_dir / f"fair_parsed_{input_file.stem}.json"
    json_content = {"metadata": {"fair_parse_time": file_mtime + 10}}
    json_file.write_text(json.dumps(json_content), encoding="utf-8")

    # Call run_parser directly, with force=False
    skipped = run_parser(input_file, output_dir, force=False)

    # Assert that run_parser *returned True* (indicating a skip)
    assert skipped

    # And double-check it didn't try to run nomad
    mock_subprocess_run.assert_not_called()


# --- [NEW TEST 4] ---
@patch("subprocess.run")
def test_run_parser_reparses_when_fair_parse_time_is_missing(mock_subprocess_run, tmp_path):
    """
    Tests that run_parser re-parses if the existing JSON
    is missing the 'fair_parse_time' key.
    (Moved from test_parse_fairtime.py)
    """
    input_file = tmp_path / "vasprun_no_time.xml"
    input_file.write_text("content")

    output_dir = tmp_path / "out"
    output_dir.mkdir()

    # Create an existing parsed JSON *without* fair_parse_time
    json_file = output_dir / f"fair_parsed_{input_file.stem}.json"
    json_content = {"metadata": {"some_other_key": "value"}}
    json_file.write_text(json.dumps(json_content), encoding="utf-8")

    # Mock the subprocess to return minimal valid output
    fake_proc = MagicMock()
    fake_proc.stdout = json.dumps({"metadata": {}, "run": []})
    fake_proc.stderr = ""
    fake_proc.returncode = 0
    mock_subprocess_run.return_value = fake_proc

    # Call run_parser directly, with force=False
    skipped = run_parser(input_file, output_dir, force=False)

    # Assert that run_parser *did not skip*
    assert not skipped

    # And check that it *did* call nomad
    mock_subprocess_run.assert_called_once()


# --- [NEW TEST 5] ---
@patch("subprocess.run")
def test_run_parser_reparses_when_file_is_newer(mock_subprocess_run, tmp_path):
    """
    Tests that run_parser re-parses if the input file
    is newer than the existing JSON's 'fair_parse_time'.
    """
    input_file = tmp_path / "vasprun_newer.xml"
    output_dir = tmp_path / "out"
    output_dir.mkdir()

    # Create an existing parsed JSON with an *old* timestamp
    json_file = output_dir / f"fair_parsed_{input_file.stem}.json"
    old_time = time.time() - 10
    json_content = {"metadata": {"fair_parse_time": old_time}}
    json_file.write_text(json.dumps(json_content), encoding="utf-8")

    # Wait a tiny bit to ensure the new file's mtime is measurably newer
    time.sleep(0.1)
    input_file.write_text("new content")
    assert input_file.stat().st_mtime > old_time

    # Mock the subprocess to return minimal valid output
    fake_proc = MagicMock()
    fake_proc.stdout = json.dumps({"metadata": {}, "run": []})
    fake_proc.stderr = ""
    fake_proc.returncode = 0
    mock_subprocess_run.return_value = fake_proc

    # Call run_parser directly, with force=False
    skipped = run_parser(input_file, output_dir, force=False)

    # Assert that run_parser *did not skip*
    assert not skipped

    # And check that it *did* call nomad
    mock_subprocess_run.assert_called_once()
