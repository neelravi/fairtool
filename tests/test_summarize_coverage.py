import json
from unittest.mock import patch

import numpy as np
import pytest

from fairtool.parse import ELEMENTARY_CHARGE_VALUE as EV
from fairtool.summarize import (
    _add_row,
    _as_qty,
    _convert_field,
    _extract_energy_lists,
    _format_field_numeric,
    _generate_dos_chart_html,
    _generate_final_energies_table,
    _generate_kpoints_table,
    _generate_lattice_table,
    _generate_material_composition_table,
    _generate_metadata_table,
    _generate_scf_chart_html,
    _generate_scf_energies_table,
    _generate_symmetry_table,
    _scalar,
    _strip_parens,
    extract_context,
    generate_markdown,
    load_data,
    run_summarization,
    save_report,
    u,
)


def test_scalar_helper():
    """Test _scalar unwrap behavior."""
    assert _scalar([42]) == 42
    assert _scalar((99,)) == 99
    assert _scalar([1, 2]) == [1, 2]
    assert _scalar(10) == 10


def test_as_qty_helper():
    """Test _as_qty handling of sentinels and invalid inputs."""
    assert _as_qty(None, u.m) is None
    assert _as_qty("unavailable", u.m) is None
    assert _as_qty("not_a_number", u.m) is None
    qty = _as_qty([5.0], u.m)
    assert qty is not None
    assert qty.magnitude == 5.0


def test_convert_field_helper():
    """Test _convert_field unknown field, default fallback, and numeric return."""
    with pytest.raises(KeyError):
        _convert_field(1.0, "unknown_field_name")

    assert _convert_field("unavailable", "a", default="N/A") == "N/A"
    num = _convert_field(5.43e-10, "a", return_numeric=True)
    assert abs(num - 5.43) < 1e-4
    text = _convert_field(5.43e-10, "a", return_numeric=False)
    assert "5.430 Å" in text


def test_strip_parens_helper():
    """Test _strip_parens with various edge inputs."""
    assert _strip_parens(None) == "unavailable"
    assert _strip_parens("") == "unavailable"
    assert _strip_parens("   ") == "unavailable"
    assert _strip_parens(" (something) ") == "unavailable"
    assert _strip_parens("VASP (version 5.4.4)") == "VASP"
    assert _strip_parens("SimpleText") == "SimpleText"


def test_format_field_numeric_helper():
    """Test _format_field_numeric error branches."""
    assert _format_field_numeric(None, "a", default="—") == "—"
    assert _format_field_numeric(5.43e-10, "nonexistent_field", default="—") == "—"


def test_extract_energy_lists_division_and_none():
    """Test _extract_energy_lists with None and division errors."""
    iterations = [
        {"energy": {"total": {"value": None}}},
        {"energy": {"total": {"value": 1.602176634e-19}}},
        {"energy": {}},
    ]
    ev_list, j_list = _extract_energy_lists(iterations, "total")
    assert np.isnan(ev_list[0])
    assert np.isnan(j_list[0])
    assert abs(ev_list[1] - 1.0) < 1e-6
    assert np.isnan(ev_list[2])


def test_load_data_edge_cases(tmp_path):
    """Test load_data with non-dict JSON, empty dict, and corrupt file."""
    # Non-dict JSON
    list_json = tmp_path / "list.json"
    list_json.write_text("[1, 2, 3]", encoding="utf-8")
    assert load_data(list_json) is None

    # Empty dict
    empty_json = tmp_path / "empty.json"
    empty_json.write_text("{}", encoding="utf-8")
    assert load_data(empty_json) is None

    # Corrupt file
    corrupt_json = tmp_path / "corrupt.json"
    corrupt_json.write_text("{ incomplete", encoding="utf-8")
    assert load_data(corrupt_json) is None


def _eigenvalues(energies_eV, occupations):
    """An `eigenvalues` block, shaped (spin channel, k-point, band), with the energies in joules."""
    return {"energies": (np.asarray(energies_eV) * EV).tolist(), "occupations": occupations}


def test_extract_context_topology_and_energies():
    """Test extract_context with non-dict topology and energy calculations."""
    data = {
        "results": {
            "material": {
                "topology": [
                    "not-a-dict",  # Should be skipped
                    {"label": "original", "cell": {"a": 5e-10}},
                    {"label": "primitive cell", "cell": {"a": 5e-10}, "symmetry": {"crystal_system": "Cubic"}},
                ]
            },
            "method": {"simulation": {}},
        },
        "run": [
            {
                "calculation": [
                    {
                        "energy": {
                            "total": {"value": -1.602176634e-19},
                            "custom_free": {"value": None},
                        },
                        # Highest occupied state at 1.0 eV, lowest unoccupied at 3.5 eV
                        "eigenvalues": [_eigenvalues([[[1.0, 3.5], [0.5, 4.0]]], [[[1.0, 0.0], [1.0, 0.0]]])],
                    }
                ]
            }
        ],
    }
    ctx = extract_context(data)
    assert abs(ctx["final_energies_ev"]["total"] - (-1.0)) < 1e-6
    assert abs(ctx["final_energies_ev"]["band_gap"] - 2.5) < 1e-6
    assert ctx["original_cell"]["a"] == 5e-10
    assert ctx["t_cell_data_sym"]["crystal_system"] == "Cubic"


def test_extract_context_uses_final_calculation():
    """
    For a relaxation, report the last ionic step, not the first. As in example06, only the
    last step holds the eigenvalues and the DOS.
    """
    first_step = {
        "energy": {"total": {"value": -9.0 * EV}},
        "scf_iteration": [{"energy": {"total": {"value": -8.0 * EV}}}] * 3,
    }
    final_step = {
        "energy": {"total": {"value": -10.0 * EV}},
        "scf_iteration": [{"energy": {"total": {"value": -10.0 * EV}}}] * 2,
        "eigenvalues": [_eigenvalues([[[1.0, 2.0], [1.5, 2.5]]], [[[1.0, 0.0], [1.0, 0.0]]])],
        "dos_electronic": [{"energies": [1e-19, 2e-19], "energy_fermi": 1e-19, "total": [{"value": [4.0, 5.0]}]}],
    }
    ctx = extract_context({"run": [{"calculation": [first_step, final_step]}]})

    assert ctx["final_energies_ev"]["total"] == pytest.approx(-10.0)
    assert ctx["final_energies_ev"]["band_gap"] == pytest.approx(0.5)
    assert [row["total_ev"] for row in ctx["scf_table_data"]] == pytest.approx([-10.0, -10.0])
    assert len(ctx["dos_chart_data"]) == 2


@pytest.mark.parametrize(
    ("calculation", "band_gap"),
    [
        # A metal: the second band is filled at the first k-point and empty at the second
        ({"eigenvalues": [_eigenvalues([[[3.0, 4.0], [3.5, 4.1]]], [[[1.0, 1.0], [1.0, 0.0]]])]}, 0.0),
        # A band-structure run keeps its eigenvalues in the segments of the band path
        (
            {
                "band_structure_electronic": [
                    {
                        "segment": [
                            _eigenvalues([[[1.0, 3.0]]], [[[1.0, 0.0]]]),
                            _eigenvalues([[[1.5, 2.5]]], [[[1.0, 0.0]]]),
                        ]
                    }
                ]
            },
            1.0,
        ),
    ],
    ids=["metal", "band_path"],
)
def test_extract_context_derives_band_gap(calculation, band_gap):
    """The band gap comes from the eigenvalues, and a metal's gap of 0 still gets a row."""
    ctx = extract_context({"run": [{"calculation": [calculation]}]})

    assert ctx["final_energies_ev"]["band_gap"] == pytest.approx(band_gap)
    assert f"| **Band Gap** | {band_gap:.6f} |" in _generate_final_energies_table(ctx)


@pytest.mark.parametrize(
    "calculation",
    [
        # Archives from older NOMAD versions store `band_gap[*].value`, which can be wrong:
        # 7.23 eV for metallic Cs2AgHgCl6 in example01. It is not used.
        {"band_gap": [{"value": 7.2254 * EV}]},
        # Without unoccupied states there is no gap to measure
        {"eigenvalues": [_eigenvalues([[[1.0, 2.0], [1.5, 2.5]]], [[[1.0, 1.0], [1.0, 1.0]]])]},
        # Energies and occupations of different shapes
        {"eigenvalues": [_eigenvalues([[[1.0, 2.0], [1.5, 2.5]]], [[[1.0], [1.0]]])]},
    ],
    ids=["stored_value_only", "all_occupied", "shape_mismatch"],
)
def test_extract_context_without_band_gap(calculation):
    """No Band Gap row when the eigenvalues cannot give one."""
    ctx = extract_context({"run": [{"calculation": [{"energy": {"total": {"value": -EV}}, **calculation}]}]})

    assert "band_gap" not in ctx["final_energies_ev"]
    assert "Band Gap" not in _generate_final_energies_table(ctx)


def test_extract_context_dos_spin_polarized():
    """Test extract_context with spin-polarized DOS (dos_up and dos_down)."""
    energies_j = [1e-19, 2e-19, 3e-19]
    fermi_j = 2e-19
    data = {
        "run": [
            {
                "calculation": [
                    {
                        "dos_electronic": [
                            {
                                "energies": energies_j,
                                "energy_fermi": fermi_j,
                                "spin_polarized": True,
                                "total": [
                                    {"value": [1.0, 2.0, 3.0]},
                                    {"value": [0.5, 1.5, 2.5]},
                                ],
                            }
                        ]
                    }
                ]
            }
        ]
    }
    ctx = extract_context(data)
    assert ctx["dos_is_spin_polarized"] is True
    assert len(ctx["dos_chart_data"]) == 3
    assert ctx["dos_chart_data"][0]["dos_up"] == 1.0
    assert ctx["dos_chart_data"][0]["dos_down"] == -0.5  # Negated for plotting


def test_extract_context_dos_spin_polarized_mismatch():
    """Test extract_context with spin-polarized DOS array length mismatch."""
    data = {
        "run": [
            {
                "calculation": [
                    {
                        "dos_electronic": [
                            {
                                "energies": [1e-19, 2e-19],
                                "energy_fermi": 1e-19,
                                "spin_polarized": True,
                                "total": [
                                    {"value": [1.0]},  # mismatch
                                    {"value": [0.5, 1.5]},
                                ],
                            }
                        ]
                    }
                ]
            }
        ]
    }
    ctx = extract_context(data)
    assert len(ctx["dos_chart_data"]) == 0


def test_extract_context_dos_non_spin_polarized():
    """Test extract_context with non-spin-polarized DOS."""
    data = {
        "run": [
            {
                "calculation": [
                    {
                        "dos_electronic": [
                            {
                                "energies": [1e-19, 2e-19],
                                "energy_fermi": 1e-19,
                                "spin_polarized": False,
                                "total": [{"value": [4.0, 5.0]}],
                            }
                        ]
                    }
                ]
            }
        ]
    }
    ctx = extract_context(data)
    assert ctx["dos_is_spin_polarized"] is False
    assert len(ctx["dos_chart_data"]) == 2
    assert ctx["dos_chart_data"][0]["dos"] == 4.0


def test_extract_context_dos_non_spin_mismatch():
    """Test extract_context with non-spin-polarized DOS length mismatch."""
    data = {
        "run": [
            {
                "calculation": [
                    {
                        "dos_electronic": [
                            {
                                "energies": [1e-19, 2e-19],
                                "energy_fermi": 1e-19,
                                "spin_polarized": False,
                                "total": [{"value": [4.0]}],  # mismatch
                            }
                        ]
                    }
                ]
            }
        ]
    }
    ctx = extract_context(data)
    assert len(ctx["dos_chart_data"]) == 0


def test_extract_context_dos_exception(monkeypatch):
    """Test extract_context gracefully handles exceptions in DOS block."""
    data = {
        "run": [
            {
                "calculation": [
                    {
                        "dos_electronic": [
                            {"energies": [1.0]}  # triggers numpy error if not array-like j
                        ]
                    }
                ]
            }
        ]
    }
    ctx = extract_context(data)
    assert ctx["dos_chart_data"] == []


def test_add_row_branches():
    """Test _add_row edge conditions."""
    rows = []
    _add_row(rows, "Empty", None)
    _add_row(rows, "EmptyStr", "")
    _add_row(rows, "EmptyList", [])
    _add_row(rows, "Unavail", "unavailable")
    _add_row(rows, "UnavailPad", "  unavailable  ")
    assert len(rows) == 0

    _add_row(rows, "WithUnit", "10", unit="eV")
    assert rows[0] == "    | WithUnit | **10** | eV |"

    _add_row(rows, "WithoutBold", "val", bold_value=False)
    assert rows[1] == "    | WithoutBold | val |"


def test_generate_material_composition_table():
    """Test _generate_material_composition_table empty and populated."""
    assert _generate_material_composition_table({}) == ""

    ctx = {
        "t_original_data": {
            "chemical_formula_iupac": "Si",
            "chemical_formula_reduced": "Si",
            "label": "Silicon",
            "elements": ["Si"],
            "n_atoms": 2,
            "dimensionality": "3D",
        }
    }
    md = _generate_material_composition_table(ctx)
    assert "Material Composition - Silicon" in md
    assert "Number of elements" in md


def test_generate_lattice_table():
    """Test _generate_lattice_table empty, partial, and full."""
    assert _generate_lattice_table({}, "original_cell", "orig") == ""

    # Constants only
    ctx = {"cell": {"a": 5e-10, "b": 5e-10, "c": 5e-10}}
    md_const = _generate_lattice_table(ctx, "cell", "TestCell")
    assert "Lattice constant" in md_const
    assert "Lattice angles" not in md_const

    # Angles only
    ctx_angles = {"cell": {"alpha": 1.5708, "beta": 1.5708, "gamma": 1.5708}}
    md_angles = _generate_lattice_table(ctx_angles, "cell", "TestCell")
    assert "Lattice angles" in md_angles

    # Quantities only
    ctx_quant = {"cell": {"volume": 1e-28}}
    md_quant = _generate_lattice_table(ctx_quant, "cell", "TestCell")
    assert "Cell quantities" in md_quant


def test_generate_symmetry_table():
    """Test _generate_symmetry_table empty and populated."""
    assert _generate_symmetry_table({}) == ""
    assert _generate_symmetry_table({"t_cell_data_sym": {}}) == ""

    ctx = {
        "t_cell_data": {"label": "Primitive"},
        "t_cell_data_sym": {
            "crystal_system": "Cubic",
            "space_group_symbol": "Fm-3m",
            "space_group_number": 225,
        },
    }
    md = _generate_symmetry_table(ctx)
    assert "Symmetry (Primitive)" in md
    assert "Cubic" in md


def test_generate_kpoints_table():
    """Test _generate_kpoints_table empty and populated."""
    assert _generate_kpoints_table({}) == ""
    assert _generate_kpoints_table({"k_mesh": {}}) == ""

    ctx = {"k_mesh": {"dimensionality": 3, "sampling_method": "Monkhorst-Pack", "n_points": 64}}
    md = _generate_kpoints_table(ctx)
    assert "K points information" in md
    assert "Monkhorst-Pack" in md


def test_generate_metadata_table():
    """Test _generate_metadata_table empty and populated."""
    assert _generate_metadata_table({}) == ""

    ctx = {
        "metadata": {"entry_name": "MyEntry", "mainfile": "/path/to/vasprun.xml"},
        "method": {"method_name": "DFT", "workflow_name": "SinglePoint"},
        "simulation": {"program_name": "VASP", "program_version": "5.4.4 (opt)"},
        "sim_first_nested_data": {
            "basis_set_type": "plane waves",
            "xc_functional_names": ["PBE", "GGA"],
        },
        "sim_second_nested_data": {"basis_set": "Standard"},
    }
    md = _generate_metadata_table(ctx)
    assert "Calculation Metadata" in md
    assert "vasprun.xml" in md
    assert "PBE, GGA" in md
    assert "5.4.4" in md


def test_generate_final_energies_table():
    """Test _generate_final_energies_table empty and with custom extra keys."""
    assert _generate_final_energies_table({}) == ""

    ctx = {
        "final_energies_ev": {
            "total": -120.0,
            "band_gap": 1.5,
            "custom_energy_x": -10.0,  # Non-standard key branch
        }
    }
    md = _generate_final_energies_table(ctx)
    assert "Final Calculation Energies" in md
    assert "Total" in md
    assert "Custom Energy X" in md


def test_generate_scf_energies_table():
    """Test _generate_scf_energies_table empty and with NaNs."""
    assert _generate_scf_energies_table({}) == ""

    ctx = {"scf_table_data": [{"step": 1, "total_ev": -100.0, "free_ev": float("nan"), "total_t0_ev": None}]}
    md = _generate_scf_energies_table(ctx)
    assert "SCF Iteration Energies" in md
    assert "N/A" in md


def test_generate_charts_html():
    """Test _generate_scf_chart_html and _generate_dos_chart_html empty and populated."""
    assert _generate_scf_chart_html({}) == ""
    assert _generate_dos_chart_html({}) == ""

    # SCF chart
    ctx_scf = {"scf_table_data": [{"step": 1, "total_ev": -100.0, "free_ev": -100.1, "total_t0_ev": -100.0}]}
    html_scf = _generate_scf_chart_html(ctx_scf)
    assert "scf_chart_div" in html_scf

    # DOS chart - non-spin-polarized
    ctx_dos_non_spin = {
        "dos_chart_data": [{"energy_ev": 0.1, "dos": 2.5}],
        "dos_is_spin_polarized": False,
    }
    html_dos = _generate_dos_chart_html(ctx_dos_non_spin)
    assert "dos_chart_div" in html_dos
    assert "isSpinPolarized = false" in html_dos

    # DOS chart - spin-polarized
    ctx_dos_spin = {
        "dos_chart_data": [{"energy_ev": 0.1, "dos_up": 2.5, "dos_down": -2.5}],
        "dos_is_spin_polarized": True,
    }
    html_dos_spin = _generate_dos_chart_html(ctx_dos_spin)
    assert "isSpinPolarized = true" in html_dos_spin
    assert "Spin Down" in html_dos_spin


def test_generate_markdown_full():
    """Test generate_markdown creates full document."""
    ctx = {
        "metadata": {"entry_name": "Full Test"},
        "t_original_data": {"chemical_formula_iupac": "Si", "elements": ["Si"]},
    }
    md = generate_markdown(ctx)
    assert "# __Full Test__" in md
    assert "Structural information" in md


def test_save_report_write_error(tmp_path, monkeypatch):
    """Test save_report logs error on write failure."""

    def mock_open(*args, **kwargs):
        raise OSError("Disk write error")

    monkeypatch.setattr("builtins.open", mock_open)
    # Should not raise
    save_report("content", tmp_path / "fair_parsed_test.json", tmp_path / "out")


def test_run_summarization_error_paths(tmp_path):
    """Test run_summarization data load failure, extract context error, and markdown generation error."""
    out_dir = tmp_path / "out"
    out_dir.mkdir()

    # Load failure
    bad_file = tmp_path / "bad.json"
    bad_file.write_text("invalid", encoding="utf-8")
    run_summarization(bad_file, out_dir)
    assert not (out_dir / "fair_summarized_bad.md").exists()

    # Context extraction failure
    good_file = tmp_path / "fair_parsed_good.json"
    good_file.write_text(json.dumps({"test": "ok"}), encoding="utf-8")
    with patch("fairtool.summarize.extract_context", side_effect=RuntimeError("Extraction failed")):
        run_summarization(good_file, out_dir)
        assert not (out_dir / "fair_summarized_good.md").exists()

    # Markdown generation failure
    with patch("fairtool.summarize.generate_markdown", side_effect=RuntimeError("MD failed")):
        run_summarization(good_file, out_dir)
        assert not (out_dir / "fair_summarized_good.md").exists()
