import json
import os

import subprocess
import threading
import os
import csv
from Folder_management import *

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#####################################################################################################################################################
# insert: 
# 1. exe_path: address of cfd-post executable 
# 2. state_file: session file containing the post-processing operations to replicate in other solution files 
# 3. address_file: file containing the addresses of the solution files 
# 4. expression_file: file containing the expression names of the quantities evaluated in the customized post-processing (session file)
# 5. state_filename: CFX state file name to use when saving post-processing on other solutions
# 6. postproc_filename: txt file name to use when saving post-processing on other solutions

   
#! exe_path: address of cfd-post executable 

#####################################################################################################################################################

Project_Name = "Database_L_comp_00"
Project_Folder = "D:\\Davide"

#####################################################################################################################################################

ansys_path = r"C:\Program Files\ANSYS Inc\v242"
exe_path = ansys_path + r"\CFD-Post\bin\cfdpost.exe"

postproc_filename = "postprocessing.txt"

Results_dict = read_json_file(f"{Project_Folder}\\{Project_Name}\\simulation_results_L_comp.json")
Simulations_list = list_folders(f"{Project_Folder}\\{Project_Name}\\Simulations")
print(f"Simulations found:\n{Simulations_list}")
Go_on = input(f"Found {len(Simulations_list)} simulations. Do you want to continue? Y/n > ")

if Go_on.lower() == 'y':
    
    address_file = f"D:\\Davide\\BladeGenCode_Repository\\FrameworkVer2\\results_uitls\\{Project_Name}.txt"
    
    with open(address_file, 'a') as file:
        for sim in Simulations_list:
            print(f"Simulation: {sim}")
            file.write(f"{Project_Folder}\\{Project_Name}\\Simulations\\{sim}\\{sim}_files\\dp0\\CFX\\CFX\\CFXpre_case_001.res\n")
    

    state_file = r"D:\Davide\BladeGenCode_Repository\FrameworkVer2\results_uitls\postprocessing4calibration1D_candidacy.cst"
    expression_file = r"D:\Davide\BladeGenCode_Repository\FrameworkVer2\results_uitls\expressionlist4calibration1D.txt"

    solution_addresses = list_elements(address_file)
    expression_names = list_elements(expression_file)

    #####################################################################################################################################################

    state_file = state_file.replace(os.sep, '/')

    for i in range(len(solution_addresses)):
        solution_addresses[i] = solution_addresses[i].replace(os.sep, '/')
        
    # defining commands to submit to the CFX environment
    cfx_commands = []
    flag_state = True
    count = 0
    for solution_address in solution_addresses:
        count += 1
        # cfx_commands.extend(["load filename=%s, force_reload=true"%solution_address,
        #                     "readsession filename=%s"%state_file,
        #                     "savestate mode=overwrite,filename=%s/%s"%(os.path.dirname(solution_address),state_filename)])
        cfx_commands.append("load filename=%s, force_reload=true"%solution_address)
        if(flag_state == True):
            append_text(state_file, os.path.dirname(solution_address)+'\postprocessing.cst',["    Current Case Name = ","    Current Results File = ","  Current Case Name = ","  Current Results File = "], solution_address)
            cfx_commands.append("readstate filename=%s"%(os.path.dirname(solution_address)+'/postprocessing.cst'))
            cfx_commands.append("load filename=%s, force_reload=true"%solution_address)
            flag_state = False
        # cfx_commands.append("readsession filename=%s"%(os.path.dirname(solution_address)+'/export_streamlines.cse'))
        cfx_commands.append("!open(OUT, '>%s/%s');"%(os.path.dirname(solution_address),postproc_filename))

        for expression_name in expression_names:
            cfx_commands.extend(["!$var_name = '%s';"%expression_name,
                                "!$var_value = getExprString($var_name);",
                                "!print OUT qq($var_name, $var_value\\n);"])

        cfx_commands.append("!close(OUT);")
    cfx_commands.append("quit")


    # #####################################################################################################################################################

    # Open the subprocess to access CFX environment
    try:
        process = subprocess.Popen([exe_path, '-line'], 
                                stdin=subprocess.PIPE, 
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.PIPE, 
                                text=True)
    except Exception as e:
        raise Exception(f"Error launching {exe_path}: {e}")

    # Create separate threads for sending commands and reading output
    send_thread = threading.Thread(target=send_commands, args=(process, cfx_commands))
    read_thread = threading.Thread(target=read_output, args=(process,))

    # Start the threads
    send_thread.start()
    read_thread.start()

    # Wait for both threads to finish
    send_thread.join()
    read_thread.join()

    # Wait for the subprocess to finish
    process.wait()
    
    print(f"\n-----------------------------------------------------\nPost-processing completed")

