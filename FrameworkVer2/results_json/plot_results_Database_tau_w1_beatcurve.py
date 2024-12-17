from plot_utils import *
import os
import matplotlib.pyplot as plt
import numpy as np
from CoolProp.CoolProp import PropsSI
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import Normalize
#http://www.coolprop.org/coolprop/HighLevelAPI.html#parameter-table

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
        labels = ["tau_0", "tau_1", feature]
        
        fig = plt.figure(figsize=(16, 6))
        
        # 2D plot
        ax1 = fig.add_subplot(121)
        plot_2d(results, labels, feature)
        plt.tick_params(axis='both', which='major', labelsize=6) #added tick labelsize

        # 3D plot
        ax2 = fig.add_subplot(122, projection='3d')
        norm = Normalize(vmin=0.7735, vmax=0.7790) if feature == "Efficiency_0t0" else Normalize(vmin=1.92, vmax=1.97) #added normalization and conditional vmin/vmax
        ax2.scatter(tau_0, tau_1, pressure_ratio, c=pressure_ratio, cmap='viridis', norm=norm) #added norm
        tau_0_grid, tau_1_grid = np.meshgrid(np.unique(tau_0), np.unique(tau_1))
        pressure_ratio_grid = griddata((tau_0, tau_1), pressure_ratio, (tau_0_grid, tau_1_grid), method='cubic')
        surf = ax2.plot_surface(tau_0_grid, tau_1_grid, pressure_ratio_grid, cmap='viridis', edgecolor='none', norm=norm) #added norm
        #Removed colorbar
        ax2.set_xlabel('tau_0', fontsize=8) #added fontsize
        ax2.set_ylabel('tau_1', fontsize=8) #added fontsize
        ax2.set_zlabel(feature, fontsize=8) #added fontsize
        ax2.set_title(f'3D plot of {feature} for w1 = {w1}', fontsize=10) #added fontsize
        plt.tick_params(axis='both', which='major', labelsize=6) #added tick labelsize
        
        plt.show()
        filename = f"{File}_w1_{w1}_3d.png"
        plt.savefig(filename)
        plt.close()
        
        if feature == "Efficiency_0t0":
            print(w1)
            if w1 == 5.5:   
                tau_0 = []
                efficiency = []
                for key in data.keys():
                    if data[key]['w1'] == w1 and data[key]['tau_1'] == -0.5666666666666667:
                        tau_0.append(data[key]['tau_0'])
                        efficiency.append(data[key]['Results']['Efficiency_0t0'])
                plt.figure("Efficiency vs tau_0 for w1 = 5.5 and tau_1 = -0.6", figsize=(8, 6))
                plt.plot(tau_0, efficiency, marker='o')
                plt.xlabel("tau_0", fontsize=8) #added fontsize
                plt.ylabel("Efficiency_0t0", fontsize=8) #added fontsize
                plt.title("Efficiency as a function of tau_0 for w1 = 5.5 and tau_1 = -0.6", fontsize=10) #added fontsize
                plt.grid(True)
                plt.tick_params(axis='both', which='major', labelsize=6) #added tick labelsize
                plt.show()
