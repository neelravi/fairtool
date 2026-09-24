
# __AcAg VASP GeometryOptimization simulation__

<div class="grid cards" markdown>

{{ structure_viewer("fair-structure.json") }}

- ### Material Composition - original

    | Property                     | Value                       |
    |------------------------------|-----------------------------|
    | Chemical formula (IUPAC) | **AcAg** |
    | Chemical formula (Reduced) | **AcAg** |
    | Label | **original** |
    | Elements | **Ac, Ag** |
    | Number of elements | **2** |
    | Number of atoms | **2** |
    | Dimensionality | **3D** |

</div>

## __Structural information__

<div class="grid cards" markdown>

- ### Lattice (original)

    | Lattice constant | Value     | Units |
    |------------------|-----------|-------|
    | a | **4.610** | Angstrom |
    | b | **4.610** | Angstrom |
    | c | **4.610** | Angstrom |

    | Lattice angles    | Value     | Units |
    |------------------|-----------|-------|
    | Alpha | **60** | Degrees |
    | Beta | **60** | Degrees |
    | Gamma | **60** | Degrees |

    | Cell quantities   | Value     | Units |
    |------------------|-----------|-------|
    | Volume | **69.263** | Å³ |
    | Mass density | **8.028e-27** | kg / Å³ |
    | Atomic density | **0.029** | Å⁻³ |

- ### Lattice (conventional cell)

    | Lattice constant | Value     | Units |
    |------------------|-----------|-------|
    | a | **6.519** | Angstrom |
    | b | **6.519** | Angstrom |
    | c | **6.519** | Angstrom |

    | Lattice angles    | Value     | Units |
    |------------------|-----------|-------|
    | Alpha | **90** | Degrees |
    | Beta | **90** | Degrees |
    | Gamma | **90** | Degrees |

    | Cell quantities   | Value     | Units |
    |------------------|-----------|-------|
    | Volume | **277.053** | Å³ |
    | Mass density | **8.028e-27** | kg / Å³ |
    | Atomic density | **0.029** | Å⁻³ |

- ### Symmetry (conventional cell)

    | Property                       | Value            |
    |---------------------------------|------------------|
    | Crystal system | **cubic** |
    | Bravais lattice | **cF** |
    | Space group symbol | **Fm-3m** |
    | Space group number | **225** |
    | Point group | **m-3m** |
    | Hall number | **523** |
    | Hall symbol | **-F 4 2 3** |
    | Prototype name | **rock salt** |
    | Prototype label aflow | **AB_cF8_225_a_b** |

- ### K points information

    | Property               | Value |
    |------------------------|--------|
    | Dimensionality | **3** |
    | Sampling method | **Gamma-centered** |
    | Number of points | **4096** |
    | Grid | **[16, 16, 16]** |

</div>

## __Metadata__

<div class="grid cards" markdown>

- ### Calculation Metadata

    | Property                   | Value                                                      |
    |----------------------------|------------------------------------------------------------|
    | **Method name** | DFT |
    | **Workflow name** | GeometryOptimization |
    | **Program name** | VASP |
    | **Program version** | 5.3.2 13Sep12 complex serial LinuxIFC |
    | **Basis set type** | plane waves |
    | **Core electron treatment** | pseudopotential |
    | **Jacob's ladder** | GGA |
    | **XC functional names** | GGA_C_PBE, GGA_X_PBE |
    | **Code-specific tier** | VASP - accurate |
    | **Basis set** | plane waves |
    | **Entry type** | VASP GeometryOptimization |
    | **Entry name** | AcAg VASP GeometryOptimization simulation |
    | **Mainfile** | vasprun.xml |

</div>

## __Energies__

### SCF Convergence

<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
<div id="scf_chart_div" style="width: 100%; height: 500px; margin-bottom: 20px;"></div>
<script type="text/javascript">
  google.charts.load('current', {'packages':['corechart']});
  google.charts.setOnLoadCallback(drawChart);

  function drawChart() {
    // Parse the JSON data passed from Python
    const scfData = JSON.parse('[{"step": 1, "total_ev": -7.1926636, "free_ev": -7.20245787, "total_t0_ev": -7.19919312}, {"step": 2, "total_ev": -7.1404007300000005, "free_ev": -7.15039805, "total_t0_ev": -7.147065609999999}, {"step": 3, "total_ev": -7.133523040000001, "free_ev": -7.14350932, "total_t0_ev": -7.14018056}, {"step": 4, "total_ev": -7.13171222, "free_ev": -7.14167597, "total_t0_ev": -7.138354719999999}, {"step": 5, "total_ev": -7.13172722, "free_ev": -7.14167336, "total_t0_ev": -7.13835798}, {"step": 6, "total_ev": -7.13185574, "free_ev": -7.14173545, "total_t0_ev": -7.138442220000001}]');

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

    var options = {
      title: '',
      curveType: 'function',
      legend: { position: 'bottom' },
      hAxis: {
        title: 'SCF Step'
      },
      vAxis: {
        title: 'Energy (eV)'
      },
      // This allows the chart to be responsive
      chartArea: {'width': '85%', 'height': '75%'},
    };

    var chart = new google.visualization.LineChart(document.getElementById('scf_chart_div'));
    chart.draw(data, options);
  }
</script>


<div class="grid cards" markdown>

- ### Final Calculation Energies

    | Energy | Value (eV) |
    |---|---|
    | **Total** | -7.138442 |
    | **Free** | -7.141735 |
    | **Total (T=0)** | -0.009880 |
    | **Band Gap** | 0.000000 |

- ### SCF Iteration Energies

    | Step | Total Energy (eV) | Free Energy (eV) | Total Energy (T=0) (eV) |
    |:---|---:|---:|---:|
| 1 | -7.19266 | -7.20246 | -7.19919 |
| 2 | -7.14040 | -7.15040 | -7.14707 |
| 3 | -7.13352 | -7.14351 | -7.14018 |
| 4 | -7.13171 | -7.14168 | -7.13835 |
| 5 | -7.13173 | -7.14167 | -7.13836 |
| 6 | -7.13186 | -7.14174 | -7.13844 |

</div>


<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
<div id="scf_chart_div" style="width: 100%; height: 500px; margin-bottom: 20px;"></div>
<script type="text/javascript">
  google.charts.load('current', {'packages':['corechart']});
  google.charts.setOnLoadCallback(drawChart);

  function drawChart() {
    // Parse the JSON data passed from Python
    const scfData = JSON.parse('[{"step": 1, "total_ev": -7.1926636, "free_ev": -7.20245787, "total_t0_ev": -7.19919312}, {"step": 2, "total_ev": -7.1404007300000005, "free_ev": -7.15039805, "total_t0_ev": -7.147065609999999}, {"step": 3, "total_ev": -7.133523040000001, "free_ev": -7.14350932, "total_t0_ev": -7.14018056}, {"step": 4, "total_ev": -7.13171222, "free_ev": -7.14167597, "total_t0_ev": -7.138354719999999}, {"step": 5, "total_ev": -7.13172722, "free_ev": -7.14167336, "total_t0_ev": -7.13835798}, {"step": 6, "total_ev": -7.13185574, "free_ev": -7.14173545, "total_t0_ev": -7.138442220000001}]');

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

    var options = {
      title: '',
      curveType: 'function',
      legend: { position: 'bottom' },
      hAxis: {
        title: 'SCF Step'
      },
      vAxis: {
        title: 'Energy (eV)'
      },
      // This allows the chart to be responsive
      chartArea: {'width': '85%', 'height': '75%'},
    };

    var chart = new google.visualization.LineChart(document.getElementById('scf_chart_div'));
    chart.draw(data, options);
  }
</script>


### Density of States (DOS)

<div id="dos_chart_div" style="width: 100%; height: 500px; margin-bottom: 20px;"></div>
<script type="text/javascript">
  // We assume google.charts.load is already called by the SCF chart
  google.charts.setOnLoadCallback(drawDosChart);

  function drawDosChart() {
    // Parse the JSON data passed from Python
    const dosData = JSON.parse('[{"energy_ev": -37.83053993, "dos": 0.0}, {"energy_ev": -37.68193993, "dos": 0.0}, {"energy_ev": -37.53333993, "dos": 0.0}, {"energy_ev": -37.384739929999995, "dos": 0.0}, {"energy_ev": -37.23613993000001, "dos": 0.0}, {"energy_ev": -37.087539930000005, "dos": 0.0}, {"energy_ev": -36.93903993, "dos": 0.0}, {"energy_ev": -36.79043993, "dos": 0.0}, {"energy_ev": -36.641839929999996, "dos": 0.0}, {"energy_ev": -36.49323993, "dos": 0.0}, {"energy_ev": -36.34463993, "dos": -1.185886724147545e+16}, {"energy_ev": -36.196039930000005, "dos": -2.7774715381350394e+17}, {"energy_ev": -36.04743993, "dos": -1.1627931405720402e+18}, {"energy_ev": -35.89883993, "dos": 5.631089486978501e+18}, {"energy_ev": -35.75023993, "dos": 2.3241507340569543e+19}, {"energy_ev": -35.60173993, "dos": 1.524426176346297e+19}, {"energy_ev": -35.45313993, "dos": 1.772588577146857e+17}, {"energy_ev": -35.304539930000004, "dos": -7.639607107139974e+17}, {"energy_ev": -35.15593993, "dos": -6.990490163396054e+16}, {"energy_ev": -35.00733993, "dos": -1872452722338228.8}, {"energy_ev": -34.85873993, "dos": 0.0}, {"energy_ev": -34.71013993, "dos": 0.0}, {"energy_ev": -34.56153993, "dos": 0.0}, {"energy_ev": -34.41293993, "dos": 0.0}, {"energy_ev": -34.26443993, "dos": 0.0}, {"energy_ev": -34.11583993, "dos": 0.0}, {"energy_ev": -33.96723993, "dos": 0.0}, {"energy_ev": -33.818639929999996, "dos": 0.0}, {"energy_ev": -33.67003993, "dos": 0.0}, {"energy_ev": -33.52143993, "dos": 0.0}, {"energy_ev": -33.372839930000005, "dos": 0.0}, {"energy_ev": -33.22423993, "dos": 0.0}, {"energy_ev": -33.07563993, "dos": 0.0}, {"energy_ev": -32.927139929999996, "dos": 0.0}, {"energy_ev": -32.77853993, "dos": 0.0}, {"energy_ev": -32.62993993, "dos": 0.0}, {"energy_ev": -32.481339930000004, "dos": 0.0}, {"energy_ev": -32.33273993, "dos": 0.0}, {"energy_ev": -32.18413993, "dos": 0.0}, {"energy_ev": -32.03553993, "dos": 0.0}, {"energy_ev": -31.88693993, "dos": 0.0}, {"energy_ev": -31.738339930000002, "dos": 0.0}, {"energy_ev": -31.589839930000004, "dos": 0.0}, {"energy_ev": -31.441239930000002, "dos": 0.0}, {"energy_ev": -31.29263993, "dos": 0.0}, {"energy_ev": -31.14403993, "dos": 0.0}, {"energy_ev": -30.99543993, "dos": 0.0}, {"energy_ev": -30.84683993, "dos": 0.0}, {"energy_ev": -30.69823993, "dos": 0.0}, {"energy_ev": -30.549639929999998, "dos": 0.0}, {"energy_ev": -30.401039929999996, "dos": 0.0}, {"energy_ev": -30.25253993, "dos": 0.0}, {"energy_ev": -30.10393993, "dos": 0.0}, {"energy_ev": -29.95533993, "dos": 0.0}, {"energy_ev": -29.80673993, "dos": 0.0}, {"energy_ev": -29.658139929999997, "dos": 0.0}, {"energy_ev": -29.509539929999995, "dos": 0.0}, {"energy_ev": -29.36093993, "dos": 0.0}, {"energy_ev": -29.212339930000002, "dos": 0.0}, {"energy_ev": -29.06383993, "dos": 0.0}, {"energy_ev": -28.91523993, "dos": 0.0}, {"energy_ev": -28.766639929999997, "dos": 0.0}, {"energy_ev": -28.618039930000002, "dos": 0.0}, {"energy_ev": -28.46943993, "dos": 0.0}, {"energy_ev": -28.32083993, "dos": 0.0}, {"energy_ev": -28.17223993, "dos": 0.0}, {"energy_ev": -28.023639930000005, "dos": 0.0}, {"energy_ev": -27.875039930000003, "dos": 0.0}, {"energy_ev": -27.72653993, "dos": 0.0}, {"energy_ev": -27.57793993, "dos": 0.0}, {"energy_ev": -27.42933993, "dos": 0.0}, {"energy_ev": -27.28073993, "dos": 0.0}, {"energy_ev": -27.132139929999997, "dos": 0.0}, {"energy_ev": -26.983539929999996, "dos": 0.0}, {"energy_ev": -26.83493993, "dos": 0.0}, {"energy_ev": -26.68633993, "dos": 0.0}, {"energy_ev": -26.53773993, "dos": 0.0}, {"energy_ev": -26.38923993, "dos": 0.0}, {"energy_ev": -26.240639929999997, "dos": 0.0}, {"energy_ev": -26.092039930000002, "dos": 0.0}, {"energy_ev": -25.94343993, "dos": 0.0}, {"energy_ev": -25.794839930000002, "dos": 0.0}, {"energy_ev": -25.64623993, "dos": 0.0}, {"energy_ev": -25.49763993, "dos": 0.0}, {"energy_ev": -25.349039929999996, "dos": 0.0}, {"energy_ev": -25.200439929999998, "dos": 0.0}, {"energy_ev": -25.05193993, "dos": 0.0}, {"energy_ev": -24.90333993, "dos": 0.0}, {"energy_ev": -24.75473993, "dos": 0.0}, {"energy_ev": -24.606139929999998, "dos": 0.0}, {"energy_ev": -24.457539929999996, "dos": 0.0}, {"energy_ev": -24.30893993, "dos": 0.0}, {"energy_ev": -24.16033993, "dos": 0.0}, {"energy_ev": -24.01173993, "dos": 0.0}, {"energy_ev": -23.86313993, "dos": 0.0}, {"energy_ev": -23.714639929999997, "dos": 0.0}, {"energy_ev": -23.566039930000002, "dos": 0.0}, {"energy_ev": -23.41743993, "dos": 0.0}, {"energy_ev": -23.268839930000002, "dos": 0.0}, {"energy_ev": -23.12023993, "dos": 0.0}, {"energy_ev": -22.97163993, "dos": 0.0}, {"energy_ev": -22.823039929999997, "dos": 0.0}, {"energy_ev": -22.67443993, "dos": 0.0}, {"energy_ev": -22.525839929999997, "dos": 0.0}, {"energy_ev": -22.37733993, "dos": 0.0}, {"energy_ev": -22.22873993, "dos": 0.0}, {"energy_ev": -22.080139929999998, "dos": 0.0}, {"energy_ev": -21.931539929999996, "dos": 0.0}, {"energy_ev": -21.782939929999998, "dos": 0.0}, {"energy_ev": -21.63433993, "dos": 0.0}, {"energy_ev": -21.48573993, "dos": 0.0}, {"energy_ev": -21.33713993, "dos": 0.0}, {"energy_ev": -21.18863993, "dos": 0.0}, {"energy_ev": -21.04003993, "dos": 0.0}, {"energy_ev": -20.89143993, "dos": 0.0}, {"energy_ev": -20.74283993, "dos": 0.0}, {"energy_ev": -20.59423993, "dos": 0.0}, {"energy_ev": -20.445639930000002, "dos": 0.0}, {"energy_ev": -20.29703993, "dos": 0.0}, {"energy_ev": -20.14843993, "dos": 0.0}, {"energy_ev": -19.99983993, "dos": 0.0}, {"energy_ev": -19.851339929999998, "dos": 0.0}, {"energy_ev": -19.70273993, "dos": 0.0}, {"energy_ev": -19.55413993, "dos": 0.0}, {"energy_ev": -19.40553993, "dos": 0.0}, {"energy_ev": -19.25693993, "dos": 0.0}, {"energy_ev": -19.108339930000003, "dos": 0.0}, {"energy_ev": -18.95973993, "dos": 0.0}, {"energy_ev": -18.81113993, "dos": 0.0}, {"energy_ev": -18.66253993, "dos": 0.0}, {"energy_ev": -18.51403993, "dos": 0.0}, {"energy_ev": -18.36543993, "dos": 0.0}, {"energy_ev": -18.216839930000003, "dos": 0.0}, {"energy_ev": -18.06823993, "dos": 0.0}, {"energy_ev": -17.91963993, "dos": 0.0}, {"energy_ev": -17.77103993, "dos": 0.0}, {"energy_ev": -17.62243993, "dos": 0.0}, {"energy_ev": -17.47383993, "dos": 0.0}, {"energy_ev": -17.32523993, "dos": 0.0}, {"energy_ev": -17.17673993, "dos": 0.0}, {"energy_ev": -17.02813993, "dos": 0.0}, {"energy_ev": -16.87953993, "dos": 0.0}, {"energy_ev": -16.730939929999998, "dos": 0.0}, {"energy_ev": -16.58233993, "dos": 0.0}, {"energy_ev": -16.43373993, "dos": -3744905444676457.5}, {"energy_ev": -16.28513993, "dos": -1.1796452150730843e+17}, {"energy_ev": -16.13653993, "dos": -9.224950412053007e+17}, {"energy_ev": -15.987939930000001, "dos": 2.952233792219941e+17}, {"energy_ev": -15.839439930000001, "dos": 1.5898371914466458e+19}, {"energy_ev": -15.690839930000001, "dos": 4.322681939699291e+19}, {"energy_ev": -15.54223993, "dos": 5.071850273906816e+19}, {"energy_ev": -15.39363993, "dos": 1.91202388987031e+19}, {"energy_ev": -15.24503993, "dos": -1.0903916353082953e+18}, {"energy_ev": -15.096439929999999, "dos": -1.0198625827668886e+18}, {"energy_ev": -14.947839929999999, "dos": -8.613282522755853e+16}, {"energy_ev": -14.79923993, "dos": -1872452722338228.8}, {"energy_ev": -14.65063993, "dos": 0.0}, {"energy_ev": -14.50213993, "dos": 0.0}, {"energy_ev": -14.35353993, "dos": 0.0}, {"energy_ev": -14.204939929999998, "dos": 0.0}, {"energy_ev": -14.056339929999998, "dos": 0.0}, {"energy_ev": -13.90773993, "dos": 0.0}, {"energy_ev": -13.759139929999998, "dos": 0.0}, {"energy_ev": -13.610539929999998, "dos": 0.0}, {"energy_ev": -13.46193993, "dos": 0.0}, {"energy_ev": -13.313439930000001, "dos": 0.0}, {"energy_ev": -13.164839930000001, "dos": 0.0}, {"energy_ev": -13.01623993, "dos": 0.0}, {"energy_ev": -12.86763993, "dos": 0.0}, {"energy_ev": -12.719039930000001, "dos": 0.0}, {"energy_ev": -12.570439930000001, "dos": 0.0}, {"energy_ev": -12.421839929999999, "dos": 0.0}, {"energy_ev": -12.27323993, "dos": 0.0}, {"energy_ev": -12.12463993, "dos": 0.0}, {"energy_ev": -11.976139929999999, "dos": 0.0}, {"energy_ev": -11.82753993, "dos": 0.0}, {"energy_ev": -11.678939929999999, "dos": 0.0}, {"energy_ev": -11.530339929999998, "dos": 0.0}, {"energy_ev": -11.38173993, "dos": 0.0}, {"energy_ev": -11.23313993, "dos": 0.0}, {"energy_ev": -11.08453993, "dos": 0.0}, {"energy_ev": -10.935939929999998, "dos": 0.0}, {"energy_ev": -10.78733993, "dos": 0.0}, {"energy_ev": -10.638839929999998, "dos": 0.0}, {"energy_ev": -10.49023993, "dos": 0.0}, {"energy_ev": -10.34163993, "dos": 0.0}, {"energy_ev": -10.19303993, "dos": 0.0}, {"energy_ev": -10.04443993, "dos": 0.0}, {"energy_ev": -9.895839930000001, "dos": 0.0}, {"energy_ev": -9.74723993, "dos": 0.0}, {"energy_ev": -9.598639930000001, "dos": 0.0}, {"energy_ev": -9.45003993, "dos": 0.0}, {"energy_ev": -9.30153993, "dos": 0.0}, {"energy_ev": -9.15293993, "dos": 0.0}, {"energy_ev": -9.00433993, "dos": 0.0}, {"energy_ev": -8.855739929999999, "dos": 0.0}, {"energy_ev": -8.70713993, "dos": 0.0}, {"energy_ev": -8.55853993, "dos": 0.0}, {"energy_ev": -8.40993993, "dos": 0.0}, {"energy_ev": -8.26133993, "dos": 0.0}, {"energy_ev": -8.11273993, "dos": 0.0}, {"energy_ev": -7.96423993, "dos": 0.0}, {"energy_ev": -7.81563993, "dos": 0.0}, {"energy_ev": -7.66703993, "dos": 0.0}, {"energy_ev": -7.5184399299999995, "dos": 0.0}, {"energy_ev": -7.36983993, "dos": 0.0}, {"energy_ev": -7.221239929999999, "dos": 0.0}, {"energy_ev": -7.07263993, "dos": 0.0}, {"energy_ev": -6.924039929999999, "dos": 0.0}, {"energy_ev": -6.77543993, "dos": 0.0}, {"energy_ev": -6.62693993, "dos": 0.0}, {"energy_ev": -6.47833993, "dos": 0.0}, {"energy_ev": -6.329739929999999, "dos": 0.0}, {"energy_ev": -6.18113993, "dos": -1248301814892152.8}, {"energy_ev": -6.03253993, "dos": -3.932150716910281e+16}, {"energy_ev": -5.8839399299999995, "dos": -5.2678336588448845e+17}, {"energy_ev": -5.73533993, "dos": -1.5990746248768474e+18}, {"energy_ev": -5.586739929999999, "dos": 6.997355823377961e+18}, {"energy_ev": -5.43813993, "dos": 4.101982178826358e+19}, {"energy_ev": -5.28963993, "dos": 7.771677439155564e+19}, {"energy_ev": -5.14103993, "dos": 6.98094065451213e+19}, {"energy_ev": -4.99243993, "dos": 2.081356031060431e+19}, {"energy_ev": -4.84383993, "dos": -1.626537264804475e+18}, {"energy_ev": -4.69523993, "dos": -6.472444910215812e+17}, {"energy_ev": -4.5466399299999996, "dos": 5.835810984620814e+17}, {"energy_ev": -4.3980399299999995, "dos": 6.878143000055762e+17}, {"energy_ev": -4.249439929999999, "dos": 7.839335397522717e+17}, {"energy_ev": -4.10093993, "dos": 1.021735035489227e+18}, {"energy_ev": -3.9523399299999995, "dos": 9.374746629840067e+17}, {"energy_ev": -3.80373993, "dos": 1.1259682370327217e+18}, {"energy_ev": -3.65513993, "dos": 1.6046919830438623e+18}, {"energy_ev": -3.50653993, "dos": 2.2669160958441492e+18}, {"energy_ev": -3.3579399299999992, "dos": 3.5345665888671304e+18}, {"energy_ev": -3.20933993, "dos": 4.146234478164285e+18}, {"energy_ev": -3.0607399299999996, "dos": 3.606968094130875e+18}, {"energy_ev": -2.91213993, "dos": 4.02764580574953e+18}, {"energy_ev": -2.7636399299999996, "dos": 4.658038222270068e+18}, {"energy_ev": -2.6150399299999996, "dos": 4.5419461534850975e+18}, {"energy_ev": -2.46643993, "dos": 3.573263945128787e+18}, {"energy_ev": -2.31783993, "dos": 2.2413259086388598e+18}, {"energy_ev": -2.1692399299999994, "dos": 7.951682560863013e+17}, {"energy_ev": -2.0206399299999998, "dos": 1.7101734864022493e+17}, {"energy_ev": -1.8720399299999997, "dos": 8.351139141628502e+17}, {"energy_ev": -1.7234399299999996, "dos": 1.423064068977054e+18}, {"energy_ev": -1.5748399299999996, "dos": 1.9573372457508954e+18}, {"energy_ev": -1.4263399299999997, "dos": 2.677607392943667e+18}, {"energy_ev": -1.2777399299999999, "dos": 3.098285104562323e+18}, {"energy_ev": -1.1291399299999998, "dos": 3.279913018629131e+18}, {"energy_ev": -0.9805399299999997, "dos": 3.327348487595033e+18}, {"energy_ev": -0.8319399299999998, "dos": 3.7967099699944817e+18}, {"energy_ev": -0.6833399299999998, "dos": 3.508352250754395e+18}, {"energy_ev": -0.5347399299999998, "dos": 3.6356790358733947e+18}, {"energy_ev": -0.3861399299999998, "dos": 3.2393432096451364e+18}, {"energy_ev": -0.2375399299999998, "dos": 1.9017878149881948e+18}, {"energy_ev": -0.08903993000000054, "dos": 2.820537950748819e+18}, {"energy_ev": 0.05956007000000005, "dos": 1.1605461973052342e+19}, {"energy_ev": 0.20816007000000006, "dos": 1.8698937036177e+19}, {"energy_ev": 0.35676007000000004, "dos": 1.3322501119436499e+19}, {"energy_ev": 0.50536007, "dos": 9.180635697624337e+18}, {"energy_ev": 0.6539600700000007, "dos": 8.697542895261073e+18}, {"energy_ev": 0.8025600700000001, "dos": 6.715239613212335e+18}, {"energy_ev": 0.9511600700000007, "dos": 4.780995951036944e+18}, {"energy_ev": 1.09976007, "dos": 4.017035240322947e+18}, {"energy_ev": 1.248260070000001, "dos": 3.719939408378615e+18}, {"energy_ev": 1.3968600699999993, "dos": 3.1107681227112443e+18}, {"energy_ev": 1.5454600699999999, "dos": 3.058339446485774e+18}, {"energy_ev": 1.6940600700000004, "dos": 2.8336451198051866e+18}, {"energy_ev": 1.8426600699999998, "dos": 2.796820216265868e+18}, {"energy_ev": 1.9912600700000005, "dos": 3.745529595583904e+18}, {"energy_ev": 2.1398600699999997, "dos": 4.900832925266592e+18}, {"energy_ev": 2.2884600700000006, "dos": 6.081102291247121e+18}, {"energy_ev": 2.43706007, "dos": 6.152255494695974e+18}, {"energy_ev": 2.585560070000001, "dos": 6.314534730631954e+18}, {"energy_ev": 2.73416007, "dos": 7.496052398427377e+18}, {"energy_ev": 2.8827600700000007, "dos": 6.851928661943027e+18}, {"energy_ev": 3.0313600700000003, "dos": 6.907478092705726e+18}, {"energy_ev": 3.179960070000001, "dos": 8.623893088182436e+18}, {"energy_ev": 3.3285600700000004, "dos": 9.29610361550186e+18}, {"energy_ev": 3.477160070000001, "dos": 9.857215281295882e+18}, {"energy_ev": 3.6257600700000014, "dos": 1.0984431820143497e+19}, {"energy_ev": 3.774260069999999, "dos": 1.2134741942566615e+19}, {"energy_ev": 3.9228600699999996, "dos": 1.229327627305792e+19}, {"energy_ev": 4.07146007, "dos": 1.596141115611851e+19}, {"energy_ev": 4.22006007, "dos": 2.144145612349506e+19}, {"energy_ev": 4.36866007, "dos": 2.5014720068623843e+19}, {"energy_ev": 4.51726007, "dos": 2.1116273500715655e+19}, {"energy_ev": 4.66586007, "dos": 1.0702939760885318e+19}, {"energy_ev": 4.814460069999999, "dos": 2.355545524701492e+18}, {"energy_ev": 4.96306007, "dos": -2.3218413756994038e+17}, {"energy_ev": 5.11156007, "dos": -1.691448959178867e+17}, {"energy_ev": 5.26016007, "dos": -1.872452722338229e+16}, {"energy_ev": 5.40876007, "dos": -624150907446076.4}, {"energy_ev": 5.557360070000001, "dos": 0.0}, {"energy_ev": 5.705960070000001, "dos": 0.0}, {"energy_ev": 5.85456007, "dos": 0.0}, {"energy_ev": 6.003160069999999, "dos": 0.0}, {"energy_ev": 6.151760070000001, "dos": 0.0}, {"energy_ev": 6.300360070000001, "dos": 0.0}, {"energy_ev": 6.448860069999999, "dos": 0.0}, {"energy_ev": 6.597460069999999, "dos": 0.0}, {"energy_ev": 6.746060069999998, "dos": 0.0}]');
    const isSpinPolarized = false;

    var data = new google.visualization.DataTable();
    data.addColumn('number', 'Energy (eV vs Fermi)');
    
    var rows;
    
    if (isSpinPolarized) {
      data.addColumn('number', 'Spin Up');
      data.addColumn('number', 'Spin Down');
      rows = dosData.map(item => [
        item.energy_ev, 
        item.dos_up, 
        item.dos_down // Already negative
      ]);
    } else {
      data.addColumn('number', 'DOS');
      rows = dosData.map(item => [
        item.energy_ev, 
        item.dos
      ]);
    }

    data.addRows(rows);

    var options = {
      title: '',
      legend: { position: 'bottom' },
      hAxis: {
        title: 'Energy (eV) [Fermi Energy at 0 eV]'
      },
      vAxis: {
        title: 'DOS (States/eV)'
      },
      // This allows the chart to be responsive
      chartArea: {'width': '85%', 'height': '75%'},
      // Ensure spin down is a different color
      series: {
        1: { color: 'red' }
      }
    };

    var chart = new google.visualization.LineChart(document.getElementById('dos_chart_div'));
    chart.draw(data, options);
  }
</script>


