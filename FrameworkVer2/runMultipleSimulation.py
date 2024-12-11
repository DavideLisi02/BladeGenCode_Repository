import os
import Folder_management
import threading
from datetime import datetime

abspath = os.path.abspath(__file__)
package_path = os.path.dirname(abspath)
os.chdir(package_path)

import CFXbatch
from simulationParameters import *

####################################################################################
####################################################################################

#! Parallel running?
parallel = False
#! Number of parallel simulations
batch_size = 5

#! Folder Management Settings
Project_Name = "Database_L_comp_00"
Project_Folder = "D:\\Davide" # Absolute path of the project folder created for the geometries
number_of_channels = 9
std_ANSYS_Folder_settings = "C:\\Program Files\\ANSYS Inc\\v242"

####################################################################################
####################################################################################

names = Folder_management.copy_bgd_for_simulation(f"{Project_Folder}\\{Project_Name}\\{Folder_management.output_bgdfolder_settings}", f"{package_path}\\CFXsetup_files\\geometry_turbocompressor_database")
print(names)
def run_simulation(name):
    simulation_definition = create_simulation_def(ansys_path = std_ANSYS_Folder_settings,
                                                simulation_path = f"{Project_Folder}\\{Project_Name}\\{Folder_management.output_simulation_folder}",
                                                case_name = name,
                                                geometry_name = name,
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




print(f"Number of geometries: {len(names)}")
Go_on = input(f"Are you sure you want to run {len(names)} simulations? Y/n > ")

# If user confirms the simulations
if Go_on.lower() == 'y':
    if parallel: # Set parallel to True to run simulations in parallel
        threads = []
        i = 0  
        
        # Loop through the names list, processing 5 simulations at a time
        while i < len(names):
            # Create threads for the next batch of 5 simulations
            for j in range(i, min(i + batch_size, len(names))):
                print(f"############## >      Simulation {i+j}    < ##############")
                thread = threading.Thread(target=run_simulation, args=(names[j],))
                threads.append(thread)
                thread.start()
            
            # Wait for the batch of threads to finish before starting the next batch
            for thread in threads[i:min(i + batch_size, len(names))]:
                print(f"############## >   Simulation Completed   < ##############")
                thread.join()
            
            # Move to the next batch
            i += batch_size

        print("All simulations have been completed.")
    else:
        i = 0
        for name in names:
            print(f"############## > Simulation {i}:{name} < ##############")
            run_simulation(name)
            print(f"Simulation {i} completed.")
            i+=1
else:
    print("Simulation aborted.")