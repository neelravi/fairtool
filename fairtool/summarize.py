# fairtool/summarize.py

"""
Handles the generation of human-readable summaries from parsed VASP data.

This refactored version separates concerns into:
1.  Loading data (load_data)
2.  Extracting and processing data into a context dict (extract_context)
3.  Generating Markdown from the context (generate_markdown)
4.  Saving the final report (save_report)

The main 'run_summarization' function orchestrates this flow.
"""

import json
import logging
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pint

# --- Setup ---
u = pint.UnitRegistry()
log = logging.getLogger("fairtool")
ELEMENTARY_CHARGE_VALUE = 1.602176634e-19  # Elementary charge in Coulombs
J_PER_EV = ELEMENTARY_CHARGE_VALUE  # Alias for clarity

# --- Original Helper Functions (Unchanged) ---
# These functions are well-structured and perform specific tasks.


def _extract_energy_lists(scf_iterations: List[dict], energy_key: str) -> Tuple[List[float], List[float]]:
    """
    Helper to safely extract energy lists from scf_iterations.

    Args:
        scf_iterations: The list of scf_iteration blocks.
        energy_key: The key of the energy to extract (e.g., "total", "xc").

    Returns:
        A tuple of (energies_in_eV, energies_in_J).
    """
    energies_J = []
    energies_eV = []
    for iteration in scf_iterations:
        value = iteration.get("energy", {}).get(energy_key, {}).get("value")

        if value is not None:
            energies_J.append(value)
            try:
                energies_eV.append(value / J_PER_EV)
            except (ZeroDivisionError, TypeError):
                energies_eV.append(float("nan"))
        else:
            energies_J.append(float("nan"))
            energies_eV.append(float("nan"))
    return energies_eV, energies_J


def _scalar(x):
    """Unwrap 1-item list/tuple -> value; otherwise return as-is."""
    if isinstance(x, (list, tuple)) and len(x) == 1:
        return x[0]
    return x


def _as_qty(v, unit):
    """Attach a unit if v is numeric; return None for missing/sentinel."""
    v = _scalar(v)
    if v is None or v == "unavailable":
        return None
    try:
        return float(v) * unit
    except (TypeError, ValueError):
        return None


FIELD_UNITS = {
    "a": (u.m, u.angstrom, "Å", ".3f"),
    "b": (u.m, u.angstrom, "Å", ".3f"),
    "c": (u.m, u.angstrom, "Å", ".3f"),
    "alpha": (u.radian, u.degree, "°", ".0f"),
    "beta": (u.radian, u.degree, "°", ".0f"),
    "gamma": (u.radian, u.degree, "°", ".0f"),
    "volume": (u.m**3, u.angstrom**3, "Å^3", ".3f"),
    "atomic_density": (1 / u.m**3, 1 / u.angstrom**3, "Å^-3", ".3f"),
    "mass_density": (u.kg / u.m**3, u.kg / u.angstrom**3, "kg/Å^3", ".3e"),
}


def _convert_field(value, field, default=None, return_numeric=False):
    """
    Convert a raw value for a known field to its display unit and format.
    """
    spec = FIELD_UNITS.get(field)
    if not spec:
        raise KeyError(f"Unknown field '{field}'. Known: {sorted(FIELD_UNITS)}")
    from_u, to_u, symbol, fmt = spec
    q = _as_qty(value, from_u)
    if q is None:
        return default
    num = q.to(to_u).magnitude
    return num if return_numeric else f"{format(num, fmt)} {symbol}"


def _strip_parens(s: object, default: str = "unavailable") -> str:
    """Return the string with any parenthetical "( ... )" removed."""
    if s is None:
        return default
    s = str(s)
    if s == "":
        return default
    cleaned = re.sub(r"\s*\(.*?\)", "", s)
    return cleaned.strip() or default


def _format_field_numeric(value, field, default=None):
    """Return a string formatted according to FIELD_UNITS for the given field."""
    try:
        num = _convert_field(value, field, default=None, return_numeric=True)
    except KeyError:
        return default
    if num is None:
        return default
    fmt = FIELD_UNITS.get(field, (None, None, None, ".3f"))[3]
    try:
        return format(num, fmt)
    except Exception:
        return default


# --- New Modular Functions ---


def load_data(input_path: Path) -> Optional[Dict[str, Any]]:
    """Loads and parses the JSON data file."""
    try:
        log.info(f"Loading parsed data from: {input_path}")
        with open(input_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        log.info("Successfully loaded JSON data.")
        if not isinstance(data, dict) or not data:
            log.warning("No valid data loaded.")
            return None
        return data
    except Exception as e:
        log.error(f"Failed to load or parse JSON: {e}")
        return None


def extract_context(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extracts all necessary data from the raw JSON dict into a flat context.

    This context is used by the Markdown generator.
    """
    context = {}

    # --- Safe Data Extraction ---
    run_list = data.get("run", [])
    run = run_list[0] if run_list else {}
    context["metadata"] = data.get("metadata", {})
    results = data.get("results", {})

    method = results.get("method", {})
    simulation = method.get("simulation", {})
    material = results.get("material", {})
    topology = material.get("topology", [])

    # Safely get sim data
    nested_dicts = [v for v in simulation.values() if isinstance(v, dict)]
    context["sim_first_nested_data"] = nested_dicts[0] if len(nested_dicts) > 0 else {}
    context["sim_second_nested_data"] = nested_dicts[1] if len(nested_dicts) > 1 else {}

    # Safely get topology data
    t_original_data = {}
    t_cell_data = {}
    for obj in topology:
        if not isinstance(obj, dict):
            continue
        label = (obj.get("label") or "").strip().lower()
        if label == "original":
            t_original_data = obj
        elif label in ("primitive cell", "conventional cell"):
            t_cell_data = obj

    context["t_original_data"] = t_original_data
    context["t_cell_data"] = t_cell_data
    context["original_cell"] = t_original_data.get("cell", {})
    context["cell_type_data"] = t_cell_data.get("cell", {})
    context["t_cell_data_sym"] = t_cell_data.get("symmetry", {})

    # Safely get calculation data
    calculation = run.get("calculation", [])
    calc = calculation[0] if calculation else {}
    scf_iterations = calc.get("scf_iteration", [])

    # Safely get k_mesh data
    runmethod = run.get("method", [])
    k_mesh = runmethod[0].get("k_mesh", {}) if runmethod else {}

    # --- Populate Context ---
    context["method"] = method
    context["simulation"] = simulation
    context["k_mesh"] = k_mesh

    # --- **NEW:** Extract Final Energies (from run.calculation[0].energy) ---
    final_energy_data = calc.get("energy", {})
    final_energies_ev = {}
    for key, value_dict in final_energy_data.items():
        if isinstance(value_dict, dict) and "value" in value_dict:
            value_j = value_dict.get("value")
            if value_j is not None:
                try:
                    final_energies_ev[key] = value_j / J_PER_EV
                except (ZeroDivisionError, TypeError):
                    final_energies_ev[key] = float("nan")
    context["final_energies_ev"] = final_energies_ev

    # --- **NEW:** Extract Band Gap Info ---
    band_gap_list = calc.get("band_gap", [])
    band_gap_data = band_gap_list[0] if band_gap_list else {}
    band_gap_j = band_gap_data.get("value")
    if band_gap_j is not None:
        try:
            # Add band gap in eV to the final_energies_ev dict for convenience
            context["final_energies_ev"]["band_gap"] = band_gap_j / J_PER_EV
        except (ZeroDivisionError, TypeError):
            context["final_energies_ev"]["band_gap"] = float("nan")

    # --- **NEW:** Extract SCF Iteration Energies ---
    log.info("Extracting SCF energy data.")
    total_ev, _ = _extract_energy_lists(scf_iterations, "total")
    free_ev, _ = _extract_energy_lists(scf_iterations, "free")
    total_t0_ev, _ = _extract_energy_lists(scf_iterations, "total_t0")

    scf_table_data = []
    # Use the longest list to determine the number of steps
    n_steps = max(len(total_ev), len(free_ev), len(total_t0_ev))
    for i in range(n_steps):
        scf_table_data.append(
            {
                "step": i + 1,
                "total_ev": total_ev[i] if i < len(total_ev) else None,
                "free_ev": free_ev[i] if i < len(free_ev) else None,
                "total_t0_ev": total_t0_ev[i] if i < len(total_t0_ev) else None,
            }
        )
    context["scf_table_data"] = scf_table_data

    # --- **NEW:** Extract DOS Data ---
    log.info("Extracting DOS data for charting.")
    dos_chart_data = []
    is_spin_polarized = False
    try:
        dos_electronic = calc.get("dos_electronic", [])
        if dos_electronic:
            dos_data = dos_electronic[0]
            energies_j = np.array(dos_data.get("energies", []))
            fermi_j = dos_data.get("energy_fermi")
            dos_total = dos_data.get("total", [])  # List of value objects

            if energies_j.any() and fermi_j is not None and dos_total:
                # Convert energies to eV and shift relative to Fermi
                energies_ev = (energies_j - fermi_j) / J_PER_EV

                is_spin_polarized = dos_data.get("spin_polarized", False)

                if is_spin_polarized and len(dos_total) >= 2:
                    dos_up = np.array(dos_total[0].get("value", []))
                    dos_down = np.array(dos_total[1].get("value", [])) * -1  # Negate for plotting

                    if len(energies_ev) == len(dos_up) == len(dos_down):
                        for e, up, down in zip(energies_ev, dos_up, dos_down):
                            dos_chart_data.append({"energy_ev": e, "dos_up": up, "dos_down": down})
                    else:
                        log.warning("DOS energy and value array lengths mismatch (spin-polarized).")

                elif not is_spin_polarized and len(dos_total) >= 1:
                    dos = np.array(dos_total[0].get("value", []))
                    if len(energies_ev) == len(dos):
                        for e, d in zip(energies_ev, dos):
                            dos_chart_data.append({"energy_ev": e, "dos": d})
                    else:
                        log.warning("DOS energy and value array lengths mismatch (non-spin-polarized).")
            else:
                log.info("No complete DOS data found (missing energies, fermi, or total).")
    except Exception as e:
        log.error(f"Failed to process DOS data: {e}", exc_info=True)

    context["dos_chart_data"] = dos_chart_data
    context["dos_is_spin_polarized"] = is_spin_polarized
    log.info(f"Finished extracting DOS data. Found {len(dos_chart_data)} points.")

    return context


# --- New Markdown Table Generator Functions ---


def _add_row(rows: List[str], label: str, value: Any, unit: str = "", bold_value: bool = True):
    """Helper to add a formatted Markdown row if value is valid."""
    if value is None or value == "" or value == [] or value == "unavailable":
        return  # Skip row

    # Special handling for _strip_parens default
    if isinstance(value, str) and value.strip() == "unavailable":
        return

    value_str = f"**{value}**" if bold_value else str(value)

    if unit:
        rows.append(f"    | {label} | {value_str} | {unit} |")
    else:
        rows.append(f"    | {label} | {value_str} |")


def _generate_material_composition_table(context: Dict[str, Any]) -> str:
    """Generates the Markdown table for Material Composition."""
    t_original_data = context.get("t_original_data", {})
    rows = []

    _add_row(rows, "Chemical formula (IUPAC)", t_original_data.get("chemical_formula_iupac"))
    _add_row(rows, "Chemical formula (Reduced)", t_original_data.get("chemical_formula_reduced"))
    _add_row(rows, "Label", t_original_data.get("label"))

    elements = t_original_data.get("elements")
    _add_row(rows, "Elements", ", ".join(elements) if elements else None)
    if elements:
        _add_row(rows, "Number of elements", len(elements))

    _add_row(rows, "Number of atoms", t_original_data.get("n_atoms"))
    _add_row(rows, "Dimensionality", t_original_data.get("dimensionality"))

    if not rows:
        return ""

    header = [
        f"- ### Material Composition - {t_original_data.get('label', 'Original Material')}\n",
        "    | Property                     | Value                       |",
        "    |------------------------------|-----------------------------|",
    ]
    return "\n".join(header + rows)


def _generate_lattice_table(context: Dict[str, Any], cell_key: str, label_key: str) -> str:
    """Generates the Markdown tables for Lattice properties."""
    cell_data = context.get(cell_key, {})
    if not cell_data:
        return ""

    rows_const = []
    rows_angles = []
    rows_quant = []

    _add_row(rows_const, "a", _format_field_numeric(cell_data.get("a"), "a"), "Angstrom")
    _add_row(rows_const, "b", _format_field_numeric(cell_data.get("b"), "b"), "Angstrom")
    _add_row(rows_const, "c", _format_field_numeric(cell_data.get("c"), "c"), "Angstrom")

    _add_row(rows_angles, "Alpha", _format_field_numeric(cell_data.get("alpha"), "alpha"), "Degrees")
    _add_row(rows_angles, "Beta", _format_field_numeric(cell_data.get("beta"), "beta"), "Degrees")
    _add_row(rows_angles, "Gamma", _format_field_numeric(cell_data.get("gamma"), "gamma"), "Degrees")

    _add_row(rows_quant, "Volume", _format_field_numeric(cell_data.get("volume"), "volume"), "Å³")
    _add_row(
        rows_quant, "Mass density", _format_field_numeric(cell_data.get("mass_density"), "mass_density"), "kg / Å³"
    )
    _add_row(
        rows_quant, "Atomic density", _format_field_numeric(cell_data.get("atomic_density"), "atomic_density"), "Å⁻³"
    )

    if not (rows_const or rows_angles or rows_quant):
        return ""

    table = [f"- ### Lattice ({label_key})\n"]
    if rows_const:
        table.extend(
            [
                "    | Lattice constant | Value     | Units |",
                "    |------------------|-----------|-------|",
            ]
            + rows_const
        )
    if rows_angles:
        table.extend(
            [
                "\n    | Lattice angles    | Value     | Units |",
                "    |------------------|-----------|-------|",
            ]
            + rows_angles
        )
    if rows_quant:
        table.extend(
            [
                "\n    | Cell quantities   | Value     | Units |",
                "    |------------------|-----------|-------|",
            ]
            + rows_quant
        )

    return "\n".join(table)


def _generate_symmetry_table(context: Dict[str, Any]) -> str:
    """Generates the Markdown table for Symmetry properties."""
    t_cell_data_sym = context.get("t_cell_data_sym", {})
    t_cell_data = context.get("t_cell_data", {})
    if not t_cell_data_sym:
        return ""

    rows = []
    _add_row(rows, "Crystal system", t_cell_data_sym.get("crystal_system"))
    _add_row(rows, "Bravais lattice", t_cell_data_sym.get("bravais_lattice"))
    _add_row(rows, "Space group symbol", t_cell_data_sym.get("space_group_symbol"))
    _add_row(rows, "Space group number", t_cell_data_sym.get("space_group_number"))
    _add_row(rows, "Point group", t_cell_data_sym.get("point_group"))
    _add_row(rows, "Hall number", t_cell_data_sym.get("hall_number"))
    _add_row(rows, "Hall symbol", t_cell_data_sym.get("hall_symbol"))
    _add_row(rows, "Prototype name", t_cell_data_sym.get("prototype_name"))
    _add_row(rows, "Prototype label aflow", t_cell_data_sym.get("prototype_label_aflow"))

    if not rows:
        return ""

    label = t_cell_data.get("label", "unavailable")
    header = [
        f"- ### Symmetry ({label})\n",
        "    | Property                       | Value            |",
        "    |---------------------------------|------------------|",
    ]
    return "\n".join(header + rows)


def _generate_kpoints_table(context: Dict[str, Any]) -> str:
    """Generates the Markdown table for K points information."""
    k_mesh = context.get("k_mesh", {})
    if not k_mesh:
        return ""

    rows = []
    _add_row(rows, "Dimensionality", k_mesh.get("dimensionality"))
    _add_row(rows, "Sampling method", k_mesh.get("sampling_method"))
    _add_row(rows, "Number of points", k_mesh.get("n_points"))
    _add_row(rows, "Grid", k_mesh.get("grid"))

    if not rows:
        return ""

    header = [
        "- ### K points information\n",
        "    | Property               | Value |",
        "    |------------------------|--------|",
    ]
    return "\n".join(header + rows)


def _generate_metadata_table(context: Dict[str, Any]) -> str:
    """Generates the Markdown table for Calculation Metadata."""
    metadata = context.get("metadata", {})
    method = context.get("method", {})
    simulation = context.get("simulation", {})
    sim_first = context.get("sim_first_nested_data", {})
    sim_second = context.get("sim_second_nested_data", {})

    rows = []
    _add_row(rows, "**Method name**", method.get("method_name"), bold_value=False)
    _add_row(rows, "**Workflow name**", method.get("workflow_name"), bold_value=False)
    _add_row(rows, "**Program name**", simulation.get("program_name"), bold_value=False)
    _add_row(
        rows, "**Program version**", _strip_parens(simulation.get("program_version"), default=None), bold_value=False
    )
    _add_row(rows, "**Basis set type**", sim_first.get("basis_set_type"), bold_value=False)
    _add_row(rows, "**Core electron treatment**", sim_first.get("core_electron_treatment"), bold_value=False)
    _add_row(rows, "**Jacob's ladder**", sim_first.get("jacobs_ladder"), bold_value=False)

    xc_names = sim_first.get("xc_functional_names")
    _add_row(rows, "**XC functional names**", ", ".join(xc_names) if xc_names else None, bold_value=False)

    _add_row(rows, "**Code-specific tier**", sim_second.get("native_tier"), bold_value=False)
    _add_row(rows, "**Basis set**", sim_second.get("basis_set"), bold_value=False)
    _add_row(rows, "**Entry type**", metadata.get("entry_type"), bold_value=False)
    _add_row(rows, "**Entry name**", metadata.get("entry_name"), bold_value=False)

    mainfile = metadata.get("mainfile")
    _add_row(rows, "**Mainfile**", Path(mainfile).name if mainfile else None, bold_value=False)

    if not rows:
        return ""

    header = [
        "- ### Calculation Metadata\n",
        "    | Property                   | Value                                                      |",
        "    |----------------------------|------------------------------------------------------------|",
    ]
    return "\n".join(header + rows)


def _generate_final_energies_table(context: Dict[str, Any]) -> str:
    """Generates the Markdown table for final energies."""
    final_energies_ev = context.get("final_energies_ev", {})
    if not final_energies_ev:
        return ""

    rows = []
    # Define preferred order and formatting
    key_order = ["total", "free", "total_t0", "fermi", "highest_occupied", "lowest_unoccupied", "band_gap"]

    # Custom labels for clarity
    label_map = {
        "total": "Total",
        "free": "Free",
        "total_t0": "Total (T=0)",
        "fermi": "Fermi Energy",
        "highest_occupied": "Highest Occupied (VBM)",
        "lowest_unoccupied": "Lowest Unoccupied (CBM)",
        "band_gap": "Band Gap",
    }

    processed_keys = set()

    for key in key_order:
        if key in final_energies_ev:
            value = final_energies_ev[key]
            label = label_map.get(key, key.replace("_", " ").title())
            rows.append(f"    | **{label}** | {value:.6f} |")
            processed_keys.add(key)

    # Add any other keys not in the preferred list
    for key, value in final_energies_ev.items():
        if key not in processed_keys:
            label = label_map.get(key, key.replace("_", " ").title())
            rows.append(f"    | {label} | {value:.6f} |")

    table = [
        "- ### Final Calculation Energies\n",
        "    | Energy | Value (eV) |",
        "    |---|---|",
    ]
    table.extend(rows)
    return "\n".join(table)


def _generate_scf_energies_table(context: Dict[str, Any]) -> str:
    """Generates the Markdown table for SCF iteration energies."""
    scf_table_data = context.get("scf_table_data", [])
    if not scf_table_data:
        return ""

    rows = []
    for item in scf_table_data:
        step = item["step"]

        def fmt_val(v):
            if v is None or np.isnan(v):
                return "N/A"
            return f"{v:.5f}"

        total = fmt_val(item["total_ev"])
        free = fmt_val(item["free_ev"])
        total_t0 = fmt_val(item["total_t0_ev"])
        rows.append(f"| {step} | {total} | {free} | {total_t0} |")

    table = [
        "- ### SCF Iteration Energies\n",
        "    | Step | Total Energy (eV) | Free Energy (eV) | Total Energy (T=0) (eV) |",
        "    |:---|---:|---:|---:|",
    ]
    table.extend(rows)
    return "\n".join(table)


def _generate_scf_chart_html(context: Dict[str, Any]) -> str:
    """
    Generates the HTML and JavaScript block for the Google Chart.
    """
    scf_table_data = context.get("scf_table_data", [])
    if not scf_table_data:
        return ""

    # Serialize the Python data to a JSON string
    # This is safe because we converted NaN to None in extract_context
    scf_data_json = json.dumps(scf_table_data)

    # Note: The backticks inside the f-string (for JSON.parse)
    # must be escaped by doubling them (``) if the outer string uses
    # f-strings, but here we use ''' so it's fine.
    # We must be careful with indentation in the JS block.
    html_js_block = f"""
<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
<div id="scf_chart_div" style="width: 100%; height: 500px; margin-bottom: 20px;"></div>
<script type="text/javascript">
  google.charts.load('current', {{'packages':['corechart']}});
  google.charts.setOnLoadCallback(drawChart);

  function drawChart() {{
    // Parse the JSON data passed from Python
    const scfData = JSON.parse('{scf_data_json}');

    var data = new google.visualization.DataTable();
    data.addColumn('number', 'Step');
    data.addColumn('number', 'Total Energy (eV)');
    data.addColumn('number', 'Free Energy (eV)');
    data.addColumn('number', 'Total Energy (T=0) (eV)');

    // Convert the list of objects into an array of arrays
    // Google Charts expects null for missing values, which JSON.parse handles
    const rows = scfData.map(item => [
      item.step, 
      item.total_ev, 
      item.free_ev, 
      item.total_t0_ev
    ]);

    data.addRows(rows);

    var options = {{
      title: '',
      curveType: 'function',
      legend: {{ position: 'bottom' }},
      hAxis: {{
        title: 'SCF Step'
      }},
      vAxis: {{
        title: 'Energy (eV)'
      }},
      // This allows the chart to be responsive
      chartArea: {{'width': '85%', 'height': '75%'}},
    }};

    var chart = new google.visualization.LineChart(document.getElementById('scf_chart_div'));
    chart.draw(data, options);
  }}
</script>
"""
    return html_js_block


def _generate_dos_chart_html(context: Dict[str, Any]) -> str:
    """
    Generates the HTML and JavaScript block for the DOS Google Chart.
    """
    dos_chart_data = context.get("dos_chart_data", [])
    if not dos_chart_data:
        log.info("No DOS chart data found, skipping chart generation.")
        return ""

    is_spin_polarized = context.get("dos_is_spin_polarized", False)
    dos_data_json = json.dumps(dos_chart_data)

    # We must be careful with indentation in the JS block.
    html_js_block = f"""
<div id="dos_chart_div" style="width: 100%; height: 500px; margin-bottom: 20px;"></div>
<script type="text/javascript">
  // We assume google.charts.load is already called by the SCF chart
  google.charts.setOnLoadCallback(drawDosChart);

  function drawDosChart() {{
    // Parse the JSON data passed from Python
    const dosData = JSON.parse('{dos_data_json}');
    const isSpinPolarized = {str(is_spin_polarized).lower()};

    var data = new google.visualization.DataTable();
    data.addColumn('number', 'Energy (eV vs Fermi)');
    
    var rows;
    
    if (isSpinPolarized) {{
      data.addColumn('number', 'Spin Up');
      data.addColumn('number', 'Spin Down');
      rows = dosData.map(item => [
        item.energy_ev, 
        item.dos_up, 
        item.dos_down // Already negative
      ]);
    }} else {{
      data.addColumn('number', 'DOS');
      rows = dosData.map(item => [
        item.energy_ev, 
        item.dos
      ]);
    }}

    data.addRows(rows);

    var options = {{
      title: '',
      legend: {{ position: 'bottom' }},
      hAxis: {{
        title: 'Energy (eV) [Fermi Energy at 0 eV]'
      }},
      vAxis: {{
        title: 'DOS (States/eV)'
      }},
      // This allows the chart to be responsive
      chartArea: {{'width': '85%', 'height': '75%'}},
      // Ensure spin down is a different color
      series: {{
        1: {{ color: 'red' }}
      }}
    }};

    var chart = new google.visualization.LineChart(document.getElementById('dos_chart_div'));
    chart.draw(data, options);
  }}
</script>
"""
    return html_js_block


def generate_markdown(context: Dict[str, Any]) -> str:
    """
    Generates the full Markdown report string from the extracted context.
    """
    # Pull data from context for readability
    metadata = context.get("metadata", {})
    t_original_data = context.get("t_original_data", {})
    t_cell_data = context.get("t_cell_data", {})

    # --- Generate table strings ---
    material_table = _generate_material_composition_table(context)
    lattice_original_table = _generate_lattice_table(
        context, "original_cell", t_original_data.get("label", "unavailable")
    )
    lattice_cell_table = _generate_lattice_table(context, "cell_type_data", t_cell_data.get("label", "unavailable"))
    symmetry_table = _generate_symmetry_table(context)
    kpoints_table = _generate_kpoints_table(context)
    metadata_table = _generate_metadata_table(context)
    final_energies_table = _generate_final_energies_table(context)

    scf_chart_html = _generate_scf_chart_html(context)
    scf_energies_table = _generate_scf_energies_table(context)

    # --- **NEW:** Generate DOS Chart ---
    dos_chart_html = _generate_dos_chart_html(context)

    # --- Main Markdown f-string ---
    # This is now much cleaner, reading directly from the context.
    markdown_content = f"""
# __{metadata.get("entry_name", "FAIR Parsed Report")}__

<div class="grid cards" markdown>

{{{{ structure_viewer("fair-structure.json") }}}}

{material_table}

</div>

## __Structural information__

<div class="grid cards" markdown>

{lattice_original_table}

{lattice_cell_table}

{symmetry_table}

{kpoints_table}

</div>

## __Metadata__

<div class="grid cards" markdown>

{metadata_table}

</div>

## __Energies__

### SCF Convergence
{scf_chart_html}

<div class="grid cards" markdown>

{final_energies_table}

{scf_energies_table}

</div>

{scf_chart_html}

### Density of States (DOS)
{dos_chart_html}

"""
    return markdown_content


def save_report(content: str, input_path: Path, output_dir: Path):
    """Saves the generated Markdown content to a file."""
    # The output name is based on the *input* JSON file name
    base_name = input_path.stem  # e.g., "fair_parsed_my_calc"
    summary_base_name = base_name.replace("fair_parsed_", "fair_summarized_")
    output_path = output_dir / f"{summary_base_name}.md"

    try:
        output_dir.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        log.info(f"Successfully generated markdown summary at: {output_path}")
    except Exception as e:
        log.error(f"Failed to write summary file: {e}")


# --- Main Orchestration Function ---


def run_summarization(input_path: Path, output_dir: Path, template_path: Optional[str] = None):
    """
    Generates summary reports (e.g., Markdown) from parsed or analyzed data.

    Args:
        input_path: Path to input JSON file (e.g., fair_parsed_vasprun.json).
        output_dir: Directory to save the summary report.
        template_path: Optional path to a custom template (not used here).
    """

    # 1. Load Data
    data = load_data(input_path)
    if not data:
        log.error("Aborting summarization due to data load failure.")
        return

    # 2. Extract Data
    try:
        context = extract_context(data)
        log.info("Successfully extracted data context.")
    except Exception as e:
        log.error(f"Failed during data extraction: {e}", exc_info=True)
        return

    # 3. Generate Markdown
    try:
        markdown_content = generate_markdown(context)
        log.info("Successfully generated Markdown content.")
    except Exception as e:
        log.error(f"Failed during Markdown generation: {e}", exc_info=True)
        return

    # 4. Save Report
    save_report(markdown_content, input_path, output_dir)

    log.info("Summarization process completed.")


# --- Example Usage (if run as a script) ---
if __name__ == "__main__":
    # Configure logging for standalone script testing
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # Define dummy paths for testing
    # Assumes 'fair_parsed_vasprun.json' is in the same directory
    # and we want to output to a 'summary_output' directory

    script_dir = Path(__file__).parent
    test_input = script_dir / "fair_parsed_vasprun.json"
    test_output_dir = script_dir / "summary_output"

    log.info(f"Running summarization for: {test_input}")
    if test_input.exists():
        run_summarization(test_input, test_output_dir)
    else:
        log.error(f"Test input file not found: {test_input}")
