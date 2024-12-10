from plot_utils import *
import os
import matplotlib.pyplot as plt
import numpy as np
from CoolProp.CoolProp import PropsSI

#####################################################################################################################################################
File = "RESULTS_Database_tau_w1_betacurve.json"
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

    print(f"BBB P0 S1: {BBB_P0_S1} Pa")
    print(f"BBB P0 S5: {BBB_P0_S5} Pa")
    print(f"BBB h0 S1: {BBB_h0_S1} J/kg")
    print(f"BBB h0 S5: {BBB_h0_S5} J/kg")

    entropy_1 = PropsSI('S', 'P', BBB_P0_S1, 'H', BBB_h0_S1, fluid_name)
    BBB_h0iso_5 = PropsSI('H', 'P', BBB_P0_S5, 'S', entropy_1, fluid_name)

    # Efficiency 0-to-0
    efficiency = (BBB_h0_S1 - BBB_h0iso_5)/(BBB_h0_S1 - BBB_h0_S5)
    data[key]["Results"]["Efficiency_0t0"] = efficiency



# Extract data for plotting
w1_values = sorted(set(data[key]['w1'] for key in data.keys()))

plotted_features = ["Pressure_Ratio", "Efficiency_0t0"]

for feature in plotted_features:
    for w1 in w1_values:
        tau_0 = []
        tau_1 = []
        pressure_ratio = []
        
        for key in data.keys():
            if data[key]['w1'] == w1:
                tau_0.append(data[key]['tau_0'])
                tau_1.append(data[key]['tau_1'])
                pressure_ratio.append(data[key]['Results'][feature])
        # Convert lists to numpy arrays and reshape for plot_2d
        results = np.array([tau_0, tau_1, pressure_ratio]).T
        print(results)
        labels = ["tau_0", "tau_1", feature]
        plt.figure(f"w1 = {w1}", figsize=(8, 6))  # Set the figure size to be smaller
        plot_2d(results, labels, feature)
        plt.show()
        filename = f"{File}_w1_{w1}.png"
        plt.savefig(filename)
        plt.close()
