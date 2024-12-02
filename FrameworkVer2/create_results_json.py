import json
import os

import subprocess
import threading
import os
import csv

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

def read_json_file(file_path):
    """
    Reads a JSON file and returns its content as a dictionary.
    
    :param file_path: Path to the JSON file.
    :return: Dictionary containing the JSON file content.
    """
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def read_txt_file(file_path):
    """
    Reads a text file and returns its content as a list of lines.
    
    :param file_path: Path to the text file.
    :return: List of lines from the text file.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return lines



def list_folders(directory_path):
    """
    Lists all folders inside the given directory.
    
    :param directory_path: Path to the directory.
    :return: List of folder names inside the directory.
    """
    return [name for name in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, name))]


def send_commands(process, commands):
    for command in commands:
        print(f'>>>  {command}')
        process.stdin.write(command + "\n")
        process.stdin.flush()

def read_output(process):
    while True:
        output_line = process.stdout.readline()
        if not output_line:
            break
        print(output_line.strip())

def list_elements(file_path):
# given a comma separated file at "file_path", the function retrieves all the elements contained and returns the first one of each line

    # Initialize an empty list to store the data
    data = []

    # Open the CSV file and read its content
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        
        # Iterate over each row in the CSV file
        for row in reader:
            data.append(row)
    
    res = []
    for row in data:
        res.append(row[0])

    return res

def append_text(template_file, new_file,trigger_strings, replacement_text):

    replacement_text = replacement_text+"\n"

    # Read the contents of the file
    with open(template_file, 'r') as file:
        lines = file.readlines()

    modified_lines = []
    jump = False
    for line in lines:
        if(jump==False):
            flag = True
            for trigger_string in trigger_strings:
                if flag == True and line.rstrip().startswith(trigger_string):
                    modified_lines.append(trigger_string+replacement_text)
                    flag = False
                    jump = line.rstrip().endswith("\\")
            if flag == True:
                modified_lines.append(line)
        else:
            jump = False

    with open(new_file, 'w') as file:
        file.writelines(modified_lines)

def replace_text(template_file, new_file,trigger_strings, replacement_text):

    replacement_text = replacement_text+"\n"

    # Read the contents of the file
    with open(template_file, 'r') as file:
        lines = file.readlines()

    modified_lines = []
    jump = False
    for line in lines:
        if(jump==False):
            flag = True
            for trigger_string in trigger_strings:
                if flag == True and line.rstrip().startswith(trigger_string):
                    modified_lines.append(replacement_text)
                    flag = False
                    jump = line.rstrip().endswith("\\")
            if flag == True:
                modified_lines.append(line)
        else:
            jump = False
    with open(new_file, 'w') as file:
        file.writelines(modified_lines)

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

Project_Name = "Database_tau_w1_betacurve"
Project_Folder = "D:\\Davide"

#####################################################################################################################################################

ansys_path = r"C:\Program Files\ANSYS Inc\v242"
exe_path = ansys_path + r"\CFD-Post\bin\cfdpost.exe"

postproc_filename = "postprocessing.txt"

Results_dict = read_json_file(f"{Project_Folder}\\{Project_Name}\\simulation_results.json")
Simulations_list = list_folders(f"{Project_Folder}\\{Project_Name}\\Simulations")

Go_on = input(f"Found {len(Simulations_list)} simulations. Do you want to continue? Y/n > ")

if Go_on.lower() == 'y':
    
    address_file = f"D:\Davide\BladeGenCode_Repository\FrameworkVer2\results_uitls\{Project_Name}.txt"
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
    
    print(f"\n-----------------------------------------------------\nPost-processing completed\nComputing Efficiency and Pressure ratio\n")

    data = read_json_file(f"{Project_Folder}\\{Project_Name}\\simulation_results.json")

    for sim in Simulations_list:
        print(f"Simulation: {sim}")
        idx = sim.split('_')[1]
        txt_file_path = f"{Project_Folder}\\{Project_Name}\\Simulations\\{sim}\\{sim}_files\\dp0\\CFX\\CFX\\{postproc_filename}"
        with open(txt_file_path, 'r') as file:
            lines = file.readlines()

            BBB_P0_S1 = None
            BBB_P0_S5 = None
            BBB_h0_S1 = None
            BBB_h0_S5 = None

            for line in lines:
                if line.startswith("BBB P0 S1"):
                    BBB_P0_S1 = float(line.split(",")[1].strip().split(" ")[0]) #kg m^-1 s^-2
                elif line.startswith("BBB P0 S5"):
                    BBB_P0_S5 = float(line.split(",")[1].strip().split(" ")[0]) #kg m^-1 s^-2
                elif line.startswith("BBB h0 S1"):
                    BBB_h0_S1 = float(line.split(",")[1].strip().split(" ")[0]) #m^2 s^-2
                elif line.startswith("BBB h0 S5"):
                    BBB_h0_S5 = float(line.split(",")[1].strip().split(" ")[0]) #m^2 s^-2

            print(f"BBB P0 S1: {BBB_P0_S1}")
            print(f"BBB P0 S5: {BBB_P0_S5}")
            print(f"BBB h0 S1: {BBB_h0_S1}")
            print(f"BBB h0 S5: {BBB_h0_S5}")

            # Calculate pressure ratio
            pr_ratio = BBB_P0_S5/BBB_P0_S1

            # Missing efficiency !!!!!!!!!!!!!!!!!!!

            data[idx][1] = {"P_0_S1":BBB_P0_S1, "P_0_S5":BBB_P0_S5, "h_0_S1":BBB_h0_S1, "h_0_S5":BBB_h0_S5, "Pressure_Ratio":pr_ratio}

            




