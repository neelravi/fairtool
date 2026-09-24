
# __C428H42N8O8 VASP DFT SinglePoint simulation__

<div class="grid cards" markdown>

{{ structure_viewer("fair-structure.json") }}

- ### Material Composition - original

    | Property                     | Value                       |
    |------------------------------|-----------------------------|
    | Chemical formula (IUPAC) | **C214N4H21O4** |
    | Chemical formula (Reduced) | **C214H21N4O4** |
    | Label | **original** |
    | Elements | **C, H, N, O** |
    | Number of elements | **4** |
    | Number of atoms | **486** |

</div>

## __Structural information__

<div class="grid cards" markdown>

- ### Lattice (original)

    | Lattice constant | Value     | Units |
    |------------------|-----------|-------|
    | a | **29.774** | Angstrom |
    | b | **30.067** | Angstrom |
    | c | **29.542** | Angstrom |

    | Lattice angles    | Value     | Units |
    |------------------|-----------|-------|
    | Alpha | **90** | Degrees |
    | Beta | **90** | Degrees |
    | Gamma | **90** | Degrees |

    | Cell quantities   | Value     | Units |
    |------------------|-----------|-------|
    | Volume | **26445.060** | Å³ |
    | Mass density | **3.405e-28** | kg / Å³ |
    | Atomic density | **0.018** | Å⁻³ |





- ### K points information

    | Property               | Value |
    |------------------------|--------|
    | Dimensionality | **3** |
    | Sampling method | **Gamma-centered** |
    | Number of points | **9** |
    | Grid | **[3, 3, 1]** |

</div>

## __Metadata__

<div class="grid cards" markdown>

- ### Calculation Metadata

    | Property                   | Value                                                      |
    |----------------------------|------------------------------------------------------------|
    | **Method name** | DFT |
    | **Workflow name** | SinglePoint |
    | **Program name** | VASP |
    | **Program version** | 5.4.4.18Apr17-6-g9f103f2a35 complex parallel LinuxIFC |
    | **Basis set type** | plane waves |
    | **Core electron treatment** | pseudopotential |
    | **Jacob's ladder** | GGA |
    | **XC functional names** | GGA_C_PBE, GGA_X_PBE |
    | **Code-specific tier** | VASP - accurate |
    | **Basis set** | plane waves |
    | **Entry type** | VASP DFT SinglePoint |
    | **Entry name** | C428H42N8O8 VASP DFT SinglePoint simulation |
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
    const scfData = JSON.parse('[{"step": 1, "total_ev": 23536.445688, "free_ev": 23536.445688, "total_t0_ev": 23536.445688}, {"step": 2, "total_ev": 9360.34183158, "free_ev": 9360.34183158, "total_t0_ev": 9360.34183158}, {"step": 3, "total_ev": 4237.00816844, "free_ev": 4237.00816844, "total_t0_ev": 4237.00816844}, {"step": 4, "total_ev": -1402.05743773, "free_ev": -1402.05743773, "total_t0_ev": -1402.05743773}, {"step": 5, "total_ev": -3678.32075784, "free_ev": -3678.32075784, "total_t0_ev": -3678.32075784}, {"step": 6, "total_ev": -4276.13044916, "free_ev": -4276.13044916, "total_t0_ev": -4276.13044916}, {"step": 7, "total_ev": -4420.33254886, "free_ev": -4420.33254886, "total_t0_ev": -4420.33254886}, {"step": 8, "total_ev": -4465.25998318, "free_ev": -4465.25998318, "total_t0_ev": -4465.25998318}, {"step": 9, "total_ev": -4484.4407469, "free_ev": -4484.4407469, "total_t0_ev": -4484.4407469}, {"step": 10, "total_ev": -4487.27402134, "free_ev": -4487.27402134, "total_t0_ev": -4487.27402134}, {"step": 11, "total_ev": -4487.38885891, "free_ev": -4487.38885891, "total_t0_ev": -4487.38885891}, {"step": 12, "total_ev": -4487.40663269, "free_ev": -4487.40663269, "total_t0_ev": -4487.40663269}, {"step": 13, "total_ev": -4281.25336229, "free_ev": -4281.25336229, "total_t0_ev": -4281.25336229}, {"step": 14, "total_ev": -4211.80625336, "free_ev": -4211.80625336, "total_t0_ev": -4211.80625336}, {"step": 15, "total_ev": -4209.7724227, "free_ev": -4209.7724227, "total_t0_ev": -4209.7724227}, {"step": 16, "total_ev": -4209.14419515, "free_ev": -4209.14419515, "total_t0_ev": -4209.14419515}, {"step": 17, "total_ev": -4208.8051858, "free_ev": -4208.8051858, "total_t0_ev": -4208.8051858}, {"step": 18, "total_ev": -4208.72094278, "free_ev": -4208.72094278, "total_t0_ev": -4208.72094278}, {"step": 19, "total_ev": -4208.74086017, "free_ev": -4208.74086017, "total_t0_ev": -4208.74086017}, {"step": 20, "total_ev": -4208.77789868, "free_ev": -4208.77789868, "total_t0_ev": -4208.77789868}, {"step": 21, "total_ev": -4208.81131797, "free_ev": -4208.81131797, "total_t0_ev": -4208.81131797}, {"step": 22, "total_ev": -4208.85549137, "free_ev": -4208.85549137, "total_t0_ev": -4208.85549137}, {"step": 23, "total_ev": -4208.89082249, "free_ev": -4208.89082249, "total_t0_ev": -4208.89082249}, {"step": 24, "total_ev": -4208.9111405, "free_ev": -4208.9111405, "total_t0_ev": -4208.9111405}, {"step": 25, "total_ev": -4208.91708139, "free_ev": -4208.91708139, "total_t0_ev": -4208.91708139}, {"step": 26, "total_ev": -4208.92309493, "free_ev": -4208.92309493, "total_t0_ev": -4208.92309493}, {"step": 27, "total_ev": -4208.92698804, "free_ev": -4208.92698804, "total_t0_ev": -4208.92698804}, {"step": 28, "total_ev": -4208.92845233, "free_ev": -4208.92845233, "total_t0_ev": -4208.92845233}, {"step": 29, "total_ev": -4208.92989582, "free_ev": -4208.92989582, "total_t0_ev": -4208.92989582}, {"step": 30, "total_ev": -4208.93054947, "free_ev": -4208.93054947, "total_t0_ev": -4208.93054947}, {"step": 31, "total_ev": -4208.93071745, "free_ev": -4208.93071745, "total_t0_ev": -4208.93071745}, {"step": 32, "total_ev": -4208.93127719, "free_ev": -4208.93127719, "total_t0_ev": -4208.93127719}, {"step": 33, "total_ev": -4208.93141213, "free_ev": -4208.93141213, "total_t0_ev": -4208.93141213}, {"step": 34, "total_ev": -4208.93161842, "free_ev": -4208.93161842, "total_t0_ev": -4208.93161842}, {"step": 35, "total_ev": -4208.9315897, "free_ev": -4208.9315897, "total_t0_ev": -4208.9315897}, {"step": 36, "total_ev": -4208.93180914, "free_ev": -4208.93180914, "total_t0_ev": -4208.93180914}, {"step": 37, "total_ev": -4208.93184731, "free_ev": -4208.93184731, "total_t0_ev": -4208.93184731}, {"step": 38, "total_ev": -4208.93183431, "free_ev": -4208.93183431, "total_t0_ev": -4208.93183431}, {"step": 39, "total_ev": -4208.93186265, "free_ev": -4208.93186265, "total_t0_ev": -4208.93186265}, {"step": 40, "total_ev": -4208.93184377, "free_ev": -4208.93184377, "total_t0_ev": -4208.93184377}, {"step": 41, "total_ev": -4208.93187937, "free_ev": -4208.93187937, "total_t0_ev": -4208.93187937}, {"step": 42, "total_ev": -4208.93188922, "free_ev": -4208.93188922, "total_t0_ev": -4208.93188922}]');

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
    | **Total** | -4252.290045 |
    | **Free** | -4252.290045 |
    | **Total (T=0)** | 0.000000 |
    | **Band Gap** | 0.000100 |

- ### SCF Iteration Energies

    | Step | Total Energy (eV) | Free Energy (eV) | Total Energy (T=0) (eV) |
    |:---|---:|---:|---:|
| 1 | 23536.44569 | 23536.44569 | 23536.44569 |
| 2 | 9360.34183 | 9360.34183 | 9360.34183 |
| 3 | 4237.00817 | 4237.00817 | 4237.00817 |
| 4 | -1402.05744 | -1402.05744 | -1402.05744 |
| 5 | -3678.32076 | -3678.32076 | -3678.32076 |
| 6 | -4276.13045 | -4276.13045 | -4276.13045 |
| 7 | -4420.33255 | -4420.33255 | -4420.33255 |
| 8 | -4465.25998 | -4465.25998 | -4465.25998 |
| 9 | -4484.44075 | -4484.44075 | -4484.44075 |
| 10 | -4487.27402 | -4487.27402 | -4487.27402 |
| 11 | -4487.38886 | -4487.38886 | -4487.38886 |
| 12 | -4487.40663 | -4487.40663 | -4487.40663 |
| 13 | -4281.25336 | -4281.25336 | -4281.25336 |
| 14 | -4211.80625 | -4211.80625 | -4211.80625 |
| 15 | -4209.77242 | -4209.77242 | -4209.77242 |
| 16 | -4209.14420 | -4209.14420 | -4209.14420 |
| 17 | -4208.80519 | -4208.80519 | -4208.80519 |
| 18 | -4208.72094 | -4208.72094 | -4208.72094 |
| 19 | -4208.74086 | -4208.74086 | -4208.74086 |
| 20 | -4208.77790 | -4208.77790 | -4208.77790 |
| 21 | -4208.81132 | -4208.81132 | -4208.81132 |
| 22 | -4208.85549 | -4208.85549 | -4208.85549 |
| 23 | -4208.89082 | -4208.89082 | -4208.89082 |
| 24 | -4208.91114 | -4208.91114 | -4208.91114 |
| 25 | -4208.91708 | -4208.91708 | -4208.91708 |
| 26 | -4208.92309 | -4208.92309 | -4208.92309 |
| 27 | -4208.92699 | -4208.92699 | -4208.92699 |
| 28 | -4208.92845 | -4208.92845 | -4208.92845 |
| 29 | -4208.92990 | -4208.92990 | -4208.92990 |
| 30 | -4208.93055 | -4208.93055 | -4208.93055 |
| 31 | -4208.93072 | -4208.93072 | -4208.93072 |
| 32 | -4208.93128 | -4208.93128 | -4208.93128 |
| 33 | -4208.93141 | -4208.93141 | -4208.93141 |
| 34 | -4208.93162 | -4208.93162 | -4208.93162 |
| 35 | -4208.93159 | -4208.93159 | -4208.93159 |
| 36 | -4208.93181 | -4208.93181 | -4208.93181 |
| 37 | -4208.93185 | -4208.93185 | -4208.93185 |
| 38 | -4208.93183 | -4208.93183 | -4208.93183 |
| 39 | -4208.93186 | -4208.93186 | -4208.93186 |
| 40 | -4208.93184 | -4208.93184 | -4208.93184 |
| 41 | -4208.93188 | -4208.93188 | -4208.93188 |
| 42 | -4208.93189 | -4208.93189 | -4208.93189 |

</div>


<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
<div id="scf_chart_div" style="width: 100%; height: 500px; margin-bottom: 20px;"></div>
<script type="text/javascript">
  google.charts.load('current', {'packages':['corechart']});
  google.charts.setOnLoadCallback(drawChart);

  function drawChart() {
    // Parse the JSON data passed from Python
    const scfData = JSON.parse('[{"step": 1, "total_ev": 23536.445688, "free_ev": 23536.445688, "total_t0_ev": 23536.445688}, {"step": 2, "total_ev": 9360.34183158, "free_ev": 9360.34183158, "total_t0_ev": 9360.34183158}, {"step": 3, "total_ev": 4237.00816844, "free_ev": 4237.00816844, "total_t0_ev": 4237.00816844}, {"step": 4, "total_ev": -1402.05743773, "free_ev": -1402.05743773, "total_t0_ev": -1402.05743773}, {"step": 5, "total_ev": -3678.32075784, "free_ev": -3678.32075784, "total_t0_ev": -3678.32075784}, {"step": 6, "total_ev": -4276.13044916, "free_ev": -4276.13044916, "total_t0_ev": -4276.13044916}, {"step": 7, "total_ev": -4420.33254886, "free_ev": -4420.33254886, "total_t0_ev": -4420.33254886}, {"step": 8, "total_ev": -4465.25998318, "free_ev": -4465.25998318, "total_t0_ev": -4465.25998318}, {"step": 9, "total_ev": -4484.4407469, "free_ev": -4484.4407469, "total_t0_ev": -4484.4407469}, {"step": 10, "total_ev": -4487.27402134, "free_ev": -4487.27402134, "total_t0_ev": -4487.27402134}, {"step": 11, "total_ev": -4487.38885891, "free_ev": -4487.38885891, "total_t0_ev": -4487.38885891}, {"step": 12, "total_ev": -4487.40663269, "free_ev": -4487.40663269, "total_t0_ev": -4487.40663269}, {"step": 13, "total_ev": -4281.25336229, "free_ev": -4281.25336229, "total_t0_ev": -4281.25336229}, {"step": 14, "total_ev": -4211.80625336, "free_ev": -4211.80625336, "total_t0_ev": -4211.80625336}, {"step": 15, "total_ev": -4209.7724227, "free_ev": -4209.7724227, "total_t0_ev": -4209.7724227}, {"step": 16, "total_ev": -4209.14419515, "free_ev": -4209.14419515, "total_t0_ev": -4209.14419515}, {"step": 17, "total_ev": -4208.8051858, "free_ev": -4208.8051858, "total_t0_ev": -4208.8051858}, {"step": 18, "total_ev": -4208.72094278, "free_ev": -4208.72094278, "total_t0_ev": -4208.72094278}, {"step": 19, "total_ev": -4208.74086017, "free_ev": -4208.74086017, "total_t0_ev": -4208.74086017}, {"step": 20, "total_ev": -4208.77789868, "free_ev": -4208.77789868, "total_t0_ev": -4208.77789868}, {"step": 21, "total_ev": -4208.81131797, "free_ev": -4208.81131797, "total_t0_ev": -4208.81131797}, {"step": 22, "total_ev": -4208.85549137, "free_ev": -4208.85549137, "total_t0_ev": -4208.85549137}, {"step": 23, "total_ev": -4208.89082249, "free_ev": -4208.89082249, "total_t0_ev": -4208.89082249}, {"step": 24, "total_ev": -4208.9111405, "free_ev": -4208.9111405, "total_t0_ev": -4208.9111405}, {"step": 25, "total_ev": -4208.91708139, "free_ev": -4208.91708139, "total_t0_ev": -4208.91708139}, {"step": 26, "total_ev": -4208.92309493, "free_ev": -4208.92309493, "total_t0_ev": -4208.92309493}, {"step": 27, "total_ev": -4208.92698804, "free_ev": -4208.92698804, "total_t0_ev": -4208.92698804}, {"step": 28, "total_ev": -4208.92845233, "free_ev": -4208.92845233, "total_t0_ev": -4208.92845233}, {"step": 29, "total_ev": -4208.92989582, "free_ev": -4208.92989582, "total_t0_ev": -4208.92989582}, {"step": 30, "total_ev": -4208.93054947, "free_ev": -4208.93054947, "total_t0_ev": -4208.93054947}, {"step": 31, "total_ev": -4208.93071745, "free_ev": -4208.93071745, "total_t0_ev": -4208.93071745}, {"step": 32, "total_ev": -4208.93127719, "free_ev": -4208.93127719, "total_t0_ev": -4208.93127719}, {"step": 33, "total_ev": -4208.93141213, "free_ev": -4208.93141213, "total_t0_ev": -4208.93141213}, {"step": 34, "total_ev": -4208.93161842, "free_ev": -4208.93161842, "total_t0_ev": -4208.93161842}, {"step": 35, "total_ev": -4208.9315897, "free_ev": -4208.9315897, "total_t0_ev": -4208.9315897}, {"step": 36, "total_ev": -4208.93180914, "free_ev": -4208.93180914, "total_t0_ev": -4208.93180914}, {"step": 37, "total_ev": -4208.93184731, "free_ev": -4208.93184731, "total_t0_ev": -4208.93184731}, {"step": 38, "total_ev": -4208.93183431, "free_ev": -4208.93183431, "total_t0_ev": -4208.93183431}, {"step": 39, "total_ev": -4208.93186265, "free_ev": -4208.93186265, "total_t0_ev": -4208.93186265}, {"step": 40, "total_ev": -4208.93184377, "free_ev": -4208.93184377, "total_t0_ev": -4208.93184377}, {"step": 41, "total_ev": -4208.93187937, "free_ev": -4208.93187937, "total_t0_ev": -4208.93187937}, {"step": 42, "total_ev": -4208.93188922, "free_ev": -4208.93188922, "total_t0_ev": -4208.93188922}]');

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
    const dosData = JSON.parse('[{"energy_ev": -24.570914499999997, "dos": 0.0}, {"energy_ev": -24.456214499999998, "dos": 0.0}, {"energy_ev": -24.3414145, "dos": 0.0}, {"energy_ev": -24.2267145, "dos": 0.0}, {"energy_ev": -24.112014499999997, "dos": 0.0}, {"energy_ev": -23.997314499999998, "dos": 0.0}, {"energy_ev": -23.8825145, "dos": 0.0}, {"energy_ev": -23.7678145, "dos": 0.0}, {"energy_ev": -23.653114499999997, "dos": 0.0}, {"energy_ev": -23.538314499999995, "dos": 0.0}, {"energy_ev": -23.4236145, "dos": 0.0}, {"energy_ev": -23.3089145, "dos": 0.0}, {"energy_ev": -23.194214499999998, "dos": 0.0}, {"energy_ev": -23.079414500000002, "dos": 0.0}, {"energy_ev": -22.9647145, "dos": 0.0}, {"energy_ev": -22.850014499999997, "dos": 0.0}, {"energy_ev": -22.735214499999998, "dos": 0.0}, {"energy_ev": -22.6205145, "dos": 0.0}, {"energy_ev": -22.5058145, "dos": 0.0}, {"energy_ev": -22.391114499999997, "dos": 0.0}, {"energy_ev": -22.276314499999998, "dos": 0.0}, {"energy_ev": -22.1616145, "dos": 0.0}, {"energy_ev": -22.0469145, "dos": 0.0}, {"energy_ev": -21.932214500000004, "dos": 0.0}, {"energy_ev": -21.817414499999995, "dos": 0.0}, {"energy_ev": -21.7027145, "dos": 0.0}, {"energy_ev": -21.5880145, "dos": 0.0}, {"energy_ev": -21.473214499999997, "dos": 0.0}, {"energy_ev": -21.358514499999995, "dos": 0.0}, {"energy_ev": -21.2438145, "dos": 0.0}, {"energy_ev": -21.1291145, "dos": 0.0}, {"energy_ev": -21.014314499999998, "dos": 0.0}, {"energy_ev": -20.899614500000002, "dos": 0.0}, {"energy_ev": -20.7849145, "dos": 0.0}, {"energy_ev": -20.670114500000004, "dos": 0.0}, {"energy_ev": -20.555414499999998, "dos": 0.0}, {"energy_ev": -20.4407145, "dos": 0.0}, {"energy_ev": -20.3260145, "dos": 0.0}, {"energy_ev": -20.2112145, "dos": 0.0}, {"energy_ev": -20.096514499999998, "dos": 0.0}, {"energy_ev": -19.9818145, "dos": 0.0}, {"energy_ev": -19.8670145, "dos": 0.0}, {"energy_ev": -19.7523145, "dos": 0.0}, {"energy_ev": -19.637614499999994, "dos": 0.0}, {"energy_ev": -19.5229145, "dos": 0.0}, {"energy_ev": -19.408114499999996, "dos": 0.0}, {"energy_ev": -19.293414499999997, "dos": 2.2339546864219216e+20}, {"energy_ev": -19.178714499999995, "dos": 8.719731460020782e+20}, {"energy_ev": -19.0640145, "dos": 1.1566121741356017e+21}, {"energy_ev": -18.949214499999997, "dos": 5.2017922513280146e+20}, {"energy_ev": -18.834514499999997, "dos": 6.49513903721055e+20}, {"energy_ev": -18.719814500000002, "dos": 5.512269878727991e+20}, {"energy_ev": -18.6050145, "dos": 1.2101037793564528e+20}, {"energy_ev": -18.490314500000004, "dos": 1.901862713097088e+20}, {"energy_ev": -18.375614499999998, "dos": 2.1107722633283643e+20}, {"energy_ev": -18.260914500000002, "dos": 4.553574084890818e+20}, {"energy_ev": -18.1461145, "dos": 1.5450730883646128e+20}, {"energy_ev": -18.0314145, "dos": 2.5753901988312236e+20}, {"energy_ev": -17.9167145, "dos": 4.702184415953728e+20}, {"energy_ev": -17.8019145, "dos": 4.797011663322011e+20}, {"energy_ev": -17.687214500000003, "dos": 5.2468559468456215e+20}, {"energy_ev": -17.5725145, "dos": 1.7139558409013723e+20}, {"energy_ev": -17.4578145, "dos": 5.498176551237859e+20}, {"energy_ev": -17.3430145, "dos": 1.6240281781565417e+20}, {"energy_ev": -17.228314500000003, "dos": 1.0979569684574492e+21}, {"energy_ev": -17.1136145, "dos": 0.0}, {"energy_ev": -16.998814499999998, "dos": 5.5604106382193066e+20}, {"energy_ev": -16.8841145, "dos": 2.326559956559696e+20}, {"energy_ev": -16.769414500000003, "dos": 4.6465413625549115e+20}, {"energy_ev": -16.6547145, "dos": 3.580011016438279e+20}, {"energy_ev": -16.5399145, "dos": 1.0277955408005282e+20}, {"energy_ev": -16.4252145, "dos": 5.4163191597263054e+20}, {"energy_ev": -16.310514500000004, "dos": 1.7097428222761114e+20}, {"energy_ev": -16.1957145, "dos": 1.0731775532809324e+20}, {"energy_ev": -16.0810145, "dos": 4.2400755670988023e+20}, {"energy_ev": -15.966314499999998, "dos": 3.857177709907858e+20}, {"energy_ev": -15.851614500000002, "dos": 2.0713196844686977e+20}, {"energy_ev": -15.7368145, "dos": 2.238267569192374e+20}, {"energy_ev": -15.622114499999999, "dos": 1.1036336209606712e+21}, {"energy_ev": -15.507414500000003, "dos": 3.1375878872042026e+20}, {"energy_ev": -15.392714500000002, "dos": 6.542967721248143e+20}, {"energy_ev": -15.2779145, "dos": 8.578236449302757e+20}, {"energy_ev": -15.163214499999999, "dos": 3.042517220982016e+20}, {"energy_ev": -15.048514500000003, "dos": 8.719188448731302e+20}, {"energy_ev": -14.9337145, "dos": 4.131030162058899e+20}, {"energy_ev": -14.8190145, "dos": 4.28826001715364e+20}, {"energy_ev": -14.704314499999999, "dos": 3.1455270867469166e+20}, {"energy_ev": -14.589614500000001, "dos": 4.134843724103394e+20}, {"energy_ev": -14.4748145, "dos": 5.95230250998655e+20}, {"energy_ev": -14.3601145, "dos": 4.235394435292957e+20}, {"energy_ev": -14.245414499999999, "dos": 8.46856065184633e+20}, {"energy_ev": -14.130614500000002, "dos": 6.54844776621552e+20}, {"energy_ev": -14.015914500000001, "dos": 4.8862652430868e+20}, {"energy_ev": -13.9012145, "dos": 1.8239125062661476e+20}, {"energy_ev": -13.786514499999997, "dos": 2.566121557855649e+20}, {"energy_ev": -13.6717145, "dos": 3.305334685089409e+20}, {"energy_ev": -13.5570145, "dos": 1.7671584642520757e+20}, {"energy_ev": -13.442314499999998, "dos": 2.885206226269307e+20}, {"energy_ev": -13.327514500000001, "dos": 5.890112113568622e+19}, {"energy_ev": -13.2128145, "dos": 8.857637603020992e+19}, {"energy_ev": -13.0981145, "dos": 5.3482055711967157e+20}, {"energy_ev": -12.983414499999999, "dos": 1.8757794466749166e+20}, {"energy_ev": -12.868614500000001, "dos": 1.2718797395718358e+21}, {"energy_ev": -12.7539145, "dos": 4.0241568021769073e+20}, {"energy_ev": -12.6392145, "dos": 1.5393184169979603e+20}, {"energy_ev": -12.524414499999997, "dos": 2.55025564178837e+20}, {"energy_ev": -12.409714500000002, "dos": 2.36066356214255e+20}, {"energy_ev": -12.2950145, "dos": 6.023050015345562e+20}, {"energy_ev": -12.1803145, "dos": 2.3283974568312177e+21}, {"energy_ev": -12.065514500000003, "dos": 4.0714986485066924e+20}, {"energy_ev": -11.950814500000002, "dos": 2.952015339402335e+20}, {"energy_ev": -11.8361145, "dos": 4.18361487601123e+20}, {"energy_ev": -11.7214145, "dos": 2.35134498909438e+20}, {"energy_ev": -11.606614500000003, "dos": 2.7758986778482757e+20}, {"energy_ev": -11.491914500000002, "dos": 4.991971440771867e+20}, {"energy_ev": -11.3772145, "dos": 2.778638700331964e+20}, {"energy_ev": -11.262414499999998, "dos": 3.542449614828174e+20}, {"energy_ev": -11.147714500000001, "dos": 5.0251637860298496e+20}, {"energy_ev": -11.0330145, "dos": 2.683942524654245e+20}, {"energy_ev": -10.9183145, "dos": 2.737694400803501e+20}, {"energy_ev": -10.803514499999999, "dos": 6.656388424149244e+20}, {"energy_ev": -10.688814500000001, "dos": 1.731819039872479e+20}, {"energy_ev": -10.574114499999999, "dos": 2.3822903910855564e+20}, {"energy_ev": -10.4593145, "dos": 5.4509096030169675e+20}, {"energy_ev": -10.344614499999999, "dos": 5.8329710979919335e+20}, {"energy_ev": -10.2299145, "dos": 3.014923509363825e+20}, {"energy_ev": -10.115214499999999, "dos": 6.199672239134652e+20}, {"energy_ev": -10.000414500000002, "dos": 2.911262030051551e+21}, {"energy_ev": -9.8857145, "dos": 2.6686945179853373e+20}, {"energy_ev": -9.7710145, "dos": 3.7754076995233474e+20}, {"energy_ev": -9.6562145, "dos": 9.674719797467725e+20}, {"energy_ev": -9.541514500000002, "dos": 6.030414996053426e+20}, {"energy_ev": -9.4268145, "dos": 4.920468712814844e+20}, {"energy_ev": -9.312114500000002, "dos": 2.0921351172320245e+20}, {"energy_ev": -9.197314500000001, "dos": 4.554410447106796e+20}, {"energy_ev": -9.082614499999998, "dos": 5.749284944321564e+20}, {"energy_ev": -8.967914500000001, "dos": 2.42906800499501e+21}, {"energy_ev": -8.8532145, "dos": 9.525422900406624e+20}, {"energy_ev": -8.7384145, "dos": 3.8662154150476775e+20}, {"energy_ev": -8.623714499999998, "dos": 4.461062437389161e+20}, {"energy_ev": -8.509014500000001, "dos": 6.652468756450483e+20}, {"energy_ev": -8.3942145, "dos": 7.383056118143338e+20}, {"energy_ev": -8.2795145, "dos": 7.65210884981612e+20}, {"energy_ev": -8.164814499999999, "dos": 6.101075120285397e+20}, {"energy_ev": -8.0501145, "dos": 5.0501610298730643e+20}, {"energy_ev": -7.9353145000000005, "dos": 3.853751121425979e+20}, {"energy_ev": -7.8206145000000005, "dos": 6.707737319304833e+20}, {"energy_ev": -7.7059145, "dos": 8.180827083513691e+20}, {"energy_ev": -7.5911145000000015, "dos": 6.921047133433604e+20}, {"energy_ev": -7.476414500000001, "dos": 3.1917953935158936e+20}, {"energy_ev": -7.361714500000001, "dos": 7.184694718247902e+20}, {"energy_ev": -7.2470145, "dos": 4.892007431435304e+20}, {"energy_ev": -7.132214500000001, "dos": 1.3471092725972187e+21}, {"energy_ev": -7.0175145, "dos": 5.981899746017642e+20}, {"energy_ev": -6.902814500000002, "dos": 1.3605703352181082e+21}, {"energy_ev": -6.788014500000001, "dos": 2.1797346970920815e+21}, {"energy_ev": -6.6733145, "dos": 1.1356481934563029e+21}, {"energy_ev": -6.5586145, "dos": 1.243696205346108e+21}, {"energy_ev": -6.443914499999999, "dos": 1.213992863660749e+21}, {"energy_ev": -6.3291145, "dos": 1.094608398839001e+21}, {"energy_ev": -6.214414499999999, "dos": 8.916114301539615e+20}, {"energy_ev": -6.099714500000001, "dos": 8.726434840766753e+20}, {"energy_ev": -5.9849145, "dos": 1.2562366453785145e+21}, {"energy_ev": -5.8702145, "dos": 7.852735917505586e+20}, {"energy_ev": -5.755514499999999, "dos": 1.8505082005833324e+21}, {"energy_ev": -5.6408145, "dos": 1.2597038036693774e+21}, {"energy_ev": -5.5260145, "dos": 1.0075842861156094e+21}, {"energy_ev": -5.411314500000001, "dos": 7.588414249711247e+20}, {"energy_ev": -5.2966145000000004, "dos": 4.1704764994094904e+20}, {"energy_ev": -5.1819145, "dos": 7.038162809706786e+20}, {"energy_ev": -5.0671145, "dos": 5.248297735441822e+20}, {"energy_ev": -4.9524145, "dos": 7.460513245757397e+20}, {"energy_ev": -4.8377145, "dos": 5.816143989527187e+20}, {"energy_ev": -4.722914500000001, "dos": 1.3912248828864147e+21}, {"energy_ev": -4.608214500000001, "dos": 5.7466135784376946e+20}, {"energy_ev": -4.4935145, "dos": 7.525531045786055e+20}, {"energy_ev": -4.3788145, "dos": 9.94047701234919e+20}, {"energy_ev": -4.2640145, "dos": 9.095738691193522e+20}, {"energy_ev": -4.1493145, "dos": 9.65510897595577e+20}, {"energy_ev": -4.034614500000001, "dos": 7.444191699527682e+20}, {"energy_ev": -3.9198144999999998, "dos": 5.802674812944501e+20}, {"energy_ev": -3.8051145, "dos": 4.855113871296166e+20}, {"energy_ev": -3.6904145, "dos": 5.6182569443214085e+20}, {"energy_ev": -3.5757145, "dos": 4.157675164297771e+20}, {"energy_ev": -3.460914500000001, "dos": 5.149644443010895e+20}, {"energy_ev": -3.346214500000001, "dos": 4.083251410093902e+20}, {"energy_ev": -3.2315145, "dos": 5.5401444582545326e+20}, {"energy_ev": -3.116714499999999, "dos": 5.279005960088169e+20}, {"energy_ev": -3.0020144999999996, "dos": 4.506719076268841e+20}, {"energy_ev": -2.8873144999999996, "dos": 5.0943696386474705e+20}, {"energy_ev": -2.7726144999999995, "dos": 5.1638064271008465e+20}, {"energy_ev": -2.6578145, "dos": 1.1188947347986351e+21}, {"energy_ev": -2.5431145000000006, "dos": 1.4663489344084393e+21}, {"energy_ev": -2.4284145, "dos": 4.6189850999911665e+20}, {"energy_ev": -2.3136145, "dos": 6.529773171064734e+20}, {"energy_ev": -2.1989145, "dos": 1.3470281329792506e+21}, {"energy_ev": -2.0842145000000003, "dos": 5.286414631359554e+20}, {"energy_ev": -1.9695145000000003, "dos": 2.8712252459425146e+20}, {"energy_ev": -1.8547145000000003, "dos": 3.302482315442381e+20}, {"energy_ev": -1.7400145000000005, "dos": 3.343420373461769e+20}, {"energy_ev": -1.6253145, "dos": 4.20642135016931e+20}, {"energy_ev": -1.5106145, "dos": 2.2841801099441078e+20}, {"energy_ev": -1.3958145000000006, "dos": 8.29354873739845e+20}, {"energy_ev": -1.2811145000000002, "dos": 1.8843552801432257e+20}, {"energy_ev": -1.1664145000000004, "dos": 2.5464171137075764e+20}, {"energy_ev": -1.0516145000000008, "dos": 1.6070824810193807e+20}, {"energy_ev": -0.9369145000000004, "dos": 1.2080628058891041e+20}, {"energy_ev": -0.8222145, "dos": 1.2206519296922914e+20}, {"energy_ev": -0.7075145, "dos": 5.345727692094154e+19}, {"energy_ev": -0.5927145, "dos": 0.0}, {"energy_ev": -0.4780145000000001, "dos": 1.1175297167640509e+20}, {"energy_ev": -0.36331450000000026, "dos": 1.9312789453650215e+20}, {"energy_ev": -0.24851450000000022, "dos": 2.708440447771504e+19}, {"energy_ev": -0.13381449999999975, "dos": 1.439291992570652e+19}, {"energy_ev": -0.0191144999999999, "dos": 1.701435373698004e+18}, {"energy_ev": 0.09558549999999937, "dos": 5.664793635980588e+18}, {"energy_ev": 0.2103855, "dos": 1.9662626037273743e+19}, {"energy_ev": 0.32508549999999986, "dos": 3.3660458438566896e+19}, {"energy_ev": 0.43978550000000005, "dos": 1.0804239453163817e+20}, {"energy_ev": 0.5545854999999997, "dos": 3.067598725197736e+21}, {"energy_ev": 0.6692854999999996, "dos": 0.0}, {"energy_ev": 0.7839854999999998, "dos": 1.014326364217842e+20}, {"energy_ev": 0.8986854999999997, "dos": 6.625174637267866e+19}, {"energy_ev": 1.0134854999999998, "dos": 1.8474117879314924e+20}, {"energy_ev": 1.1281854999999998, "dos": 7.53249032840408e+20}, {"energy_ev": 1.2428854999999996, "dos": 1.818526083934888e+20}, {"energy_ev": 1.3575855, "dos": 4.898117868819201e+20}, {"energy_ev": 1.4723855, "dos": 2.8903991618192582e+20}, {"energy_ev": 1.5870855, "dos": 2.5876922132169857e+20}, {"energy_ev": 1.7017855, "dos": 1.1829969054460698e+21}, {"energy_ev": 1.8165855, "dos": 1.920543549756949e+20}, {"energy_ev": 1.9312855, "dos": 4.223679122760194e+20}, {"energy_ev": 2.0459854999999996, "dos": 2.7783328663873153e+20}, {"energy_ev": 2.1606855, "dos": 4.075630527513985e+20}, {"energy_ev": 2.2754855, "dos": 3.089234916404355e+20}, {"energy_ev": 2.3901855, "dos": 2.7395231629623185e+20}, {"energy_ev": 2.5048855, "dos": 9.964450648704194e+20}, {"energy_ev": 2.6196855, "dos": 5.682681800987993e+20}, {"energy_ev": 2.7343854999999997, "dos": 2.196629838005739e+21}, {"energy_ev": 2.8490854999999997, "dos": 5.1820253920891974e+20}, {"energy_ev": 2.9637854999999997, "dos": 4.6884780620262126e+20}, {"energy_ev": 3.0785854999999995, "dos": 4.459015222412737e+20}, {"energy_ev": 3.1932855, "dos": 2.888676505314707e+20}, {"energy_ev": 3.3079855, "dos": 3.252338031538163e+20}, {"energy_ev": 3.4227855000000003, "dos": 4.4360964010913176e+20}, {"energy_ev": 3.5374855, "dos": 5.250357433436394e+20}, {"energy_ev": 3.6521855, "dos": 3.490357980092725e+20}, {"energy_ev": 3.7668855000000003, "dos": 4.452967200119584e+20}, {"energy_ev": 3.8816854999999997, "dos": 7.178259722392131e+20}, {"energy_ev": 3.9963855, "dos": 5.375849214887502e+20}, {"energy_ev": 4.1110855, "dos": 8.512363562530898e+20}, {"energy_ev": 4.2258855, "dos": 5.638716611067492e+20}, {"energy_ev": 4.3405854999999995, "dos": 1.3295912290779296e+21}, {"energy_ev": 4.4552855, "dos": 7.778792759500449e+20}, {"energy_ev": 4.5699855, "dos": 1.6513166799809916e+21}, {"energy_ev": 4.684785499999999, "dos": 2.004775835471334e+21}, {"energy_ev": 4.7994855, "dos": 8.02636845844801e+20}, {"energy_ev": 4.9141855, "dos": 1.530553465804695e+21}, {"energy_ev": 5.0288854999999995, "dos": 1.5261226185127352e+21}, {"energy_ev": 5.1436855, "dos": 1.329858989817224e+21}, {"energy_ev": 5.2583855, "dos": 9.674981940848853e+20}, {"energy_ev": 5.3730855, "dos": 1.349980990922378e+21}, {"energy_ev": 5.4878855, "dos": 1.1791265456689966e+21}, {"energy_ev": 5.6025855, "dos": 1.4145518989013043e+21}, {"energy_ev": 5.717285499999999, "dos": 3.0530091977361845e+21}, {"energy_ev": 5.831985500000001, "dos": 2.069779280029121e+21}, {"energy_ev": 5.9467855, "dos": 1.869144722528765e+21}, {"energy_ev": 6.0614855, "dos": 2.004470625677593e+21}, {"energy_ev": 6.1761855, "dos": 4.4669981125189724e+20}, {"energy_ev": 6.290985499999999, "dos": 2.683184181301698e+21}, {"energy_ev": 6.405685500000001, "dos": 1.5748875289114973e+21}, {"energy_ev": 6.5203855, "dos": 1.5488254836201787e+21}, {"energy_ev": 6.6350855, "dos": 2.0217808269447028e+21}, {"energy_ev": 6.7498854999999995, "dos": 1.8955413127064744e+21}, {"energy_ev": 6.8645855000000005, "dos": 1.3948187438114894e+21}, {"energy_ev": 6.9792855000000005, "dos": 2.0595407085433756e+21}, {"energy_ev": 7.094085500000001, "dos": 2.2332924623091217e+21}, {"energy_ev": 7.208785499999999, "dos": 2.3529989889991123e+21}, {"energy_ev": 7.3234855, "dos": 3.648200751378578e+21}, {"energy_ev": 7.4381854999999995, "dos": 2.160409736695736e+21}, {"energy_ev": 7.5529855, "dos": 1.2179318800376414e+21}, {"energy_ev": 7.6676855, "dos": 3.422075870818124e+20}, {"energy_ev": 7.782385499999999, "dos": 1.377020456534757e+20}, {"energy_ev": 7.897085499999999, "dos": 0.0}, {"energy_ev": 8.011885499999998, "dos": 0.0}, {"energy_ev": 8.126585500000001, "dos": 0.0}, {"energy_ev": 8.2412855, "dos": 0.0}, {"energy_ev": 8.356085499999999, "dos": 0.0}, {"energy_ev": 8.4707855, "dos": 0.0}, {"energy_ev": 8.585485499999999, "dos": 0.0}, {"energy_ev": 8.7001855, "dos": 0.0}, {"energy_ev": 8.814985499999999, "dos": 0.0}, {"energy_ev": 8.9296855, "dos": 0.0}, {"energy_ev": 9.044385499999999, "dos": 0.0}, {"energy_ev": 9.1591855, "dos": 0.0}, {"energy_ev": 9.2738855, "dos": 0.0}, {"energy_ev": 9.3885855, "dos": 0.0}, {"energy_ev": 9.5032855, "dos": 0.0}, {"energy_ev": 9.6180855, "dos": 0.0}, {"energy_ev": 9.7327855, "dos": 0.0}, {"energy_ev": 9.8474855, "dos": 0.0}]');
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


