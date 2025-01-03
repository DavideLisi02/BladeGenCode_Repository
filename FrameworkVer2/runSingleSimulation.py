import os
import Folder_management

abspath = os.path.abspath(__file__)
package_path = os.path.dirname(abspath)
os.chdir(package_path)

import CFXbatch
from simulationParameters import *
from datetime import datetime

####################################################################################
####################################################################################

#! Folder Management Settings
Project_Name = "Database_tau_w1_betacurve"
Project_Folder = "D:\\Davide"
geometry_name = "UNMODgeometry_1_03_-07_55"
number_of_channels = 9
std_ANSYS_Folder_settings = "C:\\Program Files\\ANSYS Inc\\v242"

####################################################################################
####################################################################################

simulation_definition = create_simulation_def(ansys_path = std_ANSYS_Folder_settings,
                                            simulation_path = f"{Project_Folder}\\{Project_Name}\\{Folder_management.output_simulation_folder}",
                                            case_name = geometry_name,
                                            geometry_name = geometry_name,
                                            n_partitions = 20, # number of cores
                                            n_channels = number_of_channels)

print(f"Simulation Definition:\n{simulation_definition}")

start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(f"Start Time: {start_time}")

CFXbatch.run_CFXbatch(simulation_definition)

end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(f"End Time: {end_time}")

start_time_dt = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
end_time_dt = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
total_time = (end_time_dt - start_time_dt).total_seconds() / 60

print(f"Total Time: {total_time:.2f} minutes")

print("Simulazione terminata")