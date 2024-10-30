import os
import json
import subprocess
import re

class Geometry:

    def __init__(self,
                 parameters, # Parameters object, see ParametrizationSettings in Parameters.py
                 curves, # Curve object, see Bezier in Bezier.py
                 defaultfilePath ='defaultBGI\\geometry00.bgi', # Path of the starting bgi model to modify
                 output_jsonPath = 'modifiedJSON\\MODgeometry00.json',
                 output_bgiPath = 'modifiedBGI\\MODgeometry00.bgi',
                 output_bgdPath = 'modifiedBGD\\MODgeometry00.bgd',
                 std_ANSYS_Folder = "c:\\Program Files\\ANSYS Inc",
                **kwargs):
        """
        Class containing all functions and data about a specific .bgi file
        """
        super(Geometry, self).__init__()
        
        self.object = parameters.object
        self.definition = parameters.definition
        self.parameters = parameters
        self.curves = curves
        
        self.defaultfilePath = defaultfilePath
        self.output_jsonPath = output_jsonPath
        self.output_bgiPath = output_bgiPath
        self.output_bgdPath = output_bgdPath

        self.std_ANSYS_Folder = std_ANSYS_Folder

        return

    def readfile(self, filePath = 'defaultBGI\geometry00.bgi'):
        with open(filePath, 'r') as file:
            DataList = file.readlines()
        return DataList

    def convert_list_to_dict(self, list):
        """
        Converts the list of lines from the .bgi file into a structured dictionary.
        This version supports infinitely nested subsections using a stack,
        including handling multiple segments under a subsection.
        """
        data_dict = {}
        stack = []  # Stack to handle nested sections/subsections
        current_data = []  # For storing (x, y) or other data points
        current_subsection = None  # To track the current subsection
        subsection_counters = {}  # Track counters for repeated subsection names
        BladeCounter = 0

        for line in list:
            line = line.strip()
            print(f"Analyzed line = #{line}#")

            if line.startswith("Begin"):
                section_name = line.split()[1]
                new_section = {}
                if stack:
                    # Add the new section to the current section at the top of the stack
                    parent_section = stack[-1]

                    # Handle cases like 'SpanLayer' with multiple instances
                    if section_name in parent_section:
                        if section_name not in subsection_counters:
                            subsection_counters[section_name] = 1
                        subsection_counters[section_name] += 1
                        section_name_with_index = f"{section_name}{subsection_counters[section_name]}"
                    else:
                        section_name_with_index = section_name
                        subsection_counters[section_name] = 1

                    parent_section[section_name_with_index] = new_section
                else:
                    # This is a top-level section
                    data_dict[section_name] = new_section
                stack.append(new_section)  # Push the new section onto the stack
                current_subsection = None  # Reset current_subsection on new section

            elif line.startswith("End"):
                if current_data and stack:
                    # Store the current data into the section at the top of the stack
                    parent_section = stack[-1]
                    if "data" not in parent_section:
                        parent_section["data"] = []  # Initialize data list
                    parent_section["data"].extend(current_data)  # Append data to the "data" key
                    current_data = []
                # Pop the section off the stack when it ends
                stack.pop()
                if stack:  # Reset current_subsection when not at the top level
                    current_subsection = None

            elif "=" in line:
                # Handle key=value lines
                key, value = line.split("=", 1)
                if stack:
                    # Add the key-value pair to the current section
                    current_section = stack[-1]
                    current_section[key.strip()] = value.strip()
                else:
                    print(f"Warning: Key-value pair found outside of any section: {line}")

            elif "(" in line and ")" in line:
                # Handle data points in the form (x, y)
                # Extract and convert the (x, y) points to tuples of floats
                point = re.findall(r"\((.*?)\)", line)[0]
                x, y = map(float, point.split(','))
                current_data.append((x, y))

            elif "New" in line:
                if "Blade" in line:
                    section_name = f"{line.split()[1]}{BladeCounter}"
                    BladeCounter +=1
                    new_section = {}
                    if stack:
                        # Add the new section to the current section at the top of the stack
                        parent_section = stack[-1]

                        # Handle cases like 'SpanLayer' with multiple instances
                        if section_name in parent_section:
                            if section_name not in subsection_counters:
                                subsection_counters[section_name] = 1
                            subsection_counters[section_name] += 1
                            section_name_with_index = f"{section_name}{subsection_counters[section_name]}"
                        else:
                            section_name_with_index = section_name
                            subsection_counters[section_name] = 1

                        parent_section[section_name_with_index] = new_section
                    else:
                        # This is a top-level section
                        data_dict[section_name] = new_section
                    stack.append(new_section)  # Push the new section onto the stack
                    current_subsection = None  # Reset current_subsection on new section
                else:
                    # Handle new subsections (e.g., New Segment, New AngleCurve, etc.)
                    subsection_name = line
                    new_subsection = {}
                    if stack:
                        # Add the new subsection to the current section at the top of the stack
                        current_section = stack[-1]
                        if subsection_name not in current_section:
                            current_section[subsection_name] = []  # Initialize list for multiple segments
                        current_section[subsection_name].append(new_subsection)  # Add new subsection
                    stack.append(new_subsection)  # Push the new subsection onto the stack
                    current_subsection = subsection_name  # Track the current subsection

            elif line == '':
                # Ignore empty lines
                continue

            else:
                # Handle any other plain lines
                if stack:
                    # Add the line to the current section as a key with a value of None
                    current_section = stack[-1]
                    current_section[line] = None
                else:
                    print(f"Warning: Unrecognized line found outside of any section: {line}")

        return data_dict

    def modify_dict(self, object, definition, curve_points_list, data_dict):
        '''
        Modifies the default geometry, descripted in a json file, accordingly to
        the object and the definition of the parametrization by inserting the curve data points 
        in a new json file which is the output of the function
        '''
        modified_Dict = data_dict
        if object == "Blade" and definition == 'beta-M%':
            for layer in range(0,5): #To implement later: modify more layers differently
                modified_Dict["Blade0"]["AngleDefinition"]["New AngleCurve"][layer]["New Segment"][0]["Data"]["data"][0] = curve_points_list #Blade0 (Layer1)
        return modified_Dict
    
    def save_json(self, output_jsonPath, data_dict):
        """
        Saves the dictionary into a JSON file.
        """
        with open(output_jsonPath, 'w') as json_file:
            json.dump(data_dict, json_file, indent=4)
        return

    def convert_json_to_bgi(self, output_jsonPath, output_bgiPath):
        """
        Reads a JSON file and converts it into a .bji format
        that preserves specific formatting.
        Formatting Hints:
        If a key's value is None, only the key is written without '=' or 'None'.
        Points are written as (x.xx, y.yy).
        """
        with open(output_jsonPath, 'r') as file:
            json_data = json.load(file)

        with open(output_bgiPath, 'w') as file:
            def write_bji(data, indent_level=0):
                indent = '    ' * indent_level  # Use 4 spaces for indentation
                if isinstance(data, dict):
                    # Iterate over key-value pairs in dictionaries
                    for key, value in data.items():
                        if isinstance(value, dict):
                            if key in ["Case","PlusData"]:
                                # Handle nested sections (dictionaries)
                                file.write(f"Begin {key}\n")
                                write_bji(value, 0)
                                file.write(f"End {key}\n\n")
                            else:    
                                # Handle nested sections (dictionaries)
                                if "Blade" in key:
                                    name_key = key[:-1]
                                else:
                                    name_key = key
                                file.write(f"{indent}New {name_key}\n")
                                write_bji(value, indent_level + 1)
                                if key == "Data":
                                    file.write(f"{indent}End {name_key}\n")  # Add a blank line after the section
                                else:
                                    file.write(f"{indent}End {name_key}\n\n")

                                    
                        elif isinstance(value, list):
                            # Handle lists of subsections or multiple entries like SpanLayer
                            for item in value:
                                if isinstance(item, dict):
                                    if key.startswith("New"):
                                        # Handle subsections like 'New Segment'
                                        file.write(f"{indent}{key}\n")
                                        write_bji(item, indent_level + 1)
                                        file.write(f"{indent}End {key.split()[1]}\n")  # End <subsection>
                                    else:
                                        # Handle regular sections in a list (e.g., SpanLayer1, SpanLayer2)
                                        file.write(f"{indent}Begin {key}\n")
                                        write_bji(item, indent_level + 1)
                                        file.write(f"{indent}End {key}\n")
                                else:
                                    # If item is not a dictionary, just write the list content
                                    if key == 'data':
                                        item = tuple(item)
                                        file.write(f"{indent}{item}\n")
                                    else:
                                        file.write(f"{indent}{item}\n")

                        elif value is None:
                            # If the value is None, just write the key without '=' or 'None'
                            file.write(f"{indent}{key}\n")

                        else:
                            # Handle key-value pairs with normal values
                            file.write(f"{indent}{key}={value}\n")

                elif isinstance(data, list):
                    # If for some reason a raw list is passed, handle it (this should be rare)
                    for item in data:
                        file.write(f"{indent}{item}\n")

            write_bji(json_data)

    def convert_bgi_to_bgd(self, output_bgiPath, output_bgdPath, ANSYSfolderPath = "c:\\Program Files\\ANSYS Inc"):
        '''
        Runs terminal's commands to execute BladeBatch from BladeGen in order to run
        the .bgi file and obtain a .bgd
        '''

        # Setting the path for the ANSYS folder
        path_command = f'set path=%path%;{ANSYSfolderPath}\\v110\\AISOL\\BladeModeler\\BladeGen'
        
        # Prepare the command to run BladeBatch
        blade_batch_command = f'BladeBatch {output_bgiPath} {output_bgdPath}'
        
        # Combine commands into a single command string for the terminal
        full_command = f'cmd /c "{path_command} && {blade_batch_command}"'
        
        # Run the command in the terminal
        result = subprocess.run(full_command, shell=True, capture_output=True, text=True)

        # Print the output and errors (if any)
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)

        # Check if the command was successful
        if result.returncode == 0:
            print("Conversion bgi->bgd completed successfully.")
            return True
        else:
            print("An error occurred during the conversion bgi->bgd.")
            return None

    def create_modified_geometry(self):
        DataList = self.readfile(filePath =  self.defaultfilePath)
        DataDict = self.convert_list_to_dict(DataList)
        ModDataDict = self.modify_dict(self.object, self.definition, self.curves.points, DataDict)
        self.save_json(self.output_jsonPath, ModDataDict)
        self.convert_json_to_bgi(self.output_jsonPath, self.output_bgiPath)
        self.convert_bgi_to_bgd(self.output_bgiPath, self.output_bgdPath, ANSYSfolderPath = self.std_ANSYS_Folder)
        return
    
    def create_unmodified_json_geometry(self):
        DataList = self.readfile(filePath = self.defaultfilePath)
        print(DataList)
        DataDict = self.convert_list_to_dict(DataList)
        self.save_json(self.output_jsonPath, DataDict)
        return
    
    def create_unmodified_bgi_geometry(self):
        DataList = self.readfile(filePath =  self.defaultfilePath)
        UnModDataDict = self.convert_list_to_dict(DataList)
        self.save_json(self.output_jsonPath, UnModDataDict)
        self.convert_json_to_bgi(self.output_jsonPath, self.output_bgiPath)
        self.convert_bgi_to_bgd(self.output_bgiPath, self.output_bgdPath, ANSYSfolderPath = self.std_ANSYS_Folder)
        return