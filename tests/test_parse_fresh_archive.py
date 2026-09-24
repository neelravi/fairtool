"""
Runs the real `nomad parse` on a VASP example, as `fair parse` does, and checks the archive it writes.

The other parse tests fake NOMAD's output, and the archives committed under tests/VASP were parsed
with an older NOMAD setup, so neither shows what the installed NOMAD fills in.
"""

import json
import os
import sys
from pathlib import Path

from fairtool.parse import run_parser
from fairtool.summarize import run_summarization

VASP_EXAMPLES = Path(__file__).parent / "VASP"


def test_fresh_parse_fills_material_and_summary_tables(tmp_path, monkeypatch):
    """
    NOMAD builds results.material from the system its system normalizer marks as representative.
    Without that normalizer (nomad-normalizer-plugin-system), results.material comes out empty: no
    formula and no topology. The summary then lacks the Material Composition and Lattice tables,
    and the formula in its title.
    """
    # run_parser runs `nomad` from PATH; use the one installed next to this Python
    monkeypatch.setenv("PATH", f"{Path(sys.executable).parent}{os.pathsep}{os.environ.get('PATH', '')}")

    run_parser(VASP_EXAMPLES / "Basic" / "example03" / "dos_si_vasprun.xml", tmp_path, force=True)
    parsed_file = tmp_path / "fair_parsed_dos_si_vasprun.json"
    archive = json.loads(parsed_file.read_text(encoding="utf-8"))

    material = archive["results"]["material"]
    assert material.get("chemical_formula_reduced") == "Si"
    assert material.get("structural_type") == "bulk"
    assert {"original", "conventional cell"} <= {entry.get("label") for entry in material.get("topology", [])}
    assert archive["metadata"]["entry_name"] == "Si VASP DFT SinglePoint simulation"

    run_summarization(parsed_file, tmp_path)
    summary = (tmp_path / "fair_summarized_dos_si_vasprun.md").read_text(encoding="utf-8")
    assert "# __Si VASP DFT SinglePoint simulation__" in summary
    assert "- ### Material Composition - original" in summary
    assert "- ### Lattice (original)" in summary
    assert "- ### Lattice (conventional cell)" in summary
