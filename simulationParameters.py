def create_simulation_def(ansys_path = r"C:\Program Files\ANSYS Inc\v242",
                          simulation_path = r'C:\Users\soukhman\Desktop\LUS_test',
                          case_name = 'simulation1',
                          geometry_name = "LUS",
                          n_channels = 9):
    
    simulation_definition = {

        #! Ansys local address 

        "ansys_path" : ansys_path,

        #! project/case name definition

        "project_path" : simulation_path,
        "case_name" : case_name,

        #! geometry definition

        "geometry type" : "from database", # "from database --> retrieve existing geometry"
        "geometry name" : geometry_name,

        "tip clearance" : 50, #[micron]
        "n channels" : n_channels,
        "roughness" : 10, #[micron]

        #! fluid definition 

        "fluid name" : "r134a",
        "RGP address" : None,           # keep None if you want to create an RGP table from scratch
        "RGP Pmin" : 10000,
        "RGP Pmax" : 3000000,
        "RGP Tmin" : 180,
        "RGP Tmax" : 450,
        "RGP Tsatmin" : 180,
        "RGP Tsatmax" : 350,
        "RGP nP" : 366,                 # number pressure points
        "RGP nT" : 251,                 # number temperature points
        "RGP nPsat" : 155,              # number pressure points on saturation line

        #! operating condition definition

        "Pin" : 175000, #[Pa]
        "Tin" : 270, #[K]
        "mass flow" : 0.03, #[kg s^-1]
        "rotational speed" : 160000, #[rev min^-1]

        #! mesh and solver definition 
        "mesh size factor" : 1,  # 1
        "n partitions" : 5, # number of processes
        "n iterations" : 2, # 500
        "target residual" : 1e-5 # threshold
    }

    return simulation_definition

##############################################################################################################################
##############################################################################################################################
#! SPEEDLINE LAUNCHER

# N_rot = [150, 180]  # krpm
# mfr_list = [[20, 35, 45], [30, 45, 50]] # g/s

# for i in range(len(N_rot)):
#     for j in range(len(mfr_list[i])):

#         #! update simulation definition
#         simulation_definition["case_name"] = "sim_N%d_mfr%d"%(N_rot[i], mfr_list[i][j])
#         simulation_definition["mass flow"] = mfr_list[i][j]*1e-3
#         simulation_definition["rotational speed"] = N_rot[i]*1e3

#         run_CFXbatch(simulation_definition)

##############################################################################################################################
##############################################################################################################################
#! GRID CONVERGENCE ANALYSIS LAUNCHER

# mesh_factor = [1.0,1.3,1.5,1.8,2.0]  

# for i in range(len(mesh_factor)):

#     #! update simulation definition
#     simulation_definition["case_name"] = "sim_meshfactor_%d"%(i)
#     simulation_definition["mesh size factor"] = mesh_factor[i]

    # CFXbatch.run_CFXbatch(simulation_definition)

##############################################################################################################################
##############################################################################################################################
#! SINGLE SIMULATION LAUNCHER

# CFXbatch.run_CFXbatch(simulation_definition)

##############################################################################################################################
##############################################################################################################################
#! TEST WITH DIFFERENT GEOMETRIES

# for i in range(1):

#     #! update simulation definition
#     simulation_definition["case_name"] = "CTC%d_stage1"%(i+3)
#     simulation_definition["geometry name"] = "CTC%d_stage1"%(i+3)

#     CFXbatch.run_CFXbatch(simulation_definition)