
# __Si VASP GW SinglePoint simulation__

<div class="grid cards" markdown>

{{ structure_viewer("fair-structure.json") }}

- ### Material Composition - original

    | Property                     | Value                       |
    |------------------------------|-----------------------------|
    | Chemical formula (IUPAC) | **Si** |
    | Chemical formula (Reduced) | **Si** |
    | Label | **original** |
    | Elements | **Si** |
    | Number of elements | **1** |
    | Number of atoms | **2** |
    | Dimensionality | **3D** |

</div>

## __Structural information__

<div class="grid cards" markdown>

- ### Lattice (original)

    | Lattice constant | Value     | Units |
    |------------------|-----------|-------|
    | a | **3.867** | Angstrom |
    | b | **3.867** | Angstrom |
    | c | **3.867** | Angstrom |

    | Lattice angles    | Value     | Units |
    |------------------|-----------|-------|
    | Alpha | **60** | Degrees |
    | Beta | **60** | Degrees |
    | Gamma | **60** | Degrees |

    | Cell quantities   | Value     | Units |
    |------------------|-----------|-------|
    | Volume | **40.892** | Å³ |
    | Mass density | **2.281e-27** | kg / Å³ |
    | Atomic density | **0.049** | Å⁻³ |

- ### Lattice (conventional cell)

    | Lattice constant | Value     | Units |
    |------------------|-----------|-------|
    | a | **5.469** | Angstrom |
    | b | **5.469** | Angstrom |
    | c | **5.469** | Angstrom |

    | Lattice angles    | Value     | Units |
    |------------------|-----------|-------|
    | Alpha | **90** | Degrees |
    | Beta | **90** | Degrees |
    | Gamma | **90** | Degrees |

    | Cell quantities   | Value     | Units |
    |------------------|-----------|-------|
    | Volume | **163.568** | Å³ |
    | Mass density | **2.281e-27** | kg / Å³ |
    | Atomic density | **0.049** | Å⁻³ |

- ### Symmetry (conventional cell)

    | Property                       | Value            |
    |---------------------------------|------------------|
    | Crystal system | **cubic** |
    | Bravais lattice | **cF** |
    | Space group symbol | **Fd-3m** |
    | Space group number | **227** |
    | Point group | **m-3m** |
    | Hall number | **525** |
    | Hall symbol | **F 4d 2 3 -1d** |
    | Prototype name | **diamond** |
    | Prototype label aflow | **A_cF8_227_a** |

- ### K points information

    | Property               | Value |
    |------------------------|--------|
    | Dimensionality | **3** |
    | Sampling method | **Gamma-centered** |
    | Number of points | **216** |
    | Grid | **[6, 6, 6]** |

</div>

## __Metadata__

<div class="grid cards" markdown>

- ### Calculation Metadata

    | Property                   | Value                                                      |
    |----------------------------|------------------------------------------------------------|
    | **Method name** | GW |
    | **Workflow name** | SinglePoint |
    | **Program name** | VASP |
    | **Program version** | 6.1.0 28Jan20 complex parallel ARA Cluster |
    | **Entry type** | VASP GW SinglePoint |
    | **Entry name** | Si VASP GW SinglePoint simulation |
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
    const scfData = JSON.parse('[{"step": 1, "total_ev": NaN, "free_ev": NaN, "total_t0_ev": NaN}, {"step": 2, "total_ev": NaN, "free_ev": NaN, "total_t0_ev": NaN}, {"step": 3, "total_ev": NaN, "free_ev": NaN, "total_t0_ev": NaN}, {"step": 4, "total_ev": NaN, "free_ev": NaN, "total_t0_ev": NaN}]');

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
    | **Band Gap** | 1.720600 |

- ### SCF Iteration Energies

    | Step | Total Energy (eV) | Free Energy (eV) | Total Energy (T=0) (eV) |
    |:---|---:|---:|---:|
| 1 | N/A | N/A | N/A |
| 2 | N/A | N/A | N/A |
| 3 | N/A | N/A | N/A |
| 4 | N/A | N/A | N/A |

</div>


<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
<div id="scf_chart_div" style="width: 100%; height: 500px; margin-bottom: 20px;"></div>
<script type="text/javascript">
  google.charts.load('current', {'packages':['corechart']});
  google.charts.setOnLoadCallback(drawChart);

  function drawChart() {
    // Parse the JSON data passed from Python
    const scfData = JSON.parse('[{"step": 1, "total_ev": NaN, "free_ev": NaN, "total_t0_ev": NaN}, {"step": 2, "total_ev": NaN, "free_ev": NaN, "total_t0_ev": NaN}, {"step": 3, "total_ev": NaN, "free_ev": NaN, "total_t0_ev": NaN}, {"step": 4, "total_ev": NaN, "free_ev": NaN, "total_t0_ev": NaN}]');

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
    const dosData = JSON.parse('[{"energy_ev": -162.97722256999998, "dos": 0.0}, {"energy_ev": -162.16842257, "dos": 0.0}, {"energy_ev": -161.35952257, "dos": 0.0}, {"energy_ev": -160.55072257, "dos": 0.0}, {"energy_ev": -159.74192256999999, "dos": 0.0}, {"energy_ev": -158.93312257, "dos": 0.0}, {"energy_ev": -158.12432257, "dos": 0.0}, {"energy_ev": -157.31542256999998, "dos": 0.0}, {"energy_ev": -156.50662257, "dos": 0.0}, {"energy_ev": -155.69782257, "dos": 0.0}, {"energy_ev": -154.88902256999998, "dos": 0.0}, {"energy_ev": -154.08022257, "dos": 0.0}, {"energy_ev": -153.27132257, "dos": 0.0}, {"energy_ev": -152.46252257, "dos": 0.0}, {"energy_ev": -151.65372256999999, "dos": 3.0867383127745704e+19}, {"energy_ev": -150.84492257, "dos": 0.0}, {"energy_ev": -150.03612257, "dos": 0.0}, {"energy_ev": -149.22722256999998, "dos": 0.0}, {"energy_ev": -148.41842257, "dos": 0.0}, {"energy_ev": -147.60962257, "dos": 0.0}, {"energy_ev": -146.80082256999998, "dos": 0.0}, {"energy_ev": -145.99202257, "dos": 0.0}, {"energy_ev": -145.18312257, "dos": 0.0}, {"energy_ev": -144.37432257, "dos": 0.0}, {"energy_ev": -143.56552256999998, "dos": 0.0}, {"energy_ev": -142.75672257, "dos": 0.0}, {"energy_ev": -141.94792257, "dos": 0.0}, {"energy_ev": -141.13902256999998, "dos": 0.0}, {"energy_ev": -140.33022257, "dos": 0.0}, {"energy_ev": -139.52142257, "dos": 0.0}, {"energy_ev": -138.71262256999998, "dos": 0.0}, {"energy_ev": -137.90382257, "dos": 0.0}, {"energy_ev": -137.09492257, "dos": 0.0}, {"energy_ev": -136.28612257, "dos": 0.0}, {"energy_ev": -135.47732256999998, "dos": 0.0}, {"energy_ev": -134.66852257, "dos": 0.0}, {"energy_ev": -133.85972257, "dos": 0.0}, {"energy_ev": -133.05082256999998, "dos": 0.0}, {"energy_ev": -132.24202257, "dos": 0.0}, {"energy_ev": -131.43322257, "dos": 0.0}, {"energy_ev": -130.62442256999998, "dos": 0.0}, {"energy_ev": -129.81562257, "dos": 0.0}, {"energy_ev": -129.00672257, "dos": 0.0}, {"energy_ev": -128.19792257, "dos": 0.0}, {"energy_ev": -127.38912257, "dos": 0.0}, {"energy_ev": -126.58032256999999, "dos": 0.0}, {"energy_ev": -125.77152256999999, "dos": 0.0}, {"energy_ev": -124.96262256999998, "dos": 0.0}, {"energy_ev": -124.15382256999999, "dos": 0.0}, {"energy_ev": -123.34502257000001, "dos": 0.0}, {"energy_ev": -122.53622256999999, "dos": 0.0}, {"energy_ev": -121.72742256999999, "dos": 0.0}, {"energy_ev": -120.91852257, "dos": 0.0}, {"energy_ev": -120.10972256999997, "dos": 0.0}, {"energy_ev": -119.30092257, "dos": 0.0}, {"energy_ev": -118.49212257, "dos": 0.0}, {"energy_ev": -117.68332256999999, "dos": 0.0}, {"energy_ev": -116.87442257, "dos": 0.0}, {"energy_ev": -116.06562256999999, "dos": 0.0}, {"energy_ev": -115.25682257, "dos": 0.0}, {"energy_ev": -114.44802256999999, "dos": 0.0}, {"energy_ev": -113.63922257, "dos": 0.0}, {"energy_ev": -112.83032256999999, "dos": 0.0}, {"energy_ev": -112.02152256999999, "dos": 0.0}, {"energy_ev": -111.21272257, "dos": 0.0}, {"energy_ev": -110.40392256999999, "dos": 0.0}, {"energy_ev": -109.59512256999999, "dos": 0.0}, {"energy_ev": -108.78622256999998, "dos": 0.0}, {"energy_ev": -107.97742256999999, "dos": 0.0}, {"energy_ev": -107.16862257000001, "dos": 0.0}, {"energy_ev": -106.35982256999999, "dos": 0.0}, {"energy_ev": -105.55102256999999, "dos": 0.0}, {"energy_ev": -104.74212256999999, "dos": 0.0}, {"energy_ev": -103.93332256999997, "dos": 0.0}, {"energy_ev": -103.12452257, "dos": 0.0}, {"energy_ev": -102.31572257, "dos": 0.0}, {"energy_ev": -101.50692256999999, "dos": 0.0}, {"energy_ev": -100.69802256999999, "dos": 0.0}, {"energy_ev": -99.88922256999999, "dos": 9.260090108142222e+19}, {"energy_ev": -99.08042257, "dos": 0.0}, {"energy_ev": -98.27162256999999, "dos": 0.0}, {"energy_ev": -97.46282257, "dos": 0.0}, {"energy_ev": -96.65392256999999, "dos": 0.0}, {"energy_ev": -95.84512256999999, "dos": 0.0}, {"energy_ev": -95.03632256999998, "dos": 0.0}, {"energy_ev": -94.22752256999999, "dos": 0.0}, {"energy_ev": -93.41872256999999, "dos": 0.0}, {"energy_ev": -92.60982256999998, "dos": 0.0}, {"energy_ev": -91.80102256999999, "dos": 0.0}, {"energy_ev": -90.99222257, "dos": 0.0}, {"energy_ev": -90.18342256999999, "dos": 0.0}, {"energy_ev": -89.37462256999999, "dos": 0.0}, {"energy_ev": -88.56572256999999, "dos": 0.0}, {"energy_ev": -87.75692257, "dos": 0.0}, {"energy_ev": -86.94812257, "dos": 0.0}, {"energy_ev": -86.13932257, "dos": 0.0}, {"energy_ev": -85.33052257, "dos": 0.0}, {"energy_ev": -84.52172257000001, "dos": 0.0}, {"energy_ev": -83.71282256999999, "dos": 0.0}, {"energy_ev": -82.90402257, "dos": 0.0}, {"energy_ev": -82.09522257, "dos": 0.0}, {"energy_ev": -81.28642257, "dos": 0.0}, {"energy_ev": -80.47762257000001, "dos": 0.0}, {"energy_ev": -79.66872257, "dos": 0.0}, {"energy_ev": -78.85992257000001, "dos": 0.0}, {"energy_ev": -78.05112256999999, "dos": 0.0}, {"energy_ev": -77.24232257, "dos": 0.0}, {"energy_ev": -76.43352257000001, "dos": 0.0}, {"energy_ev": -75.62462256999999, "dos": 0.0}, {"energy_ev": -74.81582257, "dos": 0.0}, {"energy_ev": -74.00702257, "dos": 0.0}, {"energy_ev": -73.19822257, "dos": 0.0}, {"energy_ev": -72.38942257000001, "dos": 0.0}, {"energy_ev": -71.58052257, "dos": 0.0}, {"energy_ev": -70.77172257000001, "dos": 0.0}, {"energy_ev": -69.96292256999999, "dos": 0.0}, {"energy_ev": -69.15412257, "dos": 0.0}, {"energy_ev": -68.34532257000001, "dos": 0.0}, {"energy_ev": -67.53642257, "dos": 0.0}, {"energy_ev": -66.72762257, "dos": 0.0}, {"energy_ev": -65.91882257, "dos": 0.0}, {"energy_ev": -65.11002257, "dos": 0.0}, {"energy_ev": -64.30122257000001, "dos": 0.0}, {"energy_ev": -63.492322570000006, "dos": 0.0}, {"energy_ev": -62.68352257000001, "dos": 0.0}, {"energy_ev": -61.874722569999996, "dos": 0.0}, {"energy_ev": -61.065922570000005, "dos": 0.0}, {"energy_ev": -60.25712257000001, "dos": 0.0}, {"energy_ev": -59.44822257, "dos": 0.0}, {"energy_ev": -58.63942257, "dos": 0.0}, {"energy_ev": -57.83062257, "dos": 0.0}, {"energy_ev": -57.02182257, "dos": 0.0}, {"energy_ev": -56.21302257, "dos": 0.0}, {"energy_ev": -55.404122570000006, "dos": 0.0}, {"energy_ev": -54.59532257000001, "dos": 0.0}, {"energy_ev": -53.786522569999995, "dos": 0.0}, {"energy_ev": -52.977722570000005, "dos": 0.0}, {"energy_ev": -52.16892257000001, "dos": 0.0}, {"energy_ev": -51.36002257, "dos": 0.0}, {"energy_ev": -50.55122257, "dos": 0.0}, {"energy_ev": -49.74242257, "dos": 0.0}, {"energy_ev": -48.93362257, "dos": 0.0}, {"energy_ev": -48.12482257, "dos": 0.0}, {"energy_ev": -47.315922570000005, "dos": 0.0}, {"energy_ev": -46.50712257000001, "dos": 0.0}, {"energy_ev": -45.698322569999995, "dos": 0.0}, {"energy_ev": -44.88952257, "dos": 0.0}, {"energy_ev": -44.080722570000006, "dos": 0.0}, {"energy_ev": -43.271822570000005, "dos": 0.0}, {"energy_ev": -42.46302257000001, "dos": 0.0}, {"energy_ev": -41.65422257, "dos": 0.0}, {"energy_ev": -40.84542257, "dos": 0.0}, {"energy_ev": -40.036622570000006, "dos": 0.0}, {"energy_ev": -39.227722570000005, "dos": 0.0}, {"energy_ev": -38.41892257, "dos": 0.0}, {"energy_ev": -37.61012257, "dos": 0.0}, {"energy_ev": -36.801322569999996, "dos": 0.0}, {"energy_ev": -35.992522570000006, "dos": 0.0}, {"energy_ev": -35.183622570000004, "dos": 0.0}, {"energy_ev": -34.37482257, "dos": 0.0}, {"energy_ev": -33.56602257, "dos": 0.0}, {"energy_ev": -32.75722257, "dos": 0.0}, {"energy_ev": -31.94842257, "dos": 0.0}, {"energy_ev": -31.13952257, "dos": 0.0}, {"energy_ev": -30.330722570000002, "dos": 0.0}, {"energy_ev": -29.52192257, "dos": 0.0}, {"energy_ev": -28.713122570000003, "dos": 0.0}, {"energy_ev": -27.90432257, "dos": 0.0}, {"energy_ev": -27.09542257, "dos": 0.0}, {"energy_ev": -26.286622570000002, "dos": 0.0}, {"energy_ev": -25.47782257, "dos": 0.0}, {"energy_ev": -24.669022570000003, "dos": 0.0}, {"energy_ev": -23.86022257, "dos": 0.0}, {"energy_ev": -23.051322569999996, "dos": 0.0}, {"energy_ev": -22.242522570000002, "dos": 0.0}, {"energy_ev": -21.43372257, "dos": 0.0}, {"energy_ev": -20.62492257, "dos": 0.0}, {"energy_ev": -19.81612257, "dos": 0.0}, {"energy_ev": -19.00722257, "dos": 0.0}, {"energy_ev": -18.198422569999998, "dos": 0.0}, {"energy_ev": -17.38962257, "dos": 0.0}, {"energy_ev": -16.58082257, "dos": 0.0}, {"energy_ev": -15.772022569999999, "dos": 0.0}, {"energy_ev": -14.963122569999998, "dos": 0.0}, {"energy_ev": -14.154322569999998, "dos": 0.0}, {"energy_ev": -13.345522569999998, "dos": 5617358167014687.0}, {"energy_ev": -12.53672257, "dos": 1.0005139046360603e+18}, {"energy_ev": -11.72792257, "dos": 2.2781508121781786e+18}, {"energy_ev": -10.919022570000001, "dos": 2.141461763447488e+18}, {"energy_ev": -10.11022257, "dos": 0.0}, {"energy_ev": -9.30142257, "dos": 0.0}, {"energy_ev": -8.49262257, "dos": 2.143334216169826e+18}, {"energy_ev": -7.683822569999999, "dos": 2.1882730815059438e+18}, {"energy_ev": -6.87492257, "dos": 1.3793735054558288e+17}, {"energy_ev": -6.06612257, "dos": 2.1127508217049684e+18}, {"energy_ev": -5.25732257, "dos": 0.0}, {"energy_ev": -4.448522569999999, "dos": 1.7145425427543716e+18}, {"energy_ev": -3.63972257, "dos": 1248301814892152.8}, {"energy_ev": -2.83082257, "dos": 6.275837374370298e+18}, {"energy_ev": -2.02202257, "dos": 5.140506873725884e+18}, {"energy_ev": -1.2132225699999997, "dos": 2.5708775877703885e+18}, {"energy_ev": -0.4044225699999998, "dos": 1.1434444624412118e+18}, {"energy_ev": 0.4043774300000001, "dos": 0.0}, {"energy_ev": 1.2132774300000002, "dos": 0.0}, {"energy_ev": 2.022077430000001, "dos": 1.7145425427543716e+18}, {"energy_ev": 2.83087743, "dos": 2.2282187395824924e+18}, {"energy_ev": 3.6396774300000003, "dos": 4.5768986043020774e+18}, {"energy_ev": 4.448477430000001, "dos": 3.4808896108267674e+18}, {"energy_ev": 5.257377430000001, "dos": 5.54058760539882e+18}, {"energy_ev": 6.066177430000001, "dos": 1.7145425427543716e+18}, {"energy_ev": 6.8749774299999995, "dos": 1.8687078168935524e+18}, {"energy_ev": 7.683777429999999, "dos": 1.9535923403062188e+18}, {"energy_ev": 8.49257743, "dos": 5.207291020822615e+18}, {"energy_ev": 9.301477430000002, "dos": 2.5022209879513196e+18}, {"energy_ev": 10.110277430000002, "dos": 7.35873919878924e+17}, {"energy_ev": 10.919077430000002, "dos": 4.716084256662553e+18}, {"energy_ev": 11.727877430000001, "dos": 3.565149983331988e+18}, {"energy_ev": 12.536677430000001, "dos": 2.754377954559535e+18}, {"energy_ev": 13.34547743, "dos": 3.9383922259847414e+18}, {"energy_ev": 14.154377429999998, "dos": 5.826448721009122e+18}, {"energy_ev": 14.963177430000002, "dos": 3.1763039679930824e+18}, {"energy_ev": 15.771977430000002, "dos": 8.619524031830314e+17}, {"energy_ev": 16.580777429999998, "dos": 4.999448768643072e+18}, {"energy_ev": 17.389577430000003, "dos": 5.644820806942314e+18}, {"energy_ev": 18.19847743, "dos": 7.290706749877617e+18}, {"energy_ev": 19.007277430000002, "dos": 3.4652858381406157e+18}, {"energy_ev": 19.816077430000004, "dos": 8.145793493078742e+18}, {"energy_ev": 20.624877429999998, "dos": 5.229136302583227e+18}, {"energy_ev": 21.433677430000003, "dos": 3.5370631924969144e+18}, {"energy_ev": 22.242577429999997, "dos": 1.2882474729687014e+18}, {"energy_ev": 23.05137743, "dos": 6.746447158584638e+18}, {"energy_ev": 23.860177429999997, "dos": 5.715974010391167e+18}, {"energy_ev": 24.668977429999998, "dos": 6.081102291247121e+18}, {"energy_ev": 25.477777430000003, "dos": 3.091419444580416e+18}, {"energy_ev": 26.286677429999997, "dos": 4.89459141619213e+18}, {"energy_ev": 27.09547743, "dos": 1.717663297291602e+18}, {"energy_ev": 27.904277429999997, "dos": 7.446744476739137e+18}, {"energy_ev": 28.71307743, "dos": 3.7005907302477865e+18}, {"energy_ev": 29.521877430000004, "dos": 6.408157366748866e+18}, {"energy_ev": 30.33077743, "dos": 3.2874028295184835e+18}, {"energy_ev": 31.13957743, "dos": 1.3313138855824806e+18}, {"energy_ev": 31.948377429999997, "dos": 5.328376296867154e+18}, {"energy_ev": 32.75717742999999, "dos": 5.906340037162221e+18}, {"energy_ev": 33.56597743, "dos": 3.02713190111347e+18}, {"energy_ev": 34.374877430000005, "dos": 7.921099166398154e+18}, {"energy_ev": 35.183677429999996, "dos": 6.286447939796881e+18}, {"energy_ev": 35.99247743, "dos": 4.4645514409617843e+18}, {"energy_ev": 36.80127742999999, "dos": 4.550684266189342e+18}, {"energy_ev": 37.61007743, "dos": 1.707676882772465e+18}, {"energy_ev": 38.418977430000005, "dos": 1.3748796189222169e+19}, {"energy_ev": 39.227777429999996, "dos": 1.4374195398483139e+18}, {"energy_ev": 40.03657743, "dos": 5.146748382800345e+18}, {"energy_ev": 40.84537742999999, "dos": 6.087967951229028e+18}, {"energy_ev": 41.65417743, "dos": 7.486690134815686e+18}, {"energy_ev": 42.46307742999999, "dos": 5.762161177542177e+18}, {"energy_ev": 43.27187743, "dos": 8.940337598257596e+18}, {"energy_ev": 44.080677429999994, "dos": 2.7094390892234173e+18}, {"energy_ev": 44.88947742999999, "dos": 7.665821445252709e+18}, {"energy_ev": 45.698277430000005, "dos": 1.0915775220324428e+19}, {"energy_ev": 46.50717743, "dos": 8.329293859867889e+18}, {"energy_ev": 47.31597743, "dos": 1.470312292670722e+19}, {"energy_ev": 48.12477743, "dos": 1.2449938150826883e+19}, {"energy_ev": 48.93357743, "dos": 1.8187757442978662e+18}, {"energy_ev": 49.74237743, "dos": 4.095678254661153e+18}, {"energy_ev": 50.55127742999999, "dos": 8.052170856961831e+18}, {"energy_ev": 51.360077430000004, "dos": 2.5534013623618985e+18}, {"energy_ev": 52.168877429999995, "dos": 6.909350545428064e+18}, {"energy_ev": 52.97767742999999, "dos": 7.737598799609008e+18}, {"energy_ev": 53.786477430000005, "dos": 4.5731536988574013e+18}, {"energy_ev": 54.59537743, "dos": 7.472334663944425e+18}, {"energy_ev": 55.40417743, "dos": 9.094502872396778e+18}, {"energy_ev": 56.21297743, "dos": 2.7206738055574467e+18}, {"energy_ev": 57.02177743, "dos": 8.560229695622937e+18}, {"energy_ev": 57.83057743, "dos": 1.1413223493558952e+19}, {"energy_ev": 58.63947742999999, "dos": 4.681755956753018e+18}, {"energy_ev": 59.448277430000005, "dos": 1.2209015900552698e+19}, {"energy_ev": 60.257077429999995, "dos": 7.823731624836567e+18}, {"energy_ev": 61.06587742999999, "dos": 3.9945658076548884e+18}, {"energy_ev": 61.87467743, "dos": 9.654990387283354e+18}, {"energy_ev": 62.68357743, "dos": 6.722105273194242e+18}, {"energy_ev": 63.49237742999999, "dos": 1.4822959900936866e+19}, {"energy_ev": 64.30117743, "dos": 4.3091378650077107e+18}, {"energy_ev": 65.10997743, "dos": 6.619744524373085e+18}, {"energy_ev": 65.91877742999999, "dos": 0.0}, {"energy_ev": 66.72767743, "dos": 0.0}, {"energy_ev": 67.53647742999999, "dos": 0.0}, {"energy_ev": 68.34527743, "dos": 0.0}, {"energy_ev": 69.15407743, "dos": 0.0}, {"energy_ev": 69.96287742999999, "dos": 0.0}, {"energy_ev": 70.77177743, "dos": 0.0}, {"energy_ev": 71.58057742999999, "dos": 0.0}, {"energy_ev": 72.38937743, "dos": 0.0}, {"energy_ev": 73.19817743, "dos": 0.0}, {"energy_ev": 74.00697742999999, "dos": 0.0}, {"energy_ev": 74.81587743, "dos": 0.0}, {"energy_ev": 75.62467742999999, "dos": 0.0}, {"energy_ev": 76.43347743, "dos": 0.0}, {"energy_ev": 77.24227743, "dos": 0.0}, {"energy_ev": 78.05107742999999, "dos": 0.0}, {"energy_ev": 78.85997743, "dos": 0.0}, {"energy_ev": 79.66877742999999, "dos": 0.0}]');
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


