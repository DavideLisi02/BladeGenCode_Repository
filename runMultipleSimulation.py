import os
import Folder_management

abspath = os.path.abspath(__file__)
package_path = os.path.dirname(abspath)
os.chdir(package_path)

import CFXbatch
from simulationParameters import *

####################################################################################
####################################################################################

#! Folder Management Settings
Project_Name = "Database_Test_2"
Project_Folder = "D:\\Davide" # Absolute path of the project folder created for the geometries
number_of_channels = 9
std_ANSYS_Folder_settings = "C:\\Program Files\\ANSYS Inc\\v242"

####################################################################################
####################################################################################

names = Folder_management.copy_bgd_for_simulation(f"{Project_Folder}\\{Project_Name}\\{Folder_management.output_bgdfolder_settings}", f"{package_path}\\CFXsetup_files\\geometry_turbocompressor_database")

for name in names:

    simulation_definition = create_simulation_def(ansys_path = std_ANSYS_Folder_settings,
                                                simulation_path = f"{Project_Folder}\\{Project_Name}\\{Folder_management.output_simulation_folder}",
                                                case_name = name,
                                                geometry_name = name,
                                                n_channels = number_of_channels)

    CFXbatch.run_CFXbatch(simulation_definition)