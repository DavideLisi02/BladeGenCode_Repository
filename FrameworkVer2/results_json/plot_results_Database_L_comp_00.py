from plot_utils import *
import os
import matplotlib.pyplot as plt
import numpy as np
from CoolProp.CoolProp import PropsSI
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import Normalize
#http://www.coolprop.org/coolprop/HighLevelAPI.html#parameter-table

#####################################################################################################################################################
File = "RESULTS_Database_L_comp_00.json"
#####################################################################################################################################################

# Change the working directory to the one of the current file
os.chdir(os.path.dirname(os.path.abspath(__file__)))

data = read_json_file(File)

# Calculate efficiency
fluid_name = 'R134a'
for key in data.keys():
    
    BBB_P0_S1 = data[key]['Results']['P_0_S1']
    BBB_P0_S5 = data[key]['Results']['P_0_S5']
    BBB_h0_S1 = data[key]['Results']['h_0_S1']
    BBB_h0_S5 = data[key]['Results']['h_0_S5']

    entropy_1 = PropsSI('S', 'P', BBB_P0_S1, 'H', BBB_h0_S1, fluid_name)
    BBB_h0iso_5 = PropsSI('H', 'P', BBB_P0_S5, 'S', entropy_1, fluid_name)

    # Efficiency 0-to-0
    efficiency = (BBB_h0_S1 - BBB_h0iso_5)/(BBB_h0_S1 - BBB_h0_S5)
    data[key]["Results"]["Efficiency_0t0"] = efficiency

plotted_features = ["Pressure_Ratio", "Efficiency_0t0"]

L_comp = [data[key]['L_comp'] for key in data.keys()]
efficiency = [data[key]['Results']['Efficiency_0t0'] for key in data.keys()]
pressure_ratio = [data[key]['Results']['Pressure_Ratio'] for key in data.keys()]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Plot Efficiency as a function of L_comp
ax1.plot(L_comp, efficiency, marker='o')
ax1.set_xlabel("L_comp", fontsize=8)
ax1.set_ylabel("Efficiency_0t0", fontsize=8)
ax1.set_title("Efficiency as a function of L_comp", fontsize=10)
ax1.grid(True)
ax1.tick_params(axis='both', which='major', labelsize=6)

# Plot Pressure Ratio as a function of L_comp
ax2.plot(L_comp, pressure_ratio, marker='o')
ax2.set_xlabel("L_comp", fontsize=8)
ax2.set_ylabel("Pressure Ratio", fontsize=8)
ax2.set_title("Pressure Ratio as a function of L_comp", fontsize=10)
ax2.grid(True)
ax2.tick_params(axis='both', which='major', labelsize=6)

plt.tight_layout()
plt.show()
