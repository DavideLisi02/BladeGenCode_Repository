from plot_utils import *
import os
import matplotlib.pyplot as plt
import numpy as np

#####################################################################################################################################################
File = "RESULTS_Database_tau_w1_betacurve.json"
#####################################################################################################################################################

# Change the working directory to the one of the current file
os.chdir(os.path.dirname(os.path.abspath(__file__)))

data = read_json_file(File)

# Extract data for plotting
w1_values = sorted(set(data[key]['w1'] for key in data.keys()))

for w1 in w1_values:
    tau_0 = []
    tau_1 = []
    pressure_ratio = []
    
    for key in data.keys():
        if data[key]['w1'] == w1:
            tau_0.append(data[key]['tau_0'])
            tau_1.append(data[key]['tau_1'])
            pressure_ratio.append(data[key]['Results']['Pressure_Ratio'])
    # Convert lists to numpy arrays and reshape for plot_2d
    results = np.array([tau_0, tau_1, pressure_ratio]).T
    print(results)
    labels = ["tau_0", "tau_1", "Pressure Ratio"]
    plt.figure(f"w1 = {w1}", figsize=(8, 6))  # Set the figure size to be smaller
    plot_2d(results, labels)
    plt.show()
    filename = f"{File}_w1_{w1}.png"
    plt.savefig(filename)
    plt.close()
