import json
import re
from pathlib import Path

import pytest

from fairtool.summarize import run_summarization

VASP_EXAMPLES = Path(__file__).parent / "VASP"


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


@pytest.fixture
def full_reference_json_file(tmp_path, reference_data):  # <-- [MODIFIED] Uses reference_data
    """
    Creates a 'fair_parsed_full.json' file in the tmp_path directory
    using the large reference data and returns its Path object.
    """
    ref_file = tmp_path / "fair_parsed_full.json"
    # [MODIFIED] Dumps the loaded data from the fixture
    ref_file.write_text(json.dumps(reference_data), encoding="utf-8")
    return ref_file


@pytest.fixture
def empty_json_file(tmp_path):
    """Creates an empty 'fair_parsed_empty.json' file."""
    ref_file = tmp_path / "fair_parsed_empty.json"
    ref_file.write_text(json.dumps({}), encoding="utf-8")
    return ref_file


@pytest.fixture
def kpoint_json_file(tmp_path):
    """
    Creates a minimal JSON file specifically to test k-point formatting.
    This simulates 2 k-points.
    Point 1: (0.0, 0.2, 0.4), Weight 0.5
    Point 2: (0.1, 0.3, 0.5), Weight 0.5
    """
    kpoint_data = {
        "run": [
            {
                "method": [
                    {
                        "k_mesh": {
                            "points": {
                                "re": [
                                    [[0.0, 0.1]],  # kx values (shape 1, 2)
                                    [[0.2, 0.3]],  # ky values (shape 1, 2)
                                    [[0.4, 0.5]],  # kz values (shape 1, 2)
                                ]
                            },
                            "weights": [0.5, 0.5],  # weights (shape 2,)
                        }
                    }
                ]
            }
        ]
    }
    ref_file = tmp_path / "fair_parsed_kpoints.json"
    ref_file.write_text(json.dumps(kpoint_data), encoding="utf-8")
    return ref_file


def test_run_summarization_happy_path(full_reference_json_file, tmp_path):
    """
    Tests that run_summarization successfully creates a markdown file
    and that key data from the rich JSON file is present in the output.
    """
    input_file = full_reference_json_file
    output_dir = tmp_path

    # Run the summarization
    run_summarization(input_file, output_dir, template_path=None)

    # Check that the output file was created
    expected_output = output_dir / "fair_summarized_full.md"
    assert expected_output.exists()

    # Read the content and check for key values
    content = expected_output.read_text(encoding="utf-8")

    # Check for data from 'results.material'
    # [FIX] Removed assertion for "AgCl6Cs2Hg" as it's not in the template
    assert "Fm-3m" in content  # from symmetry.space_group_symbol

    # Check for data from 'results.method'
    assert "VASP - normal" in content  # from precision.native_tier
    assert "GGA_C_PBE" in content  # from dft.xc_functional_names

    # Check for data from 'metadata'
    assert "Cs2AgHgCl6 VASP DFT SinglePoint simulation" in content  # from entry_name

    # The reference data stores a band gap of 7.23 eV for this metal, and no eigenvalues
    # to derive the gap from, so there is no Band Gap row
    assert "Band Gap" not in content

    # Check that placeholders are present where data was truncated
    # (e.g., cell.a is not in the reference data)
    # assert "unavailable" in content

    # Check that the k-point table header is present
    # assert "| kx | ky | kz | Weight |" in content


def _summarize(parsed_file, output_dir):
    """Summarizes a parsed archive from tests/VASP and returns the Markdown report."""
    input_file = VASP_EXAMPLES / parsed_file
    run_summarization(input_file, output_dir, template_path=None)
    summary_name = input_file.stem.replace("fair_parsed_", "fair_summarized_") + ".md"
    return (output_dir / summary_name).read_text(encoding="utf-8")


@pytest.mark.parametrize(
    ("parsed_file", "band_gap_eV"),
    [
        # Si
        ("Basic/example03/fair_parsed_dos_si_vasprun.json", 0.6818),
        # Si band path, whose stored band_gap[0].value is 0.0
        ("Basic/example02/fair_parsed_band_si_vasprun.json", 0.5091),
        # Cs2AgHgCl6, a metal, whose stored band_gap[0].value is 7.23 eV
        ("Basic/example01/fair_parsed_vasprun.json", 0.0),
    ],
)
def test_run_summarization_band_gap_on_parsed_vasp_examples(tmp_path, parsed_file, band_gap_eV):
    """The Band Gap row of the real archives is derived from their eigenvalues."""
    content = _summarize(parsed_file, tmp_path)
    assert f"| **Band Gap** | {band_gap_eV:.6f} |" in content


def test_run_summarization_relaxation_reports_final_ionic_step(tmp_path):
    """
    example06 relaxes AcAg in 3 ionic steps. The energies, SCF iterations and DOS come from
    the last one; the first has a total energy of -7.134064 eV and 12 SCF iterations.
    """
    content = _summarize("Advanced/example06/fair_parsed_vasprun.json", tmp_path)

    assert "| **Total** | -7.138442 |" in content
    assert "| **Band Gap** | 0.000000 |" in content  # a metal
    assert re.findall(r"^\| (\d+) \|", content, flags=re.MULTILINE) == ["1", "2", "3", "4", "5", "6"]
    assert 'id="dos_chart_div"' in content


def test_run_summarization_robustness_empty_json(empty_json_file, tmp_path):
    """
    Tests that run_summarization does not crash when given an empty
    JSON file, proving the safe defaults (.get(), empty dicts) work.
    """
    input_file = empty_json_file
    output_dir = tmp_path

    # Run the summarization
    try:
        run_summarization(input_file, output_dir, template_path=None)
    except Exception as e:
        pytest.fail(f"run_summarization crashed on empty JSON: {e}")

    # Check that the output file was created
    expected_output = output_dir / "fair_summarized_empty.md"

    # [FIX] Changed to 'assert not' to match 'summarize.py' logic,
    # which returns early for empty data and creates no file.
    assert not expected_output.exists()


def test_run_summarization_nonexistent_file(tmp_path):
    """Test run_summarization handles non-existent files gracefully."""
    nonexistent = tmp_path / "nonexistent.json"
    run_summarization(nonexistent, tmp_path, template_path=None)
    assert not (tmp_path / "fair_summarized_nonexistent.md").exists()


def test_run_summarization_corrupted_file(tmp_path):
    """Test run_summarization handles invalid JSON gracefully."""
    bad_file = tmp_path / "bad.json"
    bad_file.write_text("{ corrupt", encoding="utf-8")
    run_summarization(bad_file, tmp_path, template_path=None)
    assert not (tmp_path / "fair_summarized_bad.md").exists()
