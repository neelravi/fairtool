
# __Si VASP DFT SinglePoint simulation__

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
    | a | **3.918** | Angstrom |
    | b | **3.918** | Angstrom |
    | c | **3.918** | Angstrom |

    | Lattice angles    | Value     | Units |
    |------------------|-----------|-------|
    | Alpha | **60** | Degrees |
    | Beta | **60** | Degrees |
    | Gamma | **60** | Degrees |

    | Cell quantities   | Value     | Units |
    |------------------|-----------|-------|
    | Volume | **42.528** | Å³ |
    | Mass density | **2.193e-27** | kg / Å³ |
    | Atomic density | **0.047** | Å⁻³ |

- ### Lattice (conventional cell)

    | Lattice constant | Value     | Units |
    |------------------|-----------|-------|
    | a | **5.541** | Angstrom |
    | b | **5.541** | Angstrom |
    | c | **5.541** | Angstrom |

    | Lattice angles    | Value     | Units |
    |------------------|-----------|-------|
    | Alpha | **90** | Degrees |
    | Beta | **90** | Degrees |
    | Gamma | **90** | Degrees |

    | Cell quantities   | Value     | Units |
    |------------------|-----------|-------|
    | Volume | **170.111** | Å³ |
    | Mass density | **2.193e-27** | kg / Å³ |
    | Atomic density | **0.047** | Å⁻³ |

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
    | Sampling method | **Monkhorst-Pack** |
    | Number of points | **3375** |
    | Grid | **[15, 15, 15]** |

</div>

## __Metadata__

<div class="grid cards" markdown>

- ### Calculation Metadata

    | Property                   | Value                                                      |
    |----------------------------|------------------------------------------------------------|
    | **Method name** | DFT |
    | **Workflow name** | SinglePoint |
    | **Program name** | VASP |
    | **Program version** | 5.2.2 15Apr09 complex serial LinuxIFC |
    | **Basis set type** | plane waves |
    | **Core electron treatment** | pseudopotential |
    | **Jacob's ladder** | GGA |
    | **XC functional names** | GGA_C_PBE, GGA_X_PBE |
    | **Code-specific tier** | VASP - accurate |
    | **Basis set** | plane waves |
    | **Entry type** | VASP DFT SinglePoint |
    | **Entry name** | Si VASP DFT SinglePoint simulation |
    | **Mainfile** | dos_si_vasprun.xml |

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
    const scfData = JSON.parse('[{"step": 1, "total_ev": 3.76925286, "free_ev": 3.76925286, "total_t0_ev": 3.76925286}, {"step": 2, "total_ev": -10.77482824, "free_ev": -10.77482824, "total_t0_ev": -10.77482824}, {"step": 3, "total_ev": -10.97884908, "free_ev": -10.97884908, "total_t0_ev": -10.97884908}, {"step": 4, "total_ev": -10.979694469999998, "free_ev": -10.979694469999998, "total_t0_ev": -10.979694469999998}, {"step": 5, "total_ev": -10.97969569, "free_ev": -10.97969569, "total_t0_ev": -10.97969569}, {"step": 6, "total_ev": -10.87928799, "free_ev": -10.87928799, "total_t0_ev": -10.87928799}, {"step": 7, "total_ev": -10.831247480000002, "free_ev": -10.831247480000002, "total_t0_ev": -10.831247480000002}, {"step": 8, "total_ev": -10.8325844, "free_ev": -10.8325844, "total_t0_ev": -10.8325844}, {"step": 9, "total_ev": -10.8326945, "free_ev": -10.8326945, "total_t0_ev": -10.8326945}, {"step": 10, "total_ev": -10.8327159, "free_ev": -10.8327159, "total_t0_ev": -10.8327159}]');

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
    | **Total** | -10.832716 |
    | **Free** | -10.832716 |
    | **Total (T=0)** | 0.000000 |
    | **Band Gap** | 0.681800 |

- ### SCF Iteration Energies

    | Step | Total Energy (eV) | Free Energy (eV) | Total Energy (T=0) (eV) |
    |:---|---:|---:|---:|
| 1 | 3.76925 | 3.76925 | 3.76925 |
| 2 | -10.77483 | -10.77483 | -10.77483 |
| 3 | -10.97885 | -10.97885 | -10.97885 |
| 4 | -10.97969 | -10.97969 | -10.97969 |
| 5 | -10.97970 | -10.97970 | -10.97970 |
| 6 | -10.87929 | -10.87929 | -10.87929 |
| 7 | -10.83125 | -10.83125 | -10.83125 |
| 8 | -10.83258 | -10.83258 | -10.83258 |
| 9 | -10.83269 | -10.83269 | -10.83269 |
| 10 | -10.83272 | -10.83272 | -10.83272 |

</div>


<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
<div id="scf_chart_div" style="width: 100%; height: 500px; margin-bottom: 20px;"></div>
<script type="text/javascript">
  google.charts.load('current', {'packages':['corechart']});
  google.charts.setOnLoadCallback(drawChart);

  function drawChart() {
    // Parse the JSON data passed from Python
    const scfData = JSON.parse('[{"step": 1, "total_ev": 3.76925286, "free_ev": 3.76925286, "total_t0_ev": 3.76925286}, {"step": 2, "total_ev": -10.77482824, "free_ev": -10.77482824, "total_t0_ev": -10.77482824}, {"step": 3, "total_ev": -10.97884908, "free_ev": -10.97884908, "total_t0_ev": -10.97884908}, {"step": 4, "total_ev": -10.979694469999998, "free_ev": -10.979694469999998, "total_t0_ev": -10.979694469999998}, {"step": 5, "total_ev": -10.97969569, "free_ev": -10.97969569, "total_t0_ev": -10.97969569}, {"step": 6, "total_ev": -10.87928799, "free_ev": -10.87928799, "total_t0_ev": -10.87928799}, {"step": 7, "total_ev": -10.831247480000002, "free_ev": -10.831247480000002, "total_t0_ev": -10.831247480000002}, {"step": 8, "total_ev": -10.8325844, "free_ev": -10.8325844, "total_t0_ev": -10.8325844}, {"step": 9, "total_ev": -10.8326945, "free_ev": -10.8326945, "total_t0_ev": -10.8326945}, {"step": 10, "total_ev": -10.8327159, "free_ev": -10.8327159, "total_t0_ev": -10.8327159}]');

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
    const dosData = JSON.parse('[{"energy_ev": -13.563215190000001, "dos": 0.0}, {"energy_ev": -13.48011519, "dos": 0.0}, {"energy_ev": -13.396915190000001, "dos": 0.0}, {"energy_ev": -13.31381519, "dos": 0.0}, {"energy_ev": -13.23061519, "dos": 0.0}, {"energy_ev": -13.147515190000002, "dos": 0.0}, {"energy_ev": -13.06441519, "dos": 0.0}, {"energy_ev": -12.98121519, "dos": 0.0}, {"energy_ev": -12.898115189999999, "dos": 0.0}, {"energy_ev": -12.814915189999999, "dos": 0.0}, {"energy_ev": -12.73181519, "dos": 0.0}, {"energy_ev": -12.64861519, "dos": 0.0}, {"energy_ev": -12.565515190000001, "dos": 0.0}, {"energy_ev": -12.482315190000001, "dos": 0.0}, {"energy_ev": -12.39921519, "dos": 0.0}, {"energy_ev": -12.31601519, "dos": 0.0}, {"energy_ev": -12.232915189999998, "dos": 0.0}, {"energy_ev": -12.149715189999998, "dos": 0.0}, {"energy_ev": -12.06661519, "dos": 0.0}, {"energy_ev": -11.98341519, "dos": 0.0}, {"energy_ev": -11.90031519, "dos": 0.0}, {"energy_ev": -11.81721519, "dos": 0.0}, {"energy_ev": -11.73401519, "dos": 0.0}, {"energy_ev": -11.650915190000001, "dos": 0.0}, {"energy_ev": -11.567715190000001, "dos": 0.0}, {"energy_ev": -11.48461519, "dos": 5.405146858483021e+17}, {"energy_ev": -11.40141519, "dos": 9.224950412053007e+17}, {"energy_ev": -11.318315189999998, "dos": 1.0966331443827561e+18}, {"energy_ev": -11.23511519, "dos": 1.334434640119711e+18}, {"energy_ev": -11.15201519, "dos": 1.4861033106291077e+18}, {"energy_ev": -11.06881519, "dos": 1.63527537750872e+18}, {"energy_ev": -10.98571519, "dos": 1.816279140668082e+18}, {"energy_ev": -10.90251519, "dos": 1.9392368694349588e+18}, {"energy_ev": -10.819415189999999, "dos": 2.069060258183743e+18}, {"energy_ev": -10.736315190000001, "dos": 2.208245910544218e+18}, {"energy_ev": -10.653115190000001, "dos": 2.3592904301461683e+18}, {"energy_ev": -10.57001519, "dos": 2.471013442579016e+18}, {"energy_ev": -10.48681519, "dos": 2.591474567716109e+18}, {"energy_ev": -10.403715190000002, "dos": 2.723170409187231e+18}, {"energy_ev": -10.32051519, "dos": 2.8604836088253676e+18}, {"energy_ev": -10.23741519, "dos": 2.9953002048337203e+18}, {"energy_ev": -10.15421519, "dos": 3.124499442675058e+18}, {"energy_ev": -10.07111519, "dos": 3.2618126423131945e+18}, {"energy_ev": -9.98791519, "dos": 3.41535376554493e+18}, {"energy_ev": -9.904815189999999, "dos": 3.5782571523883556e+18}, {"energy_ev": -9.82161519, "dos": 3.754267708288149e+18}, {"energy_ev": -9.738515190000001, "dos": 3.9446337350592026e+18}, {"energy_ev": -9.65541519, "dos": 4.169952212647236e+18}, {"energy_ev": -9.57221519, "dos": 4.4589340827947694e+18}, {"energy_ev": -9.489115190000001, "dos": 4.844659343596445e+18}, {"energy_ev": -9.40591519, "dos": 5.683518163203971e+18}, {"energy_ev": -9.32281519, "dos": 6.026801162299313e+18}, {"energy_ev": -9.23961519, "dos": 5.704115143149692e+18}, {"energy_ev": -9.15651519, "dos": 5.525607983620113e+18}, {"energy_ev": -9.07331519, "dos": 5.302161958754419e+18}, {"energy_ev": -8.99021519, "dos": 5.065608764832355e+18}, {"energy_ev": -8.90701519, "dos": 5.000072919550517e+18}, {"energy_ev": -8.823915190000001, "dos": 4.731063878441259e+18}, {"energy_ev": -8.74071519, "dos": 4.51448351355747e+18}, {"energy_ev": -8.65761519, "dos": 4.3284865431385395e+18}, {"energy_ev": -8.57451519, "dos": 4.1605899490355446e+18}, {"energy_ev": -8.49131519, "dos": 3.9433854332443105e+18}, {"energy_ev": -8.40821519, "dos": 3.704959786599909e+18}, {"energy_ev": -8.32501519, "dos": 3.526452627070331e+18}, {"energy_ev": -8.24191519, "dos": 3.3354624493918316e+18}, {"energy_ev": -8.15871519, "dos": 3.103902462729338e+18}, {"energy_ev": -8.075615189999999, "dos": 2.865476816084936e+18}, {"energy_ev": -7.99241519, "dos": 2.7668609727084564e+18}, {"energy_ev": -7.90931519, "dos": 2.3599145810536146e+18}, {"energy_ev": -7.82611519, "dos": 2.0971470490188165e+18}, {"energy_ev": -7.74301519, "dos": 6.441237364843507e+17}, {"energy_ev": -7.659815190000001, "dos": 6865659981906840.0}, {"energy_ev": -7.57671519, "dos": 1.6227923593597984e+16}, {"energy_ev": -7.49351519, "dos": 1.5229282141684262e+17}, {"energy_ev": -7.41041519, "dos": 4.918309150675081e+17}, {"energy_ev": -7.32731519, "dos": 1.0435803172498395e+18}, {"energy_ev": -7.2441151900000005, "dos": 1.8193998952053123e+18}, {"energy_ev": -7.1610151900000005, "dos": 2.5028451388587663e+18}, {"energy_ev": -7.07781519, "dos": 2.7337809746138143e+18}, {"energy_ev": -6.99471519, "dos": 2.904798323254039e+18}, {"energy_ev": -6.91151519, "dos": 3.2917718858706063e+18}, {"energy_ev": -6.82841519, "dos": 3.7280533701754143e+18}, {"energy_ev": -6.745215190000001, "dos": 4.141865421812162e+18}, {"energy_ev": -6.66211519, "dos": 5.816462306489985e+18}, {"energy_ev": -6.57891519, "dos": 1.25666543705193e+19}, {"energy_ev": -6.49581519, "dos": 8.684435726204706e+18}, {"energy_ev": -6.41261519, "dos": 6.771413194882482e+18}, {"energy_ev": -6.32951519, "dos": 5.743436650318795e+18}, {"energy_ev": -6.2464151900000005, "dos": 5.046884237608973e+18}, {"energy_ev": -6.16321519, "dos": 4.596247282432906e+18}, {"energy_ev": -6.08011519, "dos": 4.2641989996715935e+18}, {"energy_ev": -5.99691519, "dos": 3.97521712952406e+18}, {"energy_ev": -5.91381519, "dos": 3.713697899304154e+18}, {"energy_ev": -5.8306151900000005, "dos": 3.4733997999374147e+18}, {"energy_ev": -5.74751519, "dos": 3.213128871532401e+18}, {"energy_ev": -5.66431519, "dos": 3.039614919262392e+18}, {"energy_ev": -5.58121519, "dos": 2.904798323254039e+18}, {"energy_ev": -5.49801519, "dos": 2.774350783597809e+18}, {"energy_ev": -5.41491519, "dos": 2.6495206021085937e+18}, {"energy_ev": -5.331715190000001, "dos": 2.51969721335981e+18}, {"energy_ev": -5.24861519, "dos": 2.3692768446653056e+18}, {"energy_ev": -5.16551519, "dos": 2.2275945886750464e+18}, {"energy_ev": -5.08231519, "dos": 2.1164957271496448e+18}, {"energy_ev": -4.99921519, "dos": 2.0415976182561157e+18}, {"energy_ev": -4.91601519, "dos": 1.9666995093625864e+18}, {"energy_ev": -4.8329151900000005, "dos": 1.8911772495616113e+18}, {"energy_ev": -4.74971519, "dos": 1.8050444243340529e+18}, {"energy_ev": -4.66661519, "dos": 1.717663297291602e+18}, {"energy_ev": -4.58341519, "dos": 1.6334029247863816e+18}, {"energy_ev": -4.50031519, "dos": 1.5173108560014116e+18}, {"energy_ev": -4.41711519, "dos": 1.4542716143493578e+18}, {"energy_ev": -4.33401519, "dos": 1.405587843568564e+18}, {"energy_ev": -4.250815190000001, "dos": 1.3556557709728778e+18}, {"energy_ev": -4.16771519, "dos": 1.3063478492846377e+18}, {"energy_ev": -4.08451519, "dos": 2.0197523364955028e+18}, {"energy_ev": -4.00141519, "dos": 4.588757471543553e+18}, {"energy_ev": -3.91831519, "dos": 6.137900023824715e+18}, {"energy_ev": -3.8351151900000002, "dos": 8.901016091088494e+18}, {"energy_ev": -3.7520151900000003, "dos": 8.215074243805257e+18}, {"energy_ev": -3.6688151900000006, "dos": 7.712632763311165e+18}, {"energy_ev": -3.58571519, "dos": 6.910598847242957e+18}, {"energy_ev": -3.50251519, "dos": 6.763299233085683e+18}, {"energy_ev": -3.41941519, "dos": 6.493041890161532e+18}, {"energy_ev": -3.3362151900000003, "dos": 7.054777706863001e+18}, {"energy_ev": -3.2531151900000004, "dos": 6.738333196787839e+18}, {"energy_ev": -3.1699151899999998, "dos": 7.014832048786451e+18}, {"energy_ev": -3.08681519, "dos": 7.228291659133009e+18}, {"energy_ev": -3.00361519, "dos": 7.363108255141362e+18}, {"energy_ev": -2.92051519, "dos": 7.723243328737749e+18}, {"energy_ev": -2.83741519, "dos": 8.792413833192877e+18}, {"energy_ev": -2.7542151899999996, "dos": 9.085764759692533e+18}, {"energy_ev": -2.67111519, "dos": 1.0093768475217947e+19}, {"energy_ev": -2.5879151900000004, "dos": 1.0170539036833812e+19}, {"energy_ev": -2.50481519, "dos": 9.8384907540725e+18}, {"energy_ev": -2.42161519, "dos": 9.750485476122604e+18}, {"energy_ev": -2.33851519, "dos": 9.639386614597202e+18}, {"energy_ev": -2.2553151899999997, "dos": 9.368505120765604e+18}, {"energy_ev": -2.1722151899999997, "dos": 9.107610041453146e+18}, {"energy_ev": -2.0890151899999996, "dos": 9.134448530473327e+18}, {"energy_ev": -2.0059151899999996, "dos": 8.994638727205406e+18}, {"energy_ev": -1.9227151900000001, "dos": 8.757461382375897e+18}, {"energy_ev": -1.8396151900000002, "dos": 8.538384413862324e+18}, {"energy_ev": -1.7565151900000002, "dos": 8.45474819226455e+18}, {"energy_ev": -1.67331519, "dos": 8.414178383280555e+18}, {"energy_ev": -1.5902151900000001, "dos": 8.245657638270114e+18}, {"energy_ev": -1.50701519, "dos": 8.248778392807345e+18}, {"energy_ev": -1.42391519, "dos": 8.190732358414859e+18}, {"energy_ev": -1.3407151899999998, "dos": 8.011601047977836e+18}, {"energy_ev": -1.2576151899999999, "dos": 7.809376153965308e+18}, {"energy_ev": -1.1744151900000004, "dos": 7.160883361128833e+18}, {"energy_ev": -1.0913151900000004, "dos": 5.598633639791305e+18}, {"energy_ev": -1.0081151899999996, "dos": 4.798472176445435e+18}, {"energy_ev": -0.9250151899999997, "dos": 4.1524759872387456e+18}, {"energy_ev": -0.8418151900000002, "dos": 3.6675107321531443e+18}, {"energy_ev": -0.7587151900000002, "dos": 3.2012700042909256e+18}, {"energy_ev": -0.6755151900000006, "dos": 2.827403610730726e+18}, {"energy_ev": -0.5924151900000006, "dos": 2.4878655170800604e+18}, {"energy_ev": -0.5093151900000007, "dos": 2.2588021340473503e+18}, {"energy_ev": -0.4261151899999999, "dos": 1.8930497022839496e+18}, {"energy_ev": -0.34301518999999997, "dos": 1.5516391559109455e+18}, {"energy_ev": -0.2598151900000004, "dos": 1.1902557804996675e+18}, {"energy_ev": -0.17671519000000044, "dos": 7.839335397522717e+17}, {"energy_ev": -0.09351519000000032, "dos": 4.312882770452387e+17}, {"energy_ev": -0.010415189999999736, "dos": 0.0}, {"energy_ev": 0.0727848099999998, "dos": 0.0}, {"energy_ev": 0.15588480999999976, "dos": 0.0}, {"energy_ev": 0.23908480999999993, "dos": 0.0}, {"energy_ev": 0.3221848099999999, "dos": 0.0}, {"energy_ev": 0.40538481000000065, "dos": 0.0}, {"energy_ev": 0.4884848100000006, "dos": 0.0}, {"energy_ev": 0.5715848100000006, "dos": 0.0}, {"energy_ev": 0.6547848100000001, "dos": 0.0}, {"energy_ev": 0.7378848100000001, "dos": 2.7587470109116576e+17}, {"energy_ev": 0.8210848099999997, "dos": 8.43227875959649e+17}, {"energy_ev": 0.9041848099999996, "dos": 1.3132135092665446e+18}, {"energy_ev": 0.9873848100000003, "dos": 1.7457500881266755e+18}, {"energy_ev": 1.0704848100000004, "dos": 2.2194806268782474e+18}, {"energy_ev": 1.15368481, "dos": 2.7044458819638487e+18}, {"energy_ev": 1.2367848099999998, "dos": 3.070822464634695e+18}, {"energy_ev": 1.3199848099999993, "dos": 3.2836579240738074e+18}, {"energy_ev": 1.4030848100000006, "dos": 3.6937250702658796e+18}, {"energy_ev": 1.4862848100000001, "dos": 4.1618382508504366e+18}, {"energy_ev": 1.56938481, "dos": 4.697983880346617e+18}, {"energy_ev": 1.65248481, "dos": 5.309651769643771e+18}, {"energy_ev": 1.7356848099999995, "dos": 5.903843433532435e+18}, {"energy_ev": 1.8187848099999995, "dos": 6.571060753592291e+18}, {"energy_ev": 1.9019848100000003, "dos": 7.398060705958343e+18}, {"energy_ev": 1.9850848100000003, "dos": 8.407312723298648e+18}, {"energy_ev": 2.0682848099999998, "dos": 9.648124727301448e+18}, {"energy_ev": 2.1513848099999997, "dos": 1.1383264250001541e+19}, {"energy_ev": 2.2345848099999994, "dos": 1.2093547982675175e+19}, {"energy_ev": 2.3176848099999994, "dos": 1.1207877845009193e+19}, {"energy_ev": 2.40088481, "dos": 1.0701067308162978e+19}, {"energy_ev": 2.48398481, "dos": 9.467120964142084e+18}, {"energy_ev": 2.5671848099999997, "dos": 7.946065202695996e+18}, {"energy_ev": 2.6502848099999996, "dos": 7.489810889352916e+18}, {"energy_ev": 2.733484809999999, "dos": 8.29871046540303e+18}, {"energy_ev": 2.816584809999999, "dos": 7.75632332683239e+18}, {"energy_ev": 2.899684809999999, "dos": 6.534860000960419e+18}, {"energy_ev": 2.9828848099999985, "dos": 5.304658562384203e+18}, {"energy_ev": 3.0659848099999985, "dos": 5.157358948226929e+18}, {"energy_ev": 3.1491848100000004, "dos": 5.754671366652824e+18}, {"energy_ev": 3.2322848100000003, "dos": 8.215074243805257e+18}, {"energy_ev": 3.31548481, "dos": 1.5053895736691915e+19}, {"energy_ev": 3.39858481, "dos": 1.5359105530433044e+19}, {"energy_ev": 3.4817848099999993, "dos": 1.3608986385954249e+19}, {"energy_ev": 3.5648848099999992, "dos": 1.415074937361744e+19}, {"energy_ev": 3.648084809999999, "dos": 1.287061586244554e+19}, {"energy_ev": 3.731184809999999, "dos": 1.0189263564057197e+19}, {"energy_ev": 3.8143848099999995, "dos": 8.788044776840754e+18}, {"energy_ev": 3.8974848099999986, "dos": 8.200718772933998e+18}, {"energy_ev": 3.9805848099999985, "dos": 8.154531605782987e+18}, {"energy_ev": 4.0637848100000005, "dos": 7.270109769931897e+18}, {"energy_ev": 4.14688481, "dos": 6.774533949419711e+18}, {"energy_ev": 4.23008481, "dos": 7.119065250329947e+18}, {"energy_ev": 4.31318481, "dos": 7.944816900881105e+18}, {"energy_ev": 4.39638481, "dos": 8.819252322213059e+18}, {"energy_ev": 4.47948481, "dos": 8.685684028019597e+18}, {"energy_ev": 4.562684809999999, "dos": 8.211329338360581e+18}, {"energy_ev": 4.6457848099999985, "dos": 7.714505216033503e+18}, {"energy_ev": 4.72898481, "dos": 7.702646348792027e+18}, {"energy_ev": 4.81208481, "dos": 8.011601047977836e+18}, {"energy_ev": 4.895284810000001, "dos": 9.530784356701585e+18}, {"energy_ev": 4.9783848100000005, "dos": 8.255019901881805e+18}, {"energy_ev": 5.0614848100000005, "dos": 8.065902176925644e+18}, {"energy_ev": 5.14468481, "dos": 7.521642585632666e+18}, {"energy_ev": 5.22778481, "dos": 7.442375420387014e+18}, {"energy_ev": 5.310984809999999, "dos": 7.559091640079431e+18}, {"energy_ev": 5.394084809999999, "dos": 7.315048635268014e+18}, {"energy_ev": 5.4772848100000004, "dos": 7.218305244613873e+18}, {"energy_ev": 5.5603848099999995, "dos": 6.954913561671629e+18}, {"energy_ev": 5.643584809999999, "dos": 6.878143000055762e+18}, {"energy_ev": 5.72668481, "dos": 7.184601095611784e+18}, {"energy_ev": 5.80988481, "dos": 6.901860734538711e+18}, {"energy_ev": 5.892984810000001, "dos": 6.720232820471903e+18}, {"energy_ev": 5.97618481, "dos": 5.684142314111416e+18}, {"energy_ev": 6.059284810000001, "dos": 5.681021559574187e+18}, {"energy_ev": 6.142484810000001, "dos": 6.017438898687621e+18}, {"energy_ev": 6.22558481, "dos": 6.55857773544337e+18}, {"energy_ev": 6.308684810000001, "dos": 6.659066031542188e+18}, {"energy_ev": 6.3918848100000005, "dos": 6.303924165205371e+18}, {"energy_ev": 6.47498481, "dos": 6.289568694334112e+18}, {"energy_ev": 6.558184809999999, "dos": 6.240884923553317e+18}, {"energy_ev": 6.64128481, "dos": 6.423761139435017e+18}, {"energy_ev": 6.72448481, "dos": 5.908212489884558e+18}, {"energy_ev": 6.807584809999998, "dos": 5.34959742772032e+18}, {"energy_ev": 6.89078481, "dos": 4.940154432435694e+18}, {"energy_ev": 6.973884810000001, "dos": 4.44769936646074e+18}, {"energy_ev": 7.057084810000001, "dos": 4.18680428714828e+18}, {"energy_ev": 7.14018481, "dos": 3.9901967513027656e+18}, {"energy_ev": 7.22338481, "dos": 3.9059363787975455e+18}, {"energy_ev": 7.306484810000001, "dos": 3.822924308107218e+18}, {"energy_ev": 7.38958481, "dos": 3.4790171581044296e+18}, {"energy_ev": 7.4727848099999985, "dos": 3.1944043443090186e+18}, {"energy_ev": 7.55588481, "dos": 3.2112564188100623e+18}, {"energy_ev": 7.63908481, "dos": 3.2056390606430474e+18}, {"energy_ev": 7.722184810000001, "dos": 4.360318239418289e+18}, {"energy_ev": 7.8053848100000005, "dos": 2.2694126994739333e+18}, {"energy_ev": 7.888484810000001, "dos": 1.569739532226882e+18}, {"energy_ev": 7.971684810000001, "dos": 1.4786134997397548e+18}, {"energy_ev": 8.05478481, "dos": 1.4436610489227745e+18}, {"energy_ev": 8.137984809999999, "dos": 1.4093327490132403e+18}, {"energy_ev": 8.22108481, "dos": 1.3862391654377354e+18}, {"energy_ev": 8.30428481, "dos": 1.3225757728782356e+18}, {"energy_ev": 8.38738481, "dos": 1.0935123898455256e+18}, {"energy_ev": 8.47048481, "dos": 9.056429667042568e+17}, {"energy_ev": 8.55368481, "dos": 7.907991997341787e+17}, {"energy_ev": 8.63678481, "dos": 6.865659981906839e+17}, {"energy_ev": 8.71998481, "dos": 5.916950602588803e+17}, {"energy_ev": 8.803084810000001, "dos": 5.0618638593876794e+17}, {"energy_ev": 8.886284810000001, "dos": 4.306641261377927e+17}, {"energy_ev": 8.96938481, "dos": 3.6387997904106246e+17}, {"energy_ev": 9.05258481, "dos": 3.070822464634696e+17}, {"energy_ev": 9.13568481, "dos": 2.5964677749756774e+17}, {"energy_ev": 9.21888481, "dos": 2.5278111751566093e+17}, {"energy_ev": 9.30198481, "dos": 3.8884601533890554e+17}, {"energy_ev": 9.38518481, "dos": 0.0}, {"energy_ev": 9.46828481, "dos": 0.0}, {"energy_ev": 9.55138481, "dos": 0.0}, {"energy_ev": 9.63458481, "dos": 0.0}, {"energy_ev": 9.717684810000002, "dos": 0.0}, {"energy_ev": 9.800884810000001, "dos": 0.0}, {"energy_ev": 9.883984810000003, "dos": 0.0}, {"energy_ev": 9.967184810000001, "dos": 0.0}, {"energy_ev": 10.05028481, "dos": 0.0}, {"energy_ev": 10.13348481, "dos": 0.0}, {"energy_ev": 10.21658481, "dos": 0.0}, {"energy_ev": 10.29978481, "dos": 0.0}, {"energy_ev": 10.38288481, "dos": 0.0}, {"energy_ev": 10.466084809999998, "dos": 0.0}, {"energy_ev": 10.54918481, "dos": 0.0}, {"energy_ev": 10.632384810000001, "dos": 0.0}, {"energy_ev": 10.715484810000001, "dos": 0.0}, {"energy_ev": 10.798584810000001, "dos": 0.0}, {"energy_ev": 10.88178481, "dos": 0.0}, {"energy_ev": 10.964884810000001, "dos": 0.0}, {"energy_ev": 11.048084810000002, "dos": 0.0}, {"energy_ev": 11.13118481, "dos": 0.0}, {"energy_ev": 11.214384810000004, "dos": 0.0}, {"energy_ev": 11.297484809999998, "dos": 0.0}, {"energy_ev": 11.380684810000002, "dos": 0.0}]');
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


