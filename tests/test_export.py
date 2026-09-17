import json

import pandas as pd
import pytest
import yaml

from fairtool.export import run_export


@pytest.fixture
def sample_csv_data(tmp_path):
    """Creates a sample CSV file and directory containing analysis_summary.csv."""
    df = pd.DataFrame(
        [
            {"identifier": "calc_01", "total_energy_eV": -120.5, "band_gap_eV": 1.5, "converged": True},
            {"identifier": "calc_02", "total_energy_eV": -140.2, "band_gap_eV": 0.0, "converged": True},
        ]
    )
    csv_file = tmp_path / "analysis_summary.csv"
    df.to_csv(csv_file, index=False)
    return {"df": df, "csv_file": csv_file, "dir": tmp_path}


def test_run_export_csv_from_file(sample_csv_data, tmp_path):
    """Test exporting to CSV from an input CSV file."""
    out_dir = tmp_path / "out_csv"
    out_dir.mkdir()

    run_export(sample_csv_data["csv_file"], out_dir, "csv")
    exported_file = out_dir / "exported_data.csv"
    assert exported_file.exists()

    df_exported = pd.read_csv(exported_file)
    assert len(df_exported) == 2
    assert "identifier" in df_exported.columns


def test_run_export_csv_from_directory(sample_csv_data, tmp_path):
    """Test exporting to CSV from a directory containing analysis_summary.csv."""
    out_dir = tmp_path / "out_csv_dir"
    out_dir.mkdir()

    run_export(sample_csv_data["dir"], out_dir, "csv")
    assert (out_dir / "exported_data.csv").exists()


def test_run_export_yaml_from_dataframe(sample_csv_data, tmp_path):
    """Test exporting data to YAML format."""
    out_dir = tmp_path / "out_yaml"
    out_dir.mkdir()

    run_export(sample_csv_data["csv_file"], out_dir, "yaml")
    exported_file = out_dir / "exported_data.yaml"
    assert exported_file.exists()

    with open(exported_file, "r") as f:
        data = yaml.safe_load(f)
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["identifier"] == "calc_01"


def test_run_export_json_summary_with_identifier(sample_csv_data, tmp_path):
    """Test exporting to JSON summary indexed by identifier."""
    out_dir = tmp_path / "out_json"
    out_dir.mkdir()

    run_export(sample_csv_data["csv_file"], out_dir, "json_summary")
    exported_file = out_dir / "exported_summary.json"
    assert exported_file.exists()

    with open(exported_file, "r") as f:
        data = json.load(f)
    assert "calc_01" in data
    assert data["calc_01"]["total_energy_eV"] == -120.5


def test_run_export_json_summary_without_identifier(tmp_path):
    """Test exporting to JSON summary when identifier column is missing."""
    df = pd.DataFrame([{"energy": -10.0}, {"energy": -20.0}])
    csv_file = tmp_path / "no_id.csv"
    df.to_csv(csv_file, index=False)

    out_dir = tmp_path / "out_json_noid"
    out_dir.mkdir()

    run_export(csv_file, out_dir, "json_summary")
    exported_file = out_dir / "exported_summary.json"
    assert exported_file.exists()
    with open(exported_file, "r") as f:
        data = json.load(f)
    assert isinstance(data, list)


def test_run_export_unsupported_format(sample_csv_data, tmp_path):
    """Test handling of unsupported export format."""
    out_dir = tmp_path / "out_unsupported"
    out_dir.mkdir()

    run_export(sample_csv_data["csv_file"], out_dir, "unknown_format")
    assert not (out_dir / "exported_data.unknown_format").exists()


def test_run_export_missing_source(tmp_path):
    """Test behavior when input data source does not exist."""
    missing_dir = tmp_path / "missing_dir"
    missing_dir.mkdir()
    out_dir = tmp_path / "out_missing"
    out_dir.mkdir()

    run_export(missing_dir, out_dir, "csv")
    assert not (out_dir / "exported_data.csv").exists()


def test_run_export_corrupted_csv(tmp_path):
    """Test handling of unparseable CSV input."""
    bad_csv = tmp_path / "corrupted.csv"
    bad_csv.write_bytes(b"\x00\xff\xfe\xff")
    out_dir = tmp_path / "out_bad"
    out_dir.mkdir()

    run_export(bad_csv, out_dir, "csv")
    assert not (out_dir / "exported_data.csv").exists()


def test_run_export_corrupted_csv_in_directory(tmp_path):
    """Test handling of unparseable analysis_summary.csv inside directory."""
    bad_dir = tmp_path / "bad_dir"
    bad_dir.mkdir()
    bad_csv = bad_dir / "analysis_summary.csv"
    bad_csv.write_bytes(b"\x00\xff\xfe\xff")
    out_dir = tmp_path / "out_bad_dir"
    out_dir.mkdir()

    run_export(bad_dir, out_dir, "csv")
    assert not (out_dir / "exported_data.csv").exists()


def test_run_export_csv_non_dataframe(sample_csv_data, tmp_path, monkeypatch):
    """Test CSV export when loaded data is not a DataFrame."""
    out_dir = tmp_path / "out_non_df"
    out_dir.mkdir()

    # Monkeypatch pd.read_csv to return a dict
    monkeypatch.setattr(pd, "read_csv", lambda *args, **kwargs: {"not": "a dataframe"})
    run_export(sample_csv_data["csv_file"], out_dir, "csv")
    assert not (out_dir / "exported_data.csv").exists()


def test_run_export_yaml_and_json_from_list_and_dict(sample_csv_data, tmp_path, monkeypatch):
    """Test YAML and JSON summary export when data is a list or dict."""
    out_dir = tmp_path / "out_list_dict"
    out_dir.mkdir()

    monkeypatch.setattr(pd, "read_csv", lambda *args, **kwargs: [{"item": 1}, {"item": 2}])
    run_export(sample_csv_data["csv_file"], out_dir, "yaml")
    assert (out_dir / "exported_data.yaml").exists()

    run_export(sample_csv_data["csv_file"], out_dir, "json_summary")
    assert (out_dir / "exported_summary.json").exists()


def test_run_export_unsupported_data_types(sample_csv_data, tmp_path, monkeypatch):
    """Test YAML and JSON export when loaded data is an unsupported type (e.g., int/set)."""
    out_dir = tmp_path / "out_unsupported_types"
    out_dir.mkdir()

    monkeypatch.setattr(pd, "read_csv", lambda *args, **kwargs: 12345)
    run_export(sample_csv_data["csv_file"], out_dir, "yaml")
    assert not (out_dir / "exported_data.yaml").exists()

    run_export(sample_csv_data["csv_file"], out_dir, "json_summary")
    assert not (out_dir / "exported_summary.json").exists()


def test_run_export_write_exception_raised(sample_csv_data, tmp_path, monkeypatch):
    """Test that unexpected exceptions during export are logged and re-raised."""
    out_dir = tmp_path / "out_err"
    out_dir.mkdir()

    def mock_to_csv(self, *args, **kwargs):
        raise OSError("Disk write error")

    monkeypatch.setattr(pd.DataFrame, "to_csv", mock_to_csv)
    with pytest.raises(OSError):
        run_export(sample_csv_data["csv_file"], out_dir, "csv")
