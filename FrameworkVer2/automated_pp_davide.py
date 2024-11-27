import subprocess
import threading
import os
import csv

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

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

ansys_path = r"C:\Program Files\ANSYS Inc\v241"
exe_path = ansys_path + r"\CFD-Post\bin\cfdpost.exe"

postproc_filename = "postprocessing.txt"

address_file = r"address_list.txt"
state_file = r"postprocessing4calibration1D_candidacy.cst"
expression_file = r"expressionlist4calibration1D.txt"

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