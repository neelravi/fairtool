import json

import pandas as pd
import pytest
import yaml

from fairtool.analyze import perform_single_file_analysis, run_analysis


@pytest.fixture
def sample_parsed_data():
    """Returns a representative parsed data dictionary."""
    return {
        "results": {
            "properties": {
                "energy": {"total": {"value": -123.456}},
                "electronic": {"band_structure": {"band_gap": [{"value": 1.42}]}},
            },
            "workflow": [{"calculation_converged": True}],
        }
    }


def test_perform_single_file_analysis_success(sample_parsed_data):
    """Test extracting energy, band gap, and convergence successfully."""
    result = perform_single_file_analysis(sample_parsed_data, {}, "calc_01")
    assert result["identifier"] == "calc_01"
    assert result["total_energy_eV"] == -123.456
    assert result["band_gap_eV"] == 1.42
    assert result["converged"] is True


def test_perform_single_file_analysis_empty_data():
    """Test gracefully handling empty dictionary without errors."""
    result = perform_single_file_analysis({}, {}, "empty_calc")
    assert result["identifier"] == "empty_calc"
    assert result["total_energy_eV"] is None
    assert result["band_gap_eV"] is None
    assert result["converged"] is None


def test_perform_single_file_analysis_malformed_structures():
    """Test extracting from unexpected non-dict values."""
    malformed = {"results": {"properties": "not-a-dict", "workflow": "not-a-list"}}
    result = perform_single_file_analysis(malformed, {}, "malformed_calc")
    assert result["total_energy_eV"] is None
    assert result["band_gap_eV"] is None
    assert result["converged"] is None


def test_run_analysis_single_file(tmp_path, sample_parsed_data):
    """Test run_analysis on a single JSON file."""
    json_file = tmp_path / "vasp_parsed.json"
    json_file.write_text(json.dumps(sample_parsed_data), encoding="utf-8")
    out_dir = tmp_path / "output"
    out_dir.mkdir()

    run_analysis(json_file, out_dir, None)

    # Check individual analysis yaml is created
    yaml_file = out_dir / "vasp_parsed_analysis.yaml"
    assert yaml_file.exists()
    with open(yaml_file, "r") as f:
        data = yaml.safe_load(f)
    assert data["total_energy_eV"] == -123.456

    # Check aggregate CSV is created
    csv_file = out_dir / "analysis_summary.csv"
    assert csv_file.exists()
    df = pd.read_csv(csv_file)
    assert len(df) == 1
    assert df.loc[0, "identifier"] == "vasp_parsed"


def test_run_analysis_directory(tmp_path, sample_parsed_data):
    """Test run_analysis on a directory containing multiple parsed files."""
    calc_dir = tmp_path / "calcs"
    calc_dir.mkdir()
    (calc_dir / "calc1_parsed.json").write_text(json.dumps(sample_parsed_data), encoding="utf-8")
    (calc_dir / "calc2_parsed.json").write_text(json.dumps(sample_parsed_data), encoding="utf-8")

    out_dir = tmp_path / "output"
    out_dir.mkdir()

    run_analysis(calc_dir, out_dir, None)

    assert (out_dir / "calc1_parsed_analysis.yaml").exists()
    assert (out_dir / "calc2_parsed_analysis.yaml").exists()

    csv_file = out_dir / "analysis_summary.csv"
    assert csv_file.exists()
    df = pd.read_csv(csv_file)
    assert len(df) == 2


def test_run_analysis_with_config(tmp_path, sample_parsed_data):
    """Test run_analysis with a custom YAML configuration file."""
    json_file = tmp_path / "vasp_parsed.json"
    json_file.write_text(json.dumps(sample_parsed_data), encoding="utf-8")
    config_file = tmp_path / "config.yaml"
    config_file.write_text("custom_setting: true\n", encoding="utf-8")
    out_dir = tmp_path / "output"
    out_dir.mkdir()

    run_analysis(json_file, out_dir, config_file)
    assert (out_dir / "vasp_parsed_analysis.yaml").exists()


def test_run_analysis_corrupted_json(tmp_path):
    """Test run_analysis handles corrupted JSON without raising exception."""
    bad_json = tmp_path / "bad_parsed.json"
    bad_json.write_text("{ incomplete json ...", encoding="utf-8")
    out_dir = tmp_path / "output"
    out_dir.mkdir()

    run_analysis(bad_json, out_dir, None)
    # The corrupted file should be skipped; no aggregate CSV created
    assert not (out_dir / "analysis_summary.csv").exists()


def test_run_analysis_empty_directory(tmp_path):
    """Test run_analysis when no matching parsed JSON files exist."""
    empty_dir = tmp_path / "empty"
    empty_dir.mkdir()
    out_dir = tmp_path / "output"
    out_dir.mkdir()

    run_analysis(empty_dir, out_dir, None)
    assert not (out_dir / "analysis_summary.csv").exists()


def test_run_analysis_invalid_input_path(tmp_path):
    """Test run_analysis when input_path is neither a JSON file nor valid."""
    text_file = tmp_path / "dummy.txt"
    text_file.write_text("plain text", encoding="utf-8")
    out_dir = tmp_path / "output"
    out_dir.mkdir()

    run_analysis(text_file, out_dir, None)
    assert not (out_dir / "analysis_summary.csv").exists()


def test_run_analysis_bad_config_file(tmp_path, sample_parsed_data):
    """Test run_analysis when config file fails to load."""
    json_file = tmp_path / "vasp_parsed.json"
    json_file.write_text(json.dumps(sample_parsed_data), encoding="utf-8")
    bad_config = tmp_path / "bad_config.yaml"
    bad_config.write_text(":\n  - invalid yaml : {", encoding="utf-8")
    out_dir = tmp_path / "output"
    out_dir.mkdir()

    # Should log error and proceed without crashing
    run_analysis(json_file, out_dir, bad_config)
    assert (out_dir / "vasp_parsed_analysis.yaml").exists()


def test_run_analysis_single_file_exception(tmp_path, sample_parsed_data, monkeypatch):
    """Test run_analysis when perform_single_file_analysis raises an exception."""
    json_file = tmp_path / "vasp_parsed.json"
    json_file.write_text(json.dumps(sample_parsed_data), encoding="utf-8")
    out_dir = tmp_path / "output"
    out_dir.mkdir()

    import fairtool.analyze

    def mock_perform(*args, **kwargs):
        raise RuntimeError("Unexpected failure in analysis")

    monkeypatch.setattr(fairtool.analyze, "perform_single_file_analysis", mock_perform)
    run_analysis(json_file, out_dir, None)
    assert not (out_dir / "vasp_parsed_analysis.yaml").exists()


def test_run_analysis_aggregate_save_failure(tmp_path, sample_parsed_data, monkeypatch):
    """Test run_analysis when saving aggregate CSV fails."""
    json_file = tmp_path / "vasp_parsed.json"
    json_file.write_text(json.dumps(sample_parsed_data), encoding="utf-8")
    out_dir = tmp_path / "output"
    out_dir.mkdir()

    def mock_to_csv(self, *args, **kwargs):
        raise IOError("Disk full or permission denied")

    monkeypatch.setattr(pd.DataFrame, "to_csv", mock_to_csv)
    run_analysis(json_file, out_dir, None)
    assert (out_dir / "vasp_parsed_analysis.yaml").exists()
