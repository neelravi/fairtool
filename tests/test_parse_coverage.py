import json
import logging
import subprocess
from unittest.mock import MagicMock, patch

import pytest

from fairtool.parse import _create_structure_json, _nomad_atoms_to_pymatgen, run_parser


def test_nomad_atoms_to_pymatgen_valid():
    """Test valid NOMAD atoms block conversion to pymatgen Structure."""
    atoms_block = {
        "lattice_vectors": [[5.43e-10, 0, 0], [0, 5.43e-10, 0], [0, 0, 5.43e-10]],
        "positions": [[0.0, 0.0, 0.0], [1.3575e-10, 1.3575e-10, 1.3575e-10]],
        "labels": ["Si", "Si"],
    }
    struct = _nomad_atoms_to_pymatgen(atoms_block)
    assert struct is not None
    assert len(struct.sites) == 2
    assert struct.composition.reduced_formula == "Si"


def test_nomad_atoms_to_pymatgen_invalid():
    """Test invalid NOMAD atoms block returns None on error."""
    assert _nomad_atoms_to_pymatgen({}) is None
    assert _nomad_atoms_to_pymatgen({"lattice_vectors": "bad"}) is None


def test_create_structure_json_conventional_topology(tmp_path):
    """Test _create_structure_json when conventional cell is directly in NOMAD topology."""
    full_data = {
        "results": {
            "material": {
                "structural_type": "bulk",
                "topology": [
                    {
                        "label": "conventional cell",
                        "atoms": {
                            "lattice_vectors": [[4e-10, 0, 0], [0, 4e-10, 0], [0, 0, 4e-10]],
                            "positions": [[0.0, 0.0, 0.0]],
                            "labels": ["Al"],
                        },
                    }
                ],
            }
        }
    }
    _create_structure_json(full_data, tmp_path, "test_calc")
    out_file = tmp_path / "fair-structure.json"
    assert out_file.exists()
    data = json.loads(out_file.read_text(encoding="utf-8"))
    assert data["formula"] == "Al"
    assert len(data["sites"]) == 1


def test_create_structure_json_fallback_primitive(tmp_path):
    """Test _create_structure_json falling back to primitive atoms when topology is missing."""
    full_data = {
        "results": {"material": {"topology": []}},
        "run": [
            {
                "system": [
                    {
                        "atoms": {
                            "lattice_vectors": [[3e-10, 0, 0], [0, 3e-10, 0], [0, 0, 3e-10]],
                            "positions": [[0.0, 0.0, 0.0]],
                            "labels": ["Fe"],
                        }
                    }
                ]
            }
        ],
    }
    _create_structure_json(full_data, tmp_path, "fallback_calc")
    out_file = tmp_path / "fair-structure.json"
    assert out_file.exists()
    data = json.loads(out_file.read_text(encoding="utf-8"))
    assert data["formula"] == "Fe"


def test_create_structure_json_ignores_conventional_cell_of_non_bulk_material(tmp_path, caplog):
    """
    In example08, a graphene sheet with adsorbed molecules, NOMAD's topology holds the conventional
    cell of the graphene subsystem: 2 C atoms, with a zero third lattice vector. The structure
    comes from the calculated system instead, without logging an error.
    """
    full_data = {
        "results": {
            "material": {
                "structural_type": "unavailable",
                "topology": [
                    {"label": "original"},
                    {"label": "subsystem", "structural_type": "2D"},
                    {
                        "label": "conventional cell",
                        "structural_type": "2D",
                        "atoms": {
                            "lattice_vectors": [[2.4813e-10, 0, 0], [-1.2407e-10, 2.1489e-10, 0], [0, 0, 0]],
                            "positions": [[1.2407e-10, 0.7163e-10, 0], [0, 1.4326e-10, 0]],
                            "labels": ["C", "C"],
                            "periodic": [True, True, False],
                        },
                    },
                ],
            }
        },
        "run": [
            {
                "system": [
                    {
                        "atoms": {
                            "lattice_vectors": [[8e-10, 0, 0], [0, 9e-10, 0], [0, 0, 10e-10]],
                            "positions": [
                                [1.0e-10, 1.2e-10, 5.0e-10],
                                [2.2e-10, 1.9e-10, 5.1e-10],
                                [3.1e-10, 3.7e-10, 6.4e-10],
                            ],
                            "labels": ["C", "C", "H"],
                        }
                    }
                ]
            }
        ],
    }
    _create_structure_json(full_data, tmp_path, "non_bulk_calc")
    data = json.loads((tmp_path / "fair-structure.json").read_text(encoding="utf-8"))
    assert data["formula"] == "HC2"
    assert len(data["sites"]) == 3
    assert not [record for record in caplog.records if record.levelno >= logging.ERROR]


def test_create_structure_json_no_structure(tmp_path):
    """Test _create_structure_json skips creation when no structure can be extracted."""
    full_data = {"results": {}}
    _create_structure_json(full_data, tmp_path, "no_struct_calc")
    assert not (tmp_path / "fair-structure.json").exists()


def test_create_structure_json_write_failure(tmp_path, monkeypatch):
    """Test _create_structure_json raises and logs when file writing fails."""
    full_data = {
        "results": {
            "material": {
                "structural_type": "bulk",
                "topology": [
                    {
                        "label": "conventional cell",
                        "atoms": {
                            "lattice_vectors": [[4e-10, 0, 0], [0, 4e-10, 0], [0, 0, 4e-10]],
                            "positions": [[0.0, 0.0, 0.0]],
                            "labels": ["Al"],
                        },
                    }
                ],
            }
        }
    }
    # Make open raise IOError
    orig_open = open

    def mock_open(path, *args, **kwargs):
        if "fair-structure.json" in str(path):
            raise IOError("Permission denied")
        return orig_open(path, *args, **kwargs)

    monkeypatch.setattr("builtins.open", mock_open)
    with pytest.raises(IOError):
        _create_structure_json(full_data, tmp_path, "fail_calc")


def test_run_parser_skip_and_comparison_branches(tmp_path):
    """Test skipping parse when unchanged, and handling corrupted comparison timestamps."""
    input_file = tmp_path / "vasprun.xml"
    input_file.write_text("<dummy>vasprun</dummy>", encoding="utf-8")
    out_dir = tmp_path / "out"
    out_dir.mkdir()

    json_output_path = out_dir / "fair_parsed_vasprun.json"

    # Case 1: Existing JSON with fair_parse_time >= file_mtime
    file_mtime = input_file.stat().st_mtime
    json_output_path.write_text(
        json.dumps({"metadata": {"fair_parse_time": file_mtime + 100}}),
        encoding="utf-8",
    )
    skipped = run_parser(input_file, out_dir, force=False)
    assert skipped is True

    # Case 2: Existing JSON with unparseable / invalid fair_parse_time
    json_output_path.write_text(
        json.dumps({"metadata": {"fair_parse_time": "invalid-float"}}),
        encoding="utf-8",
    )
    with patch("subprocess.run") as mock_run:
        mock_proc = MagicMock()
        mock_proc.stdout = json.dumps({"entry_name": "test", "run": []})
        mock_run.return_value = mock_proc
        skipped = run_parser(input_file, out_dir, force=False)
        assert skipped is False

    # Case 3: Existing JSON unreadable / corrupted
    json_output_path.write_text("{corrupt json", encoding="utf-8")
    with patch("subprocess.run") as mock_run:
        mock_proc = MagicMock()
        mock_proc.stdout = json.dumps({"entry_name": "test", "run": []})
        mock_run.return_value = mock_proc
        skipped = run_parser(input_file, out_dir, force=False)
        assert skipped is False


def test_run_parser_empty_stdout(tmp_path):
    """Test run_parser when NOMAD returns empty output."""
    input_file = tmp_path / "vasprun.xml"
    input_file.write_text("<vasp></vasp>", encoding="utf-8")
    out_dir = tmp_path / "out"
    out_dir.mkdir()

    with patch("subprocess.run") as mock_run:
        mock_proc = MagicMock()
        mock_proc.stdout = ""
        mock_run.return_value = mock_proc

        result = run_parser(input_file, out_dir, force=True)
        assert result is False


def test_run_parser_filters_and_metadata_handling(tmp_path):
    """Test run_parser filtering k_mesh.points.im and populating missing metadata."""
    input_file = tmp_path / "vasprun.xml"
    input_file.write_text("<vasp></vasp>", encoding="utf-8")
    out_dir = tmp_path / "out"
    out_dir.mkdir()

    raw_output = {
        "run": [
            {
                "method": [{"k_mesh": {"points": {"re": [1, 2, 3], "im": [0, 0, 0]}}}],
                "calculation": [{"energy": {}}],
            }
        ],
        "entry_name": "remove_me",
        "n_quantities": 42,
    }

    with patch("subprocess.run") as mock_run:
        mock_proc = MagicMock()
        mock_proc.stdout = json.dumps(raw_output)
        mock_run.return_value = mock_proc

        result = run_parser(input_file, out_dir, force=True)
        assert result is False

    saved_json = out_dir / "fair_parsed_vasprun.json"
    assert saved_json.exists()
    saved_data = json.loads(saved_json.read_text(encoding="utf-8"))
    assert "entry_name" not in saved_data
    assert "im" not in saved_data["run"][0]["method"][0]["k_mesh"]["points"]
    assert "fair_parse_time" in saved_data["metadata"]


def test_run_parser_save_failure_unlinks_file(tmp_path, monkeypatch):
    """Test run_parser deletes output file if saving fails."""
    input_file = tmp_path / "vasprun.xml"
    input_file.write_text("<vasp></vasp>", encoding="utf-8")
    out_dir = tmp_path / "out"
    out_dir.mkdir()

    with patch("subprocess.run") as mock_run:
        mock_proc = MagicMock()
        mock_proc.stdout = json.dumps({"test": "ok"})
        mock_run.return_value = mock_proc

        # Monkeypatch json.dump to raise an error
        def mock_dump(*args, **kwargs):
            raise OSError("Failed to write full json")

        monkeypatch.setattr(json, "dump", mock_dump)
        with pytest.raises(OSError):
            run_parser(input_file, out_dir, force=True)


def test_run_parser_exceptions(tmp_path):
    """Test run_parser handling FileNotFoundError, CalledProcessError, JSONDecodeError, Exception."""
    input_file = tmp_path / "vasprun.xml"
    input_file.write_text("<vasp></vasp>", encoding="utf-8")
    out_dir = tmp_path / "out"
    out_dir.mkdir()

    # FileNotFoundError (nomad missing)
    with patch("subprocess.run", side_effect=FileNotFoundError("nomad not found")):
        with pytest.raises(FileNotFoundError):
            run_parser(input_file, out_dir, force=True)

    # CalledProcessError (nomad command failed)
    with patch("subprocess.run", side_effect=subprocess.CalledProcessError(1, "nomad", stderr="error")):
        with pytest.raises(subprocess.CalledProcessError):
            run_parser(input_file, out_dir, force=True)

    # JSONDecodeError (invalid JSON output)
    with patch("subprocess.run") as mock_run:
        mock_proc = MagicMock()
        mock_proc.stdout = "Invalid JSON output from parser"
        mock_run.return_value = mock_proc
        with pytest.raises(json.JSONDecodeError):
            run_parser(input_file, out_dir, force=True)

    # Generic Exception
    with patch("subprocess.run", side_effect=RuntimeError("Unexpected error")):
        with pytest.raises(RuntimeError):
            run_parser(input_file, out_dir, force=True)
