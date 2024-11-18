import os

abspath = os.path.abspath(__file__)
package_path = os.path.dirname(abspath)
os.chdir(package_path)

import CFXbatch
from simulationParameters import *

# Folder Management Settings
Project_Name = "Database_Test_2"
Project_Folder = "D:\\Davide"
gemoetry_name = "LUS"
std_ANSYS_Folder_settings = "C:\\Program Files\\ANSYS Inc\\v242"


simulation_definition = create_simulation_def(ansys_path = std_ANSYS_Folder_settings,
                                            simulation_path = f"{Project_Folder}\\{Project_Name}",
                                            case_name = 'simulation1',
                                            geometry_name = gemoetry_name,
                                            n_channels = 9)

CFXbatch.run_CFXbatch(simulation_definition)

