import copy
import json
from pathlib import Path

import pandas as pd
import pytest
import yaml

from fairtool.analyze import perform_single_file_analysis, run_analysis
from fairtool.parse import ELEMENTARY_CHARGE_VALUE as EV

VASP_EXAMPLES = Path(__file__).parent / "VASP"


@pytest.fixture
def sample_parsed_data():
    """
    A `fair parse` archive of bulk Si, trimmed to what the analysis reads.

    NOMAD keeps the results in the legacy `run` section, in joules. The numbers come from
    tests/VASP/Basic/example03 (dos_si_vasprun.xml).
    """
    return {
        "run": [
            {
                "method": [{"scf": {"threshold_energy_change": 1.602176634e-23}}],  # EDIFF = 1e-4 eV
                "calculation": [
                    {
                        "energy": {"total": {"value": -1.735592429774028e-18}},
                        # The last three SCF iterations
                        "scf_iteration": [
                            {"energy": {"free": {"value": -1.7355713611512908e-18}}},
                            {"energy": {"free": {"value": -1.735589001116031e-18}}},
                            {"energy": {"free": {"value": -1.735592429774028e-18}}},
                        ],
                        # Top valence and bottom conduction band, shaped (spin channel, k-point, band),
                        # at the k-points of the valence band maximum and the conduction band minimum
                        "eigenvalues": [
                            {
                                "energies": [
                                    [
                                        [8.384190325721999e-19, 1.24525974524382e-18],
                                        [4.3095347101332e-19, 9.476554354783198e-19],
                                    ]
                                ],
                                "occupations": [[[1.0, 0.0], [1.0, 0.0]]],
                            }
                        ],
                    }
                ],
            }
        ]
    }


def _final_calculation(data):
    return data["run"][0]["calculation"][-1]


def test_perform_single_file_analysis_success(sample_parsed_data):
    """Test extracting energy, band gap, and convergence from the run section, in eV."""
    result = perform_single_file_analysis(sample_parsed_data, {}, "calc_01")
    assert result["identifier"] == "calc_01"
    assert result["total_energy_eV"] == pytest.approx(-10.8327159)
    assert result["band_gap_eV"] == pytest.approx(0.6818)
    assert result["converged"] is True


def test_perform_single_file_analysis_empty_data():
    """Test gracefully handling empty dictionary without errors."""
    result = perform_single_file_analysis({}, {}, "empty_calc")
    assert result["identifier"] == "empty_calc"
    assert result["total_energy_eV"] is None
    assert result["band_gap_eV"] is None
    assert result["converged"] is None


@pytest.mark.parametrize(
    "malformed",
    [
        {"run": "not-a-list"},
        {"run": [{"calculation": "not-a-list", "method": "not-a-list"}]},
        # Non-numeric values, and eigenvalues without the (spin channel, k-point, band) shape
        {
            "run": [
                {
                    "method": [{"scf": {"threshold_energy_change": "n/a"}}],
                    "calculation": [
                        {
                            "energy": {"total": {"value": "n/a"}},
                            "eigenvalues": [{"energies": [1.0], "occupations": [1.0]}],
                            "scf_iteration": [{"energy": {"free": {"value": "n/a"}}}] * 2,
                        }
                    ],
                }
            ]
        },
        # Unexpected containers inside an otherwise usable calculation
        {
            "run": [
                {
                    "method": [{"scf": {"threshold_energy_change": 1e-23}}],
                    "calculation": [
                        {
                            "energy": "not-a-dict",
                            "eigenvalues": "not-a-list",
                            "scf_iteration": [{"energy": "not-a-dict"}, {"energy": {"free": {"value": -1e-18}}}],
                        }
                    ],
                }
            ]
        },
    ],
)
def test_perform_single_file_analysis_malformed_structures(malformed):
    """Test extracting from unexpected non-dict, non-list or non-numeric values."""
    result = perform_single_file_analysis(malformed, {}, "malformed_calc")
    assert result["total_energy_eV"] is None
    assert result["band_gap_eV"] is None
    assert result["converged"] is None


def test_perform_single_file_analysis_uses_final_calculation(sample_parsed_data):
    """For a relaxation, report the last ionic step rather than the first."""
    first_step = copy.deepcopy(_final_calculation(sample_parsed_data))
    first_step["energy"]["total"]["value"] = -9.0 * EV
    sample_parsed_data["run"][0]["calculation"].insert(0, first_step)

    result = perform_single_file_analysis(sample_parsed_data, {}, "relaxation")
    assert result["total_energy_eV"] == pytest.approx(-10.8327159)


def test_band_gap_is_zero_for_a_metal(sample_parsed_data):
    """
    A band crossing the Fermi level makes a metal, even when the k-mesh leaves a gap between
    the highest occupied and lowest unoccupied state (as for Cs2AgHgCl6 in example01).
    """
    eigenvalues = _final_calculation(sample_parsed_data)["eigenvalues"][0]
    # The second band is filled at the first k-point and empty at the second
    eigenvalues["energies"] = [[[3.0 * EV, 4.0 * EV], [3.5 * EV, 4.1 * EV]]]
    eigenvalues["occupations"] = [[[1.0, 1.0], [1.0, 0.0]]]

    assert perform_single_file_analysis(sample_parsed_data, {}, "metal")["band_gap_eV"] == 0.0


def test_band_gap_spans_both_spin_channels(sample_parsed_data):
    """The gap runs from the highest occupied to the lowest unoccupied state of either spin."""
    eigenvalues = _final_calculation(sample_parsed_data)["eigenvalues"][0]
    eigenvalues["energies"] = [
        [[1.5 * EV, 3.0 * EV], [1.0 * EV, 3.2 * EV]],  # spin up: 1.5 eV gap
        [[1.2 * EV, 2.5 * EV], [0.9 * EV, 2.8 * EV]],  # spin down: 1.3 eV gap
    ]
    eigenvalues["occupations"] = [[[1.0, 0.0], [1.0, 0.0]]] * 2

    # Spin-up valence band maximum (1.5 eV) to spin-down conduction band minimum (2.5 eV)
    assert perform_single_file_analysis(sample_parsed_data, {}, "magnetic")["band_gap_eV"] == pytest.approx(1.0)


def test_band_gap_from_band_structure_segments(sample_parsed_data):
    """A band-structure run keeps its eigenvalues in the segments of the band path."""
    calculation = _final_calculation(sample_parsed_data)
    eigenvalues = calculation.pop("eigenvalues")[0]
    # One single-k-point segment per k-point
    calculation["band_structure_electronic"] = [
        {
            "segment": [
                {"energies": [[energies]], "occupations": [[occupations]]}
                for energies, occupations in zip(eigenvalues["energies"][0], eigenvalues["occupations"][0])
            ]
        }
    ]

    assert perform_single_file_analysis(sample_parsed_data, {}, "bands")["band_gap_eV"] == pytest.approx(0.6818)


@pytest.mark.parametrize(
    ("free_energies_eV", "converged"),
    [
        ([-10.0, -10.0002, -10.00021], True),  # last change 1e-5 eV is within EDIFF = 1e-4 eV
        ([-10.0, -10.0002], False),  # 2e-4 eV is not
        ([-10.0, -10.0002, -10.0002], False),  # like NOMAD, skip a change of zero (example02's band run)
        ([-10.0, -10.0, -10.0], True),  # the energy never changed
        ([-10.0], None),  # a single iteration has no change to judge
    ],
)
def test_scf_convergence(sample_parsed_data, free_energies_eV, converged):
    """The last non-zero change in free energy between SCF iterations must be within the threshold."""
    _final_calculation(sample_parsed_data)["scf_iteration"] = [
        {"energy": {"free": {"value": energy * EV}}} for energy in free_energies_eV
    ]

    assert perform_single_file_analysis(sample_parsed_data, {}, "scf")["converged"] is converged


def test_scf_convergence_compares_the_free_energy(sample_parsed_data):
    """
    VASP applies EDIFF to the free energy. With smearing, the energy without entropy can
    change by more (as in the last ionic step of example06), which must not count.
    """
    for step, iteration in enumerate(_final_calculation(sample_parsed_data)["scf_iteration"]):
        iteration["energy"]["total"] = {"value": (-10.0 - 1e-3 * step) * EV}  # 1 meV per step

    assert perform_single_file_analysis(sample_parsed_data, {}, "smeared")["converged"] is True


def test_perform_single_file_analysis_without_total_energy_or_scf_threshold(sample_parsed_data):
    """A GW run (example04) records eigenvalues but no total energy or SCF threshold."""
    del _final_calculation(sample_parsed_data)["energy"]["total"]
    del sample_parsed_data["run"][0]["method"][0]["scf"]

    result = perform_single_file_analysis(sample_parsed_data, {}, "gw")
    assert result["total_energy_eV"] is None
    assert result["band_gap_eV"] == pytest.approx(0.6818)
    assert result["converged"] is None


@pytest.mark.parametrize(
    ("parsed_file", "total_energy_eV", "band_gap_eV", "converged"),
    [
        # Si
        ("Basic/example03/fair_parsed_dos_si_vasprun.json", -10.8327, 0.6818, True),
        # Si band path (non-self-consistent, EDIFF = 0, which NOMAD also reports as not converged)
        ("Basic/example02/fair_parsed_band_si_vasprun.json", -12.0516, 0.5091, False),
        # Cs2AgHgCl6, a metal: bands cross the Fermi level
        ("Basic/example01/fair_parsed_vasprun.json", -29.9598, 0.0, True),
        # Si GW: no total energy or SCF threshold
        ("Advanced/example04/fair_parsed_vasprun.json", None, 1.7206, None),
    ],
)
def test_perform_single_file_analysis_on_parsed_vasp_examples(parsed_file, total_energy_eV, band_gap_eV, converged):
    """Real archives written by `fair parse` for the VASP examples give sensible values."""
    data = json.loads((VASP_EXAMPLES / parsed_file).read_text(encoding="utf-8"))

    result = perform_single_file_analysis(data, {}, Path(parsed_file).stem)
    assert result["total_energy_eV"] == pytest.approx(total_energy_eV, abs=1e-4)
    assert result["band_gap_eV"] == pytest.approx(band_gap_eV, abs=1e-4)
    assert result["converged"] is converged


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
    assert data["total_energy_eV"] == pytest.approx(-10.8327159)
    assert data["band_gap_eV"] == pytest.approx(0.6818)
    assert data["converged"] is True

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
    (calc_dir / "fair_parsed_calc1.json").write_text(json.dumps(sample_parsed_data), encoding="utf-8")
    (calc_dir / "fair_parsed_calc2.json").write_text(json.dumps(sample_parsed_data), encoding="utf-8")

    out_dir = tmp_path / "output"
    out_dir.mkdir()

    run_analysis(calc_dir, out_dir, None)

    assert (out_dir / "fair_parsed_calc1_analysis.yaml").exists()
    assert (out_dir / "fair_parsed_calc2_analysis.yaml").exists()

    csv_file = out_dir / "analysis_summary.csv"
    assert csv_file.exists()
    df = pd.read_csv(csv_file)
    assert len(df) == 2


def test_run_analysis_directory_finds_fair_parse_output(tmp_path, sample_parsed_data):
    """Regression: a directory search finds the fair_parsed_<name>.json files that `fair parse` writes."""
    calc_dir = tmp_path / "calc"
    calc_dir.mkdir()
    # What `fair parse calc` leaves next to calc/dos_si_vasprun.xml
    (calc_dir / "fair_parsed_dos_si_vasprun.json").write_text(json.dumps(sample_parsed_data), encoding="utf-8")
    (calc_dir / "fair-structure.json").write_text("{}", encoding="utf-8")
    out_dir = tmp_path / "output"
    out_dir.mkdir()

    run_analysis(calc_dir, out_dir, None)

    csv_file = out_dir / "analysis_summary.csv"
    assert csv_file.exists()
    # Only the parsed calculation is analyzed, not the structure JSON beside it
    assert pd.read_csv(csv_file)["identifier"].tolist() == ["fair_parsed_dos_si_vasprun"]


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
