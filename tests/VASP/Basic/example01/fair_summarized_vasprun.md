
# __Cs2AgHgCl6 VASP DFT SinglePoint simulation__

<div class="grid cards" markdown>

{{ structure_viewer("fair-structure.json") }}

- ### Material Composition - original

    | Property                     | Value                       |
    |------------------------------|-----------------------------|
    | Chemical formula (IUPAC) | **Cs2AgHgCl6** |
    | Chemical formula (Reduced) | **AgCl6Cs2Hg** |
    | Label | **original** |
    | Elements | **Ag, Cl, Cs, Hg** |
    | Number of elements | **4** |
    | Number of atoms | **10** |
    | Dimensionality | **3D** |

</div>

## __Structural information__

<div class="grid cards" markdown>

- ### Lattice (original)

    | Lattice constant | Value     | Units |
    |------------------|-----------|-------|
    | a | **7.311** | Angstrom |
    | b | **7.311** | Angstrom |
    | c | **7.311** | Angstrom |

    | Lattice angles    | Value     | Units |
    |------------------|-----------|-------|
    | Alpha | **60** | Degrees |
    | Beta | **60** | Degrees |
    | Gamma | **60** | Degrees |

    | Cell quantities   | Value     | Units |
    |------------------|-----------|-------|
    | Volume | **276.268** | Å³ |
    | Mass density | **4.730e-27** | kg / Å³ |
    | Atomic density | **0.036** | Å⁻³ |

- ### Lattice (conventional cell)

    | Lattice constant | Value     | Units |
    |------------------|-----------|-------|
    | a | **10.339** | Angstrom |
    | b | **10.339** | Angstrom |
    | c | **10.339** | Angstrom |

    | Lattice angles    | Value     | Units |
    |------------------|-----------|-------|
    | Alpha | **90** | Degrees |
    | Beta | **90** | Degrees |
    | Gamma | **90** | Degrees |

    | Cell quantities   | Value     | Units |
    |------------------|-----------|-------|
    | Volume | **1105.074** | Å³ |
    | Mass density | **4.730e-27** | kg / Å³ |
    | Atomic density | **0.036** | Å⁻³ |

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

- ### K points information

    | Property               | Value |
    |------------------------|--------|
    | Dimensionality | **3** |
    | Sampling method | **Gamma-centered** |
    | Number of points | **64** |
    | Grid | **[4, 4, 4]** |

</div>

## __Metadata__

<div class="grid cards" markdown>

- ### Calculation Metadata

    | Property                   | Value                                                      |
    |----------------------------|------------------------------------------------------------|
    | **Method name** | DFT |
    | **Workflow name** | SinglePoint |
    | **Program name** | VASP |
    | **Program version** | 6.3.0 20Jan22 complex parallel LinuxGNU |
    | **Basis set type** | plane waves |
    | **Core electron treatment** | pseudopotential |
    | **Jacob's ladder** | GGA |
    | **XC functional names** | GGA_C_PBE, GGA_X_PBE |
    | **Code-specific tier** | VASP - normal |
    | **Basis set** | plane waves |
    | **Entry type** | VASP DFT SinglePoint |
    | **Entry name** | Cs2AgHgCl6 VASP DFT SinglePoint simulation |
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
    const scfData = JSON.parse('[{"step": 1, "total_ev": 699.14377904, "free_ev": 699.14377904, "total_t0_ev": 699.14377904}, {"step": 2, "total_ev": 39.53784668, "free_ev": 39.53784668, "total_t0_ev": 39.53784668}, {"step": 3, "total_ev": -29.39822135, "free_ev": -29.39822135, "total_t0_ev": -29.39822135}, {"step": 4, "total_ev": -31.84184981, "free_ev": -31.84185412, "total_t0_ev": -31.84185197}, {"step": 5, "total_ev": -31.95257211, "free_ev": -31.95257728, "total_t0_ev": -31.9525747}, {"step": 6, "total_ev": -23.01513748, "free_ev": -23.01514237, "total_t0_ev": -23.01513993}, {"step": 7, "total_ev": -28.92343522, "free_ev": -28.92343523, "total_t0_ev": -28.92343523}, {"step": 8, "total_ev": -28.75642267, "free_ev": -28.75642381, "total_t0_ev": -28.75642324}, {"step": 9, "total_ev": -29.84021826, "free_ev": -29.84021843, "total_t0_ev": -29.840218340000003}, {"step": 10, "total_ev": -29.927091299999997, "free_ev": -29.927094109999995, "total_t0_ev": -29.92709271}, {"step": 11, "total_ev": -29.897942950000004, "free_ev": -29.897945760000002, "total_t0_ev": -29.89794435}, {"step": 12, "total_ev": -29.95272426, "free_ev": -29.952727229999997, "total_t0_ev": -29.95272575}, {"step": 13, "total_ev": -29.958725700000002, "free_ev": -29.95872851, "total_t0_ev": -29.958727100000004}, {"step": 14, "total_ev": -29.95940956, "free_ev": -29.95941237, "total_t0_ev": -29.95941097}, {"step": 15, "total_ev": -29.95944214, "free_ev": -29.959444950000005, "total_t0_ev": -29.95944354}, {"step": 16, "total_ev": -29.959530640000004, "free_ev": -29.959533450000002, "total_t0_ev": -29.95953204}, {"step": 17, "total_ev": -29.95962655, "free_ev": -29.959629370000002, "total_t0_ev": -29.95962796}, {"step": 18, "total_ev": -29.959630790000002, "free_ev": -29.95963359, "total_t0_ev": -29.95963219}, {"step": 19, "total_ev": -29.95964678, "free_ev": -29.95964959, "total_t0_ev": -29.95964819}, {"step": 20, "total_ev": -29.95965715, "free_ev": -29.95965996, "total_t0_ev": -29.959658560000005}, {"step": 21, "total_ev": -29.95964039, "free_ev": -29.95964319, "total_t0_ev": -29.95964179}, {"step": 22, "total_ev": -29.959668219999998, "free_ev": -29.959671029999996, "total_t0_ev": -29.95966963}, {"step": 23, "total_ev": -29.95967692, "free_ev": -29.959679720000004, "total_t0_ev": -29.959678320000002}, {"step": 24, "total_ev": -29.95967697, "free_ev": -29.95968042, "total_t0_ev": -29.9596787}, {"step": 25, "total_ev": -29.95976083, "free_ev": -29.95976373, "total_t0_ev": -29.959762280000003}, {"step": 26, "total_ev": -29.959692070000003, "free_ev": -29.95969488, "total_t0_ev": -29.95969348}, {"step": 27, "total_ev": -29.959678420000003, "free_ev": -29.95968123, "total_t0_ev": -29.95967983}, {"step": 28, "total_ev": -29.9596972, "free_ev": -29.95970057, "total_t0_ev": -29.95969888}, {"step": 29, "total_ev": -29.959757799999995, "free_ev": -29.95976141, "total_t0_ev": -29.959759609999995}, {"step": 30, "total_ev": -29.95979699, "free_ev": -29.95979989, "total_t0_ev": -29.959798440000004}, {"step": 31, "total_ev": -29.95971031, "free_ev": -29.95971353, "total_t0_ev": -29.95971192}, {"step": 32, "total_ev": -29.95973759, "free_ev": -29.9597404, "total_t0_ev": -29.959739}, {"step": 33, "total_ev": -29.95966008, "free_ev": -29.95966288, "total_t0_ev": -29.95966148}, {"step": 34, "total_ev": -29.95967863, "free_ev": -29.95968225, "total_t0_ev": -29.95968044}, {"step": 35, "total_ev": -29.95980177, "free_ev": -29.95980528, "total_t0_ev": -29.95980352}, {"step": 36, "total_ev": -29.95978607, "free_ev": -29.9597897, "total_t0_ev": -29.95978789}, {"step": 37, "total_ev": -29.9598037, "free_ev": -29.95980735, "total_t0_ev": -29.959805529999997}, {"step": 38, "total_ev": -29.959805699999997, "free_ev": -29.95980864, "total_t0_ev": -29.959807169999998}, {"step": 39, "total_ev": -29.95971226, "free_ev": -29.9597159, "total_t0_ev": -29.95971408}, {"step": 40, "total_ev": -29.95980038, "free_ev": -29.959804009999996, "total_t0_ev": -29.95980219}, {"step": 41, "total_ev": -29.9598011, "free_ev": -29.95980474, "total_t0_ev": -29.95980292}]');

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
    | **Total** | -29.959801 |
    | **Free** | -29.959805 |
    | **Total (T=0)** | -29.959803 |
    | **Band Gap** | 0.000000 |

- ### SCF Iteration Energies

    | Step | Total Energy (eV) | Free Energy (eV) | Total Energy (T=0) (eV) |
    |:---|---:|---:|---:|
| 1 | 699.14378 | 699.14378 | 699.14378 |
| 2 | 39.53785 | 39.53785 | 39.53785 |
| 3 | -29.39822 | -29.39822 | -29.39822 |
| 4 | -31.84185 | -31.84185 | -31.84185 |
| 5 | -31.95257 | -31.95258 | -31.95257 |
| 6 | -23.01514 | -23.01514 | -23.01514 |
| 7 | -28.92344 | -28.92344 | -28.92344 |
| 8 | -28.75642 | -28.75642 | -28.75642 |
| 9 | -29.84022 | -29.84022 | -29.84022 |
| 10 | -29.92709 | -29.92709 | -29.92709 |
| 11 | -29.89794 | -29.89795 | -29.89794 |
| 12 | -29.95272 | -29.95273 | -29.95273 |
| 13 | -29.95873 | -29.95873 | -29.95873 |
| 14 | -29.95941 | -29.95941 | -29.95941 |
| 15 | -29.95944 | -29.95944 | -29.95944 |
| 16 | -29.95953 | -29.95953 | -29.95953 |
| 17 | -29.95963 | -29.95963 | -29.95963 |
| 18 | -29.95963 | -29.95963 | -29.95963 |
| 19 | -29.95965 | -29.95965 | -29.95965 |
| 20 | -29.95966 | -29.95966 | -29.95966 |
| 21 | -29.95964 | -29.95964 | -29.95964 |
| 22 | -29.95967 | -29.95967 | -29.95967 |
| 23 | -29.95968 | -29.95968 | -29.95968 |
| 24 | -29.95968 | -29.95968 | -29.95968 |
| 25 | -29.95976 | -29.95976 | -29.95976 |
| 26 | -29.95969 | -29.95969 | -29.95969 |
| 27 | -29.95968 | -29.95968 | -29.95968 |
| 28 | -29.95970 | -29.95970 | -29.95970 |
| 29 | -29.95976 | -29.95976 | -29.95976 |
| 30 | -29.95980 | -29.95980 | -29.95980 |
| 31 | -29.95971 | -29.95971 | -29.95971 |
| 32 | -29.95974 | -29.95974 | -29.95974 |
| 33 | -29.95966 | -29.95966 | -29.95966 |
| 34 | -29.95968 | -29.95968 | -29.95968 |
| 35 | -29.95980 | -29.95981 | -29.95980 |
| 36 | -29.95979 | -29.95979 | -29.95979 |
| 37 | -29.95980 | -29.95981 | -29.95981 |
| 38 | -29.95981 | -29.95981 | -29.95981 |
| 39 | -29.95971 | -29.95972 | -29.95971 |
| 40 | -29.95980 | -29.95980 | -29.95980 |
| 41 | -29.95980 | -29.95980 | -29.95980 |

</div>


<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
<div id="scf_chart_div" style="width: 100%; height: 500px; margin-bottom: 20px;"></div>
<script type="text/javascript">
  google.charts.load('current', {'packages':['corechart']});
  google.charts.setOnLoadCallback(drawChart);

  function drawChart() {
    // Parse the JSON data passed from Python
    const scfData = JSON.parse('[{"step": 1, "total_ev": 699.14377904, "free_ev": 699.14377904, "total_t0_ev": 699.14377904}, {"step": 2, "total_ev": 39.53784668, "free_ev": 39.53784668, "total_t0_ev": 39.53784668}, {"step": 3, "total_ev": -29.39822135, "free_ev": -29.39822135, "total_t0_ev": -29.39822135}, {"step": 4, "total_ev": -31.84184981, "free_ev": -31.84185412, "total_t0_ev": -31.84185197}, {"step": 5, "total_ev": -31.95257211, "free_ev": -31.95257728, "total_t0_ev": -31.9525747}, {"step": 6, "total_ev": -23.01513748, "free_ev": -23.01514237, "total_t0_ev": -23.01513993}, {"step": 7, "total_ev": -28.92343522, "free_ev": -28.92343523, "total_t0_ev": -28.92343523}, {"step": 8, "total_ev": -28.75642267, "free_ev": -28.75642381, "total_t0_ev": -28.75642324}, {"step": 9, "total_ev": -29.84021826, "free_ev": -29.84021843, "total_t0_ev": -29.840218340000003}, {"step": 10, "total_ev": -29.927091299999997, "free_ev": -29.927094109999995, "total_t0_ev": -29.92709271}, {"step": 11, "total_ev": -29.897942950000004, "free_ev": -29.897945760000002, "total_t0_ev": -29.89794435}, {"step": 12, "total_ev": -29.95272426, "free_ev": -29.952727229999997, "total_t0_ev": -29.95272575}, {"step": 13, "total_ev": -29.958725700000002, "free_ev": -29.95872851, "total_t0_ev": -29.958727100000004}, {"step": 14, "total_ev": -29.95940956, "free_ev": -29.95941237, "total_t0_ev": -29.95941097}, {"step": 15, "total_ev": -29.95944214, "free_ev": -29.959444950000005, "total_t0_ev": -29.95944354}, {"step": 16, "total_ev": -29.959530640000004, "free_ev": -29.959533450000002, "total_t0_ev": -29.95953204}, {"step": 17, "total_ev": -29.95962655, "free_ev": -29.959629370000002, "total_t0_ev": -29.95962796}, {"step": 18, "total_ev": -29.959630790000002, "free_ev": -29.95963359, "total_t0_ev": -29.95963219}, {"step": 19, "total_ev": -29.95964678, "free_ev": -29.95964959, "total_t0_ev": -29.95964819}, {"step": 20, "total_ev": -29.95965715, "free_ev": -29.95965996, "total_t0_ev": -29.959658560000005}, {"step": 21, "total_ev": -29.95964039, "free_ev": -29.95964319, "total_t0_ev": -29.95964179}, {"step": 22, "total_ev": -29.959668219999998, "free_ev": -29.959671029999996, "total_t0_ev": -29.95966963}, {"step": 23, "total_ev": -29.95967692, "free_ev": -29.959679720000004, "total_t0_ev": -29.959678320000002}, {"step": 24, "total_ev": -29.95967697, "free_ev": -29.95968042, "total_t0_ev": -29.9596787}, {"step": 25, "total_ev": -29.95976083, "free_ev": -29.95976373, "total_t0_ev": -29.959762280000003}, {"step": 26, "total_ev": -29.959692070000003, "free_ev": -29.95969488, "total_t0_ev": -29.95969348}, {"step": 27, "total_ev": -29.959678420000003, "free_ev": -29.95968123, "total_t0_ev": -29.95967983}, {"step": 28, "total_ev": -29.9596972, "free_ev": -29.95970057, "total_t0_ev": -29.95969888}, {"step": 29, "total_ev": -29.959757799999995, "free_ev": -29.95976141, "total_t0_ev": -29.959759609999995}, {"step": 30, "total_ev": -29.95979699, "free_ev": -29.95979989, "total_t0_ev": -29.959798440000004}, {"step": 31, "total_ev": -29.95971031, "free_ev": -29.95971353, "total_t0_ev": -29.95971192}, {"step": 32, "total_ev": -29.95973759, "free_ev": -29.9597404, "total_t0_ev": -29.959739}, {"step": 33, "total_ev": -29.95966008, "free_ev": -29.95966288, "total_t0_ev": -29.95966148}, {"step": 34, "total_ev": -29.95967863, "free_ev": -29.95968225, "total_t0_ev": -29.95968044}, {"step": 35, "total_ev": -29.95980177, "free_ev": -29.95980528, "total_t0_ev": -29.95980352}, {"step": 36, "total_ev": -29.95978607, "free_ev": -29.9597897, "total_t0_ev": -29.95978789}, {"step": 37, "total_ev": -29.9598037, "free_ev": -29.95980735, "total_t0_ev": -29.959805529999997}, {"step": 38, "total_ev": -29.959805699999997, "free_ev": -29.95980864, "total_t0_ev": -29.959807169999998}, {"step": 39, "total_ev": -29.95971226, "free_ev": -29.9597159, "total_t0_ev": -29.95971408}, {"step": 40, "total_ev": -29.95980038, "free_ev": -29.959804009999996, "total_t0_ev": -29.95980219}, {"step": 41, "total_ev": -29.9598011, "free_ev": -29.95980474, "total_t0_ev": -29.95980292}]');

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
    const dosData = JSON.parse('[{"energy_ev": -20.99259739, "dos": 0.0}, {"energy_ev": -20.89359739, "dos": 0.0}, {"energy_ev": -20.79459739, "dos": 0.0}, {"energy_ev": -20.69559739, "dos": 0.0}, {"energy_ev": -20.59669739, "dos": 0.0}, {"energy_ev": -20.49769739, "dos": 0.0}, {"energy_ev": -20.39869739, "dos": 0.0}, {"energy_ev": -20.29969739, "dos": 0.0}, {"energy_ev": -20.20069739, "dos": 0.0}, {"energy_ev": -20.101797389999998, "dos": 0.0}, {"energy_ev": -20.002797389999998, "dos": 0.0}, {"energy_ev": -19.903797389999998, "dos": 0.0}, {"energy_ev": -19.804797389999997, "dos": 0.0}, {"energy_ev": -19.705797390000004, "dos": 0.0}, {"energy_ev": -19.60689739, "dos": 0.0}, {"energy_ev": -19.507897390000004, "dos": 0.0}, {"energy_ev": -19.40889739, "dos": 0.0}, {"energy_ev": -19.30989739, "dos": 0.0}, {"energy_ev": -19.21099739, "dos": 0.0}, {"energy_ev": -19.11199739, "dos": 0.0}, {"energy_ev": -19.01299739, "dos": 0.0}, {"energy_ev": -18.91399739, "dos": 0.0}, {"energy_ev": -18.814997390000002, "dos": 0.0}, {"energy_ev": -18.716097389999998, "dos": 0.0}, {"energy_ev": -18.61709739, "dos": 0.0}, {"energy_ev": -18.518097389999998, "dos": 0.0}, {"energy_ev": -18.419097389999997, "dos": 0.0}, {"energy_ev": -18.320097390000004, "dos": 0.0}, {"energy_ev": -18.22119739, "dos": 0.0}, {"energy_ev": -18.122197390000004, "dos": 0.0}, {"energy_ev": -18.02319739, "dos": 0.0}, {"energy_ev": -17.92419739, "dos": 0.0}, {"energy_ev": -17.82529739, "dos": 0.0}, {"energy_ev": -17.72629739, "dos": 0.0}, {"energy_ev": -17.62729739, "dos": 0.0}, {"energy_ev": -17.52829739, "dos": 0.0}, {"energy_ev": -17.429297390000002, "dos": 0.0}, {"energy_ev": -17.33039739, "dos": 0.0}, {"energy_ev": -17.23139739, "dos": 0.0}, {"energy_ev": -17.13239739, "dos": 0.0}, {"energy_ev": -17.03339739, "dos": 0.0}, {"energy_ev": -16.93449739, "dos": 0.0}, {"energy_ev": -16.83549739, "dos": 0.0}, {"energy_ev": -16.73649739, "dos": 0.0}, {"energy_ev": -16.63749739, "dos": 0.0}, {"energy_ev": -16.53849739, "dos": 0.0}, {"energy_ev": -16.43959739, "dos": 0.0}, {"energy_ev": -16.34059739, "dos": 0.0}, {"energy_ev": -16.24159739, "dos": 0.0}, {"energy_ev": -16.14259739, "dos": 0.0}, {"energy_ev": -16.04359739, "dos": 0.0}, {"energy_ev": -15.944697389999998, "dos": 0.0}, {"energy_ev": -15.84569739, "dos": 0.0}, {"energy_ev": -15.746697390000001, "dos": 0.0}, {"energy_ev": -15.647697390000001, "dos": 0.0}, {"energy_ev": -15.54879739, "dos": 0.0}, {"energy_ev": -15.44979739, "dos": 0.0}, {"energy_ev": -15.350797389999999, "dos": 0.0}, {"energy_ev": -15.251797389999998, "dos": 0.0}, {"energy_ev": -15.15279739, "dos": 0.0}, {"energy_ev": -15.053897390000001, "dos": 0.0}, {"energy_ev": -14.95489739, "dos": 0.0}, {"energy_ev": -14.855897389999999, "dos": 0.0}, {"energy_ev": -14.75689739, "dos": 0.0}, {"energy_ev": -14.65789739, "dos": 0.0}, {"energy_ev": -14.55899739, "dos": 0.0}, {"energy_ev": -14.45999739, "dos": 0.0}, {"energy_ev": -14.360997390000001, "dos": 0.0}, {"energy_ev": -14.261997390000001, "dos": 0.0}, {"energy_ev": -14.16309739, "dos": 0.0}, {"energy_ev": -14.06409739, "dos": 0.0}, {"energy_ev": -13.965097389999999, "dos": 0.0}, {"energy_ev": -13.866097389999998, "dos": 0.0}, {"energy_ev": -13.76709739, "dos": 0.0}, {"energy_ev": -13.66819739, "dos": 0.0}, {"energy_ev": -13.56919739, "dos": 0.0}, {"energy_ev": -13.47019739, "dos": 0.0}, {"energy_ev": -13.37119739, "dos": 0.0}, {"energy_ev": -13.27219739, "dos": 0.0}, {"energy_ev": -13.17329739, "dos": 0.0}, {"energy_ev": -13.074297390000002, "dos": 0.0}, {"energy_ev": -12.975297390000001, "dos": 0.0}, {"energy_ev": -12.876297390000001, "dos": 0.0}, {"energy_ev": -12.77739739, "dos": 0.0}, {"energy_ev": -12.67839739, "dos": 0.0}, {"energy_ev": -12.579397389999999, "dos": 0.0}, {"energy_ev": -12.48039739, "dos": 0.0}, {"energy_ev": -12.38139739, "dos": 0.0}, {"energy_ev": -12.28249739, "dos": 0.0}, {"energy_ev": -12.18349739, "dos": 0.0}, {"energy_ev": -12.08449739, "dos": 0.0}, {"energy_ev": -11.985497389999999, "dos": 0.0}, {"energy_ev": -11.886597389999999, "dos": 0.0}, {"energy_ev": -11.787597389999998, "dos": 0.0}, {"energy_ev": -11.68859739, "dos": 0.0}, {"energy_ev": -11.589597390000002, "dos": 0.0}, {"energy_ev": -11.49059739, "dos": 0.0}, {"energy_ev": -11.391697390000001, "dos": 0.0}, {"energy_ev": -11.292697389999999, "dos": 0.0}, {"energy_ev": -11.193697389999999, "dos": 0.0}, {"energy_ev": -11.094697389999999, "dos": 0.0}, {"energy_ev": -10.995697389999998, "dos": 0.0}, {"energy_ev": -10.89679739, "dos": 0.0}, {"energy_ev": -10.797797390000001, "dos": 0.0}, {"energy_ev": -10.69879739, "dos": 0.0}, {"energy_ev": -10.59979739, "dos": 0.0}, {"energy_ev": -10.500897389999999, "dos": 0.0}, {"energy_ev": -10.40189739, "dos": 0.0}, {"energy_ev": -10.302897389999998, "dos": 0.0}, {"energy_ev": -10.203897390000002, "dos": 0.0}, {"energy_ev": -10.10489739, "dos": 0.0}, {"energy_ev": -10.005997390000001, "dos": 0.0}, {"energy_ev": -9.906997389999999, "dos": 0.0}, {"energy_ev": -9.80799739, "dos": 0.0}, {"energy_ev": -9.708997389999999, "dos": 0.0}, {"energy_ev": -9.60999739, "dos": 0.0}, {"energy_ev": -9.51109739, "dos": 0.0}, {"energy_ev": -9.41209739, "dos": 0.0}, {"energy_ev": -9.31309739, "dos": 0.0}, {"energy_ev": -9.214097390000001, "dos": 0.0}, {"energy_ev": -9.115197389999999, "dos": 0.0}, {"energy_ev": -9.01619739, "dos": 0.0}, {"energy_ev": -8.91719739, "dos": 0.0}, {"energy_ev": -8.81819739, "dos": 0.0}, {"energy_ev": -8.71919739, "dos": 0.0}, {"energy_ev": -8.62029739, "dos": 0.0}, {"energy_ev": -8.521297389999999, "dos": 0.0}, {"energy_ev": -8.42229739, "dos": 0.0}, {"energy_ev": -8.323297389999999, "dos": 0.0}, {"energy_ev": -8.22439739, "dos": 0.0}, {"energy_ev": -8.12539739, "dos": 0.0}, {"energy_ev": -8.02639739, "dos": 0.0}, {"energy_ev": -7.927397390000001, "dos": 0.0}, {"energy_ev": -7.82839739, "dos": 0.0}, {"energy_ev": -7.729497389999999, "dos": 0.0}, {"energy_ev": -7.63049739, "dos": 0.0}, {"energy_ev": -7.53149739, "dos": 0.0}, {"energy_ev": -7.432497389999999, "dos": 0.0}, {"energy_ev": -7.33349739, "dos": 0.0}, {"energy_ev": -7.23459739, "dos": 0.0}, {"energy_ev": -7.135597390000001, "dos": 0.0}, {"energy_ev": -7.03659739, "dos": 0.0}, {"energy_ev": -6.9375973900000005, "dos": 0.0}, {"energy_ev": -6.83869739, "dos": 0.0}, {"energy_ev": -6.73969739, "dos": 0.0}, {"energy_ev": -6.640697389999999, "dos": 7.882401810136497e+18}, {"energy_ev": -6.54169739, "dos": 0.0}, {"energy_ev": -6.44269739, "dos": 0.0}, {"energy_ev": -6.34379739, "dos": 0.0}, {"energy_ev": -6.24479739, "dos": 0.0}, {"energy_ev": -6.14579739, "dos": 0.0}, {"energy_ev": -6.04679739, "dos": 0.0}, {"energy_ev": -5.94779739, "dos": 0.0}, {"energy_ev": -5.84889739, "dos": 0.0}, {"energy_ev": -5.749897389999999, "dos": 0.0}, {"energy_ev": -5.65089739, "dos": 0.0}, {"energy_ev": -5.551897390000001, "dos": 0.0}, {"energy_ev": -5.45299739, "dos": 0.0}, {"energy_ev": -5.35399739, "dos": 0.0}, {"energy_ev": -5.25499739, "dos": 0.0}, {"energy_ev": -5.1559973900000005, "dos": 0.0}, {"energy_ev": -5.05699739, "dos": 0.0}, {"energy_ev": -4.95809739, "dos": 0.0}, {"energy_ev": -4.85909739, "dos": 0.0}, {"energy_ev": -4.760097389999999, "dos": 0.0}, {"energy_ev": -4.66109739, "dos": 0.0}, {"energy_ev": -4.56209739, "dos": 0.0}, {"energy_ev": -4.4631973899999995, "dos": 0.0}, {"energy_ev": -4.364197389999999, "dos": 0.0}, {"energy_ev": -4.26519739, "dos": 0.0}, {"energy_ev": -4.16619739, "dos": 0.0}, {"energy_ev": -4.06729739, "dos": 0.0}, {"energy_ev": -3.96829739, "dos": 0.0}, {"energy_ev": -3.86929739, "dos": 0.0}, {"energy_ev": -3.77029739, "dos": 0.0}, {"energy_ev": -3.67129739, "dos": 0.0}, {"energy_ev": -3.57239739, "dos": 0.0}, {"energy_ev": -3.4733973899999997, "dos": 0.0}, {"energy_ev": -3.37439739, "dos": 0.0}, {"energy_ev": -3.27539739, "dos": 0.0}, {"energy_ev": -3.17649739, "dos": 0.0}, {"energy_ev": -3.0774973899999996, "dos": 0.0}, {"energy_ev": -2.9784973900000002, "dos": 0.0}, {"energy_ev": -2.87949739, "dos": 0.0}, {"energy_ev": -2.78049739, "dos": 0.0}, {"energy_ev": -2.68159739, "dos": 0.0}, {"energy_ev": -2.58259739, "dos": 0.0}, {"energy_ev": -2.48359739, "dos": 0.0}, {"energy_ev": -2.3845973899999997, "dos": 0.0}, {"energy_ev": -2.28559739, "dos": 0.0}, {"energy_ev": -2.18669739, "dos": 0.0}, {"energy_ev": -2.08769739, "dos": 0.0}, {"energy_ev": -1.98869739, "dos": 0.0}, {"energy_ev": -1.8896973899999998, "dos": 0.0}, {"energy_ev": -1.7907973899999998, "dos": 0.0}, {"energy_ev": -1.6917973899999998, "dos": 0.0}, {"energy_ev": -1.59279739, "dos": 1.9323712094530522e+18}, {"energy_ev": -1.49379739, "dos": 0.0}, {"energy_ev": -1.39479739, "dos": 0.0}, {"energy_ev": -1.29589739, "dos": 0.0}, {"energy_ev": -1.1968973899999997, "dos": 0.0}, {"energy_ev": -1.09789739, "dos": 0.0}, {"energy_ev": -0.99889739, "dos": 0.0}, {"energy_ev": -0.8998973899999999, "dos": 0.0}, {"energy_ev": -0.8009973899999999, "dos": 0.0}, {"energy_ev": -0.70199739, "dos": 0.0}, {"energy_ev": -0.6029973899999997, "dos": 0.0}, {"energy_ev": -0.5039973899999999, "dos": 0.0}, {"energy_ev": -0.40509738999999995, "dos": 0.0}, {"energy_ev": -0.30609738999999997, "dos": 0.0}, {"energy_ev": -0.2070973899999999, "dos": 0.0}, {"energy_ev": -0.10809738999999981, "dos": 0.0}, {"energy_ev": -0.009097390000000023, "dos": 0.0}, {"energy_ev": 0.0898026099999999, "dos": 0.0}, {"energy_ev": 0.18880260999999998, "dos": 0.0}, {"energy_ev": 0.28780261000000007, "dos": 0.0}, {"energy_ev": 0.38680261000000016, "dos": 0.0}, {"energy_ev": 0.48580260999999997, "dos": 0.0}, {"energy_ev": 0.5847026099999999, "dos": 0.0}, {"energy_ev": 0.6837026100000002, "dos": 0.0}, {"energy_ev": 0.7827026099999997, "dos": 0.0}, {"energy_ev": 0.8817026100000002, "dos": 0.0}, {"energy_ev": 0.98060261, "dos": 0.0}, {"energy_ev": 1.0796026100000002, "dos": 0.0}, {"energy_ev": 1.1786026100000002, "dos": 0.0}, {"energy_ev": 1.2776026100000004, "dos": 0.0}, {"energy_ev": 1.3766026099999997, "dos": 0.0}, {"energy_ev": 1.4755026099999997, "dos": 0.0}, {"energy_ev": 1.5745026100000004, "dos": 0.0}, {"energy_ev": 1.67350261, "dos": 0.0}, {"energy_ev": 1.77250261, "dos": 0.0}, {"energy_ev": 1.8714026099999999, "dos": 0.0}, {"energy_ev": 1.97040261, "dos": 0.0}, {"energy_ev": 2.06940261, "dos": 0.0}, {"energy_ev": 2.1684026100000002, "dos": 0.0}, {"energy_ev": 2.2674026100000004, "dos": 0.0}, {"energy_ev": 2.36630261, "dos": 0.0}, {"energy_ev": 2.46530261, "dos": 0.0}, {"energy_ev": 2.5643026100000004, "dos": 0.0}, {"energy_ev": 2.6633026099999997, "dos": 0.0}, {"energy_ev": 2.76230261, "dos": 0.0}, {"energy_ev": 2.8612026100000003, "dos": 0.0}, {"energy_ev": 2.96020261, "dos": 0.0}, {"energy_ev": 3.05920261, "dos": 0.0}, {"energy_ev": 3.15820261, "dos": 0.0}, {"energy_ev": 3.2571026100000005, "dos": 0.0}, {"energy_ev": 3.3561026099999993, "dos": 0.0}, {"energy_ev": 3.4551026100000004, "dos": 0.0}, {"energy_ev": 3.55410261, "dos": 0.0}, {"energy_ev": 3.6531026100000004, "dos": 0.0}, {"energy_ev": 3.7520026100000003, "dos": 0.0}, {"energy_ev": 3.8510026099999997, "dos": 0.0}, {"energy_ev": 3.9500026100000003, "dos": 0.0}, {"energy_ev": 4.04900261, "dos": 0.0}, {"energy_ev": 4.14800261, "dos": 0.0}, {"energy_ev": 4.24690261, "dos": 0.0}, {"energy_ev": 4.34590261, "dos": 0.0}, {"energy_ev": 4.44490261, "dos": 0.0}, {"energy_ev": 4.54390261, "dos": 0.0}, {"energy_ev": 4.64280261, "dos": 0.0}, {"energy_ev": 4.74180261, "dos": 0.0}, {"energy_ev": 4.84080261, "dos": 0.0}, {"energy_ev": 4.93980261, "dos": 0.0}, {"energy_ev": 5.03880261, "dos": 0.0}, {"energy_ev": 5.137702610000001, "dos": 0.0}, {"energy_ev": 5.23670261, "dos": 0.0}, {"energy_ev": 5.33570261, "dos": 0.0}, {"energy_ev": 5.43470261, "dos": 0.0}, {"energy_ev": 5.53360261, "dos": 0.0}, {"energy_ev": 5.632602610000001, "dos": 0.0}, {"energy_ev": 5.73160261, "dos": 0.0}, {"energy_ev": 5.83060261, "dos": 3744905444676457.5}, {"energy_ev": 5.929602610000001, "dos": 0.0}, {"energy_ev": 6.02850261, "dos": 0.0}, {"energy_ev": 6.12750261, "dos": 0.0}, {"energy_ev": 6.226502610000001, "dos": 0.0}, {"energy_ev": 6.32550261, "dos": 0.0}, {"energy_ev": 6.42450261, "dos": 0.0}, {"energy_ev": 6.523402610000001, "dos": 1.9704444148072627e+18}, {"energy_ev": 6.622402610000001, "dos": 0.0}, {"energy_ev": 6.721402609999999, "dos": 0.0}, {"energy_ev": 6.820402609999999, "dos": 0.0}, {"energy_ev": 6.91930261, "dos": 0.0}, {"energy_ev": 7.018302609999999, "dos": 0.0}, {"energy_ev": 7.11730261, "dos": 1.9704444148072627e+18}, {"energy_ev": 7.216302610000001, "dos": 0.0}, {"energy_ev": 7.315302610000001, "dos": 0.0}, {"energy_ev": 7.414202609999999, "dos": 0.0}, {"energy_ev": 7.51320261, "dos": 0.0}, {"energy_ev": 7.61220261, "dos": 0.0}, {"energy_ev": 7.71120261, "dos": 0.0}, {"energy_ev": 7.810202610000001, "dos": 0.0}, {"energy_ev": 7.909102610000001, "dos": 0.0}, {"energy_ev": 8.008102610000002, "dos": 0.0}, {"energy_ev": 8.10710261, "dos": 0.0}, {"energy_ev": 8.206102609999999, "dos": 0.0}, {"energy_ev": 8.30500261, "dos": 0.0}, {"energy_ev": 8.40400261, "dos": 0.0}, {"energy_ev": 8.503002610000001, "dos": 0.0}, {"energy_ev": 8.60200261, "dos": 0.0}, {"energy_ev": 8.70100261, "dos": 0.0}]');
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


