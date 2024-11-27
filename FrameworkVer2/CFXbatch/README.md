# CFXbatch

This framework allows users to effortlessly launch CFD simulations for turbocompressors based on specified geometries and operating conditions. The CFXbatch.py script is where the user defines the simulation parameters (see the following subsection for details). Once the script is executed, CFX runs the simulation in the background. While many aspects of the CFD setup are pre-configured, the framework offers flexibility to adjust key factors that vary across different scenarios, as deemed important by the author. 

## Simulation definition

Within CFXbatch.py the user defines the simulation parameters as a dictionary like the one below.

```
simulation_definition = {
...
}
```
More specifically, the dictionary stores the following information.
```

simulation_definition = {

    #! Ansys local address 

    "ansys_path" : r"C:\Program Files\ANSYS Inc\v241",

```
"ansys_path" defines the path in which Ansys is stored locally. Might change from one machine to another.
```

    #! project/case name definition

    "project_path" : r'C:\Users\soukhman\Desktop\test',
    "case_name" : 'simulation1',

```
The "project_path" is the location where the "case_name" folder, containing all the simulation data, will be created.
```

    #! geometry definition

    "geometry type" : "from database", # "from database --> retrieve existing geometry" - "from parametrization --> use Davide's work to generate a geometry"
    "geometry name" : "LUS",
    "parametrization" : None,

    "tip clearance" : 50, #[micron]
    "n channels" : 9,
    "geom param1" : None,
    "geom param2" : None,
    "geom param3" : None,
    "geom param4" : None,
    "roughness" : 10, #[micron]

```
The "geometry type" specifies whether the simulation will use an existing geometry in .bgd format (located in "CFXbatch\CFXsetup_files\geometry_turbocompressor_database") or a geometry defined by the in-house turbocompressor parameterization.
```
    #! fluid definition 
    
    "fluid name" : "r134a",
    "RGP address" : None,           # keep None if you want to create an RGP table from scratch
    "RGP Pmin" : 10000,
    "RGP Pmax" : 3000000,
    "RGP Tmin" : 160,
    "RGP Tmax" : 450,
    "RGP Tsatmin" : 160,
    "RGP Tsatmax" : 350,
    "RGP nP" : 366,                 # number pressure points
    "RGP nT" : 251,                 # number temperature points
    "RGP nPsat" : 155,              # number pressure points on saturation line

```
The fluid for the simulation is either defined by an RGP table file specified in the "RGP address" or generated ( by means of the RGP generator in LAMD GITLAB /thermodynamics/rgp-generator) using the other provided entries.
```

    #! operating condition definition

    "Pin" : 200000, #[Pa]
    "Tin" : 273, #[K]
    "mass flow" : 0.03, #[kg s^-1]
    "rotational speed" : 150000, #[rev min^-1]

```
The operating conditions are consistent with the ones used in the in-house 1D model.
```

    #! mesh and solver definition 
    "mesh size factor" : 0.77,
    "n partitions" : 10,
    "n iterations" : 200, 
    "target residual" : 1e-6 
}
```
"mesh size factor" determines the size of the mesh (important to setup a grid convergence analysis) and "n partitions" determines the number of processes on which the simulation is distributed.

