"""
Regression tests for --output with several calculations.

Calculations in different directories often have input files with the same name (e.g.
vasprun.xml). Each must keep its own outputs under the output directory, instead of
overwriting the others or being skipped as an unchanged copy of them.
"""

import json
import os
import subprocess
import time
from pathlib import Path

import pandas as pd
import pytest
from typer.testing import CliRunner

from fairtool.cli import _output_dir_for, app

runner = CliRunner()

# Each calculation's subdirectory below the searched directory, and the element in its
# cell. Two of the calculations are in directories that also share a name.
CALCULATIONS = {".": "Si", "A/run1": "Cu", "B/run1": "Al"}


def _archive(element: str) -> dict:
    """A minimal NOMAD archive of a one-atom cubic cell of `element`."""
    return {
        "metadata": {"entry_name": f"{element} calculation"},
        "run": [
            {
                "system": [
                    {
                        "atoms": {
                            "lattice_vectors": [[3e-10, 0, 0], [0, 3e-10, 0], [0, 0, 3e-10]],
                            "positions": [[0, 0, 0]],
                            "labels": [element],
                        }
                    }
                ]
            }
        ],
    }


@pytest.fixture
def calc_root(tmp_path):
    """A directory with a vasprun.xml for each calculation; each file holds its element."""
    root = tmp_path / "calcs"
    for subdir, element in CALCULATIONS.items():
        (root / subdir).mkdir(parents=True, exist_ok=True)
        (root / subdir / "vasprun.xml").write_text(element, encoding="utf-8")
    return root


@pytest.fixture
def nomad_calls(monkeypatch):
    """Fakes `nomad parse` with the archive of the element in the input file, and records the files it parses."""
    calls = []

    def fake_nomad(command, **kwargs):
        input_file = Path(command[-1])
        calls.append(input_file)
        stdout = json.dumps(_archive(input_file.read_text(encoding="utf-8")))
        return subprocess.CompletedProcess(command, 0, stdout=stdout, stderr="")

    monkeypatch.setattr("subprocess.run", fake_nomad)
    return calls


def _assert_parsed_apart(out_dir: Path, calculations: dict):
    """Each calculation has its own parsed JSON and structure, in its subdirectory of out_dir."""
    for subdir, element in calculations.items():
        parsed = json.loads((out_dir / subdir / "fair_parsed_vasprun.json").read_text(encoding="utf-8"))
        assert parsed["run"][0]["system"][0]["atoms"]["labels"] == [element]
        structure = json.loads((out_dir / subdir / "fair-structure.json").read_text(encoding="utf-8"))
        assert structure["formula"] == element


@pytest.mark.parametrize(
    ("input_path", "output_dir", "expected"),
    [
        # Without --output, the outputs go next to the input file
        ("calcs", None, "calcs/A/run1"),
        # With --output, the input file keeps its subdirectory below the searched directory
        ("calcs", "out", "out/A/run1"),
        ("calcs/A", "out", "out/run1"),
        # A single input file writes straight into the output directory
        ("calcs/A/run1/vasprun.xml", "out", "out"),
    ],
)
def test_output_dir_for(tmp_path, input_path, output_dir, expected):
    calc_file = tmp_path / "calcs" / "A" / "run1" / "vasprun.xml"
    calc_file.parent.mkdir(parents=True)
    calc_file.write_text("Si", encoding="utf-8")
    output_path = tmp_path / output_dir if output_dir else None

    assert _output_dir_for(calc_file, tmp_path / input_path, output_path) == tmp_path / expected


def test_parse_output_keeps_same_named_calculations_apart(calc_root, nomad_calls, tmp_path):
    """Regression: `fair parse -r -o` parsed only the first of several vasprun.xml and kept one structure."""
    out_dir = tmp_path / "out"

    result = runner.invoke(app, ["parse", str(calc_root), "-r", "-y", "-o", str(out_dir)])

    assert result.exit_code == 0
    # Every calculation is parsed; none is skipped as an unchanged copy of another
    assert sorted(nomad_calls) == sorted(calc_root / subdir / "vasprun.xml" for subdir in CALCULATIONS)
    _assert_parsed_apart(out_dir, CALCULATIONS)


def test_parse_output_skips_only_unchanged_calculations(calc_root, nomad_calls, tmp_path):
    """Parsing into an output directory again skips exactly the calculations whose input has not changed."""
    out_dir = tmp_path / "out"
    parse_args = ["parse", str(calc_root), "-r", "-y", "-o", str(out_dir)]
    assert runner.invoke(app, parse_args).exit_code == 0

    # Nothing changed, so nothing is parsed again
    nomad_calls.clear()
    assert runner.invoke(app, parse_args).exit_code == 0
    assert nomad_calls == []

    # Only the calculation whose input changed is parsed again
    changed = calc_root / "A" / "run1" / "vasprun.xml"
    changed.write_text("Ni", encoding="utf-8")
    later = time.time() + 60
    os.utime(changed, (later, later))
    assert runner.invoke(app, parse_args).exit_code == 0
    assert nomad_calls == [changed]
    _assert_parsed_apart(out_dir, {**CALCULATIONS, "A/run1": "Ni"})


def test_all_output_keeps_same_named_calculations_apart(calc_root, nomad_calls, tmp_path):
    """Regression: `fair all -r -o` parsed, analyzed and summarized only one of several vasprun.xml."""
    out_dir = tmp_path / "out"

    result = runner.invoke(app, ["all", str(calc_root), "-r", "-y", "-o", str(out_dir)])

    assert result.exit_code == 0
    assert len(nomad_calls) == len(CALCULATIONS)
    _assert_parsed_apart(out_dir, CALCULATIONS)
    for subdir, element in CALCULATIONS.items():
        # The summary sits next to the fair-structure.json that its structure viewer loads
        summary = (out_dir / subdir / "fair_summarized_vasprun.md").read_text(encoding="utf-8")
        assert f"{element} calculation" in summary
        assert (out_dir / subdir / "fair_parsed_vasprun_analysis.yaml").exists()
    identifiers = pd.read_csv(out_dir / "analysis_summary.csv")["identifier"]
    assert sorted(identifiers) == ["A/run1/fair_parsed_vasprun", "B/run1/fair_parsed_vasprun", "fair_parsed_vasprun"]


def test_summarize_output_keeps_same_named_calculations_apart(tmp_path):
    """Regression: `fair summarize -o` wrote one summary and skipped the others as already existing."""
    parsed_root = tmp_path / "parsed"
    for subdir, element in CALCULATIONS.items():
        (parsed_root / subdir).mkdir(parents=True, exist_ok=True)
        parsed_file = parsed_root / subdir / "fair_parsed_vasprun.json"
        parsed_file.write_text(json.dumps(_archive(element)), encoding="utf-8")
    out_dir = tmp_path / "out"

    result = runner.invoke(app, ["summarize", str(parsed_root), "-o", str(out_dir)])

    assert result.exit_code == 0
    for subdir, element in CALCULATIONS.items():
        summary = (out_dir / subdir / "fair_summarized_vasprun.md").read_text(encoding="utf-8")
        assert f"{element} calculation" in summary
