import numpy as np
from Folder_management import *

# SETTINGS OF THE SIMULATED DATASET

# Print Results & Conversion Output | Y/n = True/False
print_results = False
print_conversion_output = False

# Beta at inlet and outlet from 1D
beta_in_settings = 24.008 # (beta_2, beta in corrispondenza dell'hub all'inlet)
beta_out_settings = 35.15 # (beta_4, beta in corrispondenza dell'hub all'outlet)

# HUB AND SHROUD PARAMETERS
# Geometrical Parameters from 1D
L_ind = 30 #30
r2s = 5.6 #5.6
r2h = 2 #2
r4  = 10 #10
b4  = 1 #1
r5  = 30 #30
# Hub ans Shroud | Weights for the control point of the hub and shroud profiles
w1_hb = 1
w1_sh = 1
# Splitter LE Cut, Meridional Target
splitter_LE_meridional_target_hub_settings = 0.3
splitter_LE_meridional_target_sh_settings = 0.3

# Constant thickness settings
thickness = 0.2

# Decide how many points to compute for the Bezier curves
beta_bezier_N = 300 # Number of points to compute for beta curve
HubShr_bezier_N = 300 # Number of points for the hub and shroud bezier

# DISCRETIZATION OF THE BETA/M% CURVE'S PARAMETERS
# Discrtization of the parameter tau_0
tau_0 = 0.42
# Discrtization of the parameter tau_1
tau_1 = -0.6
# Discrtization of the parameter w1
w1 = 5.5

# DISCRETIZATION OF L_comp
L_comp_N = 12
L_comp_max = 8*1.5
L_comp_min = 8*0.5

# Folder Management Settings
Project_Name = "Database_L_comp_00"
Project_Folder = "D:\\Davide"
postproc_filename = "postprocessing.txt"
################################################################################################################
# Valid only for Database_tau_w1_betacurve.py
L_comp = np.linspace(L_comp_min, L_comp_max, L_comp_N)
######################################################################################

data =  { i: {"L_comp": L_comp_i,"Results":None} #The "Results" string at the end is where the results will be stored (Still to be implemented), while the first one is the index
                    for i,L_comp_i in enumerate(L_comp)}

Simulations_list = list_folders(f"{Project_Folder}\\{Project_Name}\\Simulations")

for sim in Simulations_list:
    print(f"Simulation: {sim}")
    idx = int(sim.split('_')[1])
    txt_file_path = f"{Project_Folder}\\{Project_Name}\\Simulations\\{sim}\\{sim}_files\\dp0\\CFX\\CFX\\{postproc_filename}"
    with open(txt_file_path, 'r') as file:
        lines = file.readlines()

        BBB_P0_S1 = None
        BBB_P0_S5 = None
        BBB_h0_S1 = None
        BBB_h0_S5 = None

        for line in lines:
            if line.startswith("BBB P0 S1"):
                BBB_P0_S1 = float(line.split(",")[1].strip().split(" ")[0]) #kg m^-1 s^-2
            elif line.startswith("BBB P0 S5"):
                BBB_P0_S5 = float(line.split(",")[1].strip().split(" ")[0]) #kg m^-1 s^-2
            elif line.startswith("BBB h0 S1"):
                BBB_h0_S1 = float(line.split(",")[1].strip().split(" ")[0]) #m^2 s^-2
            elif line.startswith("BBB h0 S5"):
                BBB_h0_S5 = float(line.split(",")[1].strip().split(" ")[0]) #m^2 s^-2

        print(f"BBB P0 S1: {BBB_P0_S1} Pa")
        print(f"BBB P0 S5: {BBB_P0_S5} Pa")
        print(f"BBB h0 S1: {BBB_h0_S1} J/kg")
        print(f"BBB h0 S5: {BBB_h0_S5} J/kg")

        pressure_ratio = BBB_P0_S5/BBB_P0_S1

        data[idx]["Results"] = {"P_0_S1": BBB_P0_S1, "P_0_S5": BBB_P0_S5, "h_0_S1": BBB_h0_S1, "h_0_S5": BBB_h0_S5,"Pressure_Ratio": pressure_ratio}

        
save_json(f"{Project_Folder}\\{Project_Name}\\RESULTS_Database_L_comp_00.json", data)

