import numpy as np
from Folder_management import *

# Beta at inlet and outlet from 1D
beta_in_settings = 24.008 # (beta_2, beta in corrispondenza dell'hub all'inlet)
beta_out_settings = 35.15 # (beta_4, beta in corrispondenza dell'hub all'outlet)

# HUB AND SHROUD PARAMETERS
# Geometrical Parameters from 1D
L_ind = 30 #30
L_comp = 8 #8
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
tau_0_N = 4 
tau_0_max = 0.7 #   0 < tau_0_max < 1      and     tau_0_max > tau_0_min
tau_0_min = 0.3 #   0 < tau_0_min < 1      and     tau_0_min < tau_0_min
# Discrtization of the parameter tau_1
tau_1_N = 4
tau_1_max = -0.3  # 2 to have P1 at beta_ou + delta
tau_1_min = -0.7  # - 1 to have P1 at bet_in - delta
# Discrtization of the parameter w1
w1_N = 3 
w1_min = 1
w1_max = 10 

# Folder Management Settings
Project_Name = "Database_tau_w1_betacurve"
Project_Folder = "D:\\Davide"
postproc_filename = "postprocessing.txt"
################################################################################################################
# Valid only for Database_tau_w1_betacurve.py
tau_0 = np.linspace(tau_0_min, tau_0_max, tau_0_N)
tau_1 = np.linspace(tau_1_min, tau_1_max, tau_1_N)
w1 = np.linspace(w1_min, w1_max, w1_N)
######################################################################################

HubShroud_1D_dimensions = {'object':'HubShroud', 'HubShr_bezier_N':HubShr_bezier_N, 'definition':'xz', 'spline_degree':2, 'L_ind':L_ind,'L_comp':L_comp, 'r2s':r2s, 'r2h':r2h, 'r4':r4, 'b4':b4, 'r5':r5, 'w1_hb':w1_hb, 'w1_sh':w1_sh}

data = { (i * tau_1_N * w1_N) + (j * w1_N) + k : {"tau_0": tau_0_ijk, "tau_1": tau_1_ijk, "w1":w1_ijk,"Results":None} #The "Results" string at the end is where the results will be stored (Still to be implemented), while the first one is the index
                    for i,tau_0_ijk in enumerate(tau_0)
                    for j,tau_1_ijk in enumerate(tau_1)
                    for k,w1_ijk in enumerate(w1) }

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

        print(f"BBB P0 S1: {BBB_P0_S1}")
        print(f"BBB P0 S5: {BBB_P0_S5}")
        print(f"BBB h0 S1: {BBB_h0_S1}")
        print(f"BBB h0 S5: {BBB_h0_S5}")

        # Calculate pressure ratio
        pr_ratio = BBB_P0_S5/BBB_P0_S1

        # Missing efficiency !!!!!!!!!!!!!!!!!!!

        data[idx]["Results"] = {"P_0_S1":BBB_P0_S1, "P_0_S5":BBB_P0_S5, "h_0_S1":BBB_h0_S1, "h_0_S5":BBB_h0_S5, "Pressure_Ratio":pr_ratio}

        
save_json(f"{Project_Folder}\\{Project_Name}\\RESULTS_Database_tau_w1_betacurve.json", data)

