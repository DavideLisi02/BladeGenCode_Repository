import os
import Folder_management
import threading

abspath = os.path.abspath(__file__)
package_path = os.path.dirname(abspath)
os.chdir(package_path)

import CFXbatch
from simulationParameters import *

####################################################################################
####################################################################################

#! Number of parallel simulations
batch_size = 5

#! Folder Management Settings
Project_Name = "Database_Test_14"
Project_Folder = "D:\\Davide" # Absolute path of the project folder created for the geometries
number_of_channels = 9
std_ANSYS_Folder_settings = "C:\\Program Files\\ANSYS Inc\\v242"

####################################################################################
####################################################################################

names = Folder_management.copy_bgd_for_simulation(f"{Project_Folder}\\{Project_Name}\\{Folder_management.output_bgdfolder_settings}", f"{package_path}\\CFXsetup_files\\geometry_turbocompressor_database")

def run_simulation(name):
    simulation_definition = create_simulation_def(ansys_path = std_ANSYS_Folder_settings,
                                                simulation_path = f"{Project_Folder}\\{Project_Name}\\{Folder_management.output_simulation_folder}",
                                                case_name = name,
                                                geometry_name = name,
                                                n_channels = number_of_channels)

    CFXbatch.run_CFXbatch(simulation_definition)



print(f"Number of geometries: {len(names)}")
Go_on = input(f"Are you sure you want to run {len(names)} simulations? Y/n > ")

# If user confirms the simulations
if Go_on.lower() == 'y':
    threads = []
    i = 0  
    
    # Loop through the names list, processing 5 simulations at a time
    while i < len(names):
        # Create threads for the next batch of 5 simulations
        for j in range(i, min(i + batch_size, len(names))):
            print(f"############## > Simulation {i+j} < ##############")
            thread = threading.Thread(target=run_simulation, args=(names[j],))
            threads.append(thread)
            thread.start()
        
        # Wait for the batch of threads to finish before starting the next batch
        for thread in threads[i:min(i + batch_size, len(names))]:
            thread.join()
        
        # Move to the next batch
        i += batch_size

    print("All simulations have been completed.")
else:
    print("Simulation aborted.")