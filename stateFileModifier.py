import os
import json
import subprocess
import re

class Geometry:

    def __init__(self,
                 parameters, # Parameters object, see ParametrizationSettings in Parameters.py
                 defaultfilePath ='defaultBGI\\geometry00.bgi', # Path of the starting bgi model to modify
                 output_jsonPath = 'modifiedJSON\\MODgeometry00.json',
                 output_bgiPath = 'modifiedBGI\\MODgeometry00.bgi',
                 output_unmodified_bgiPath = 'unmodifiedBGI\\UNMODgeometry00.bgi',
                 output_bgdPath = 'modifiedBGD\\MODgeometry00.bgd',
                 output_unmodified_bgdPath = 'unmodifiedBGD\\UNMODgeometry00.bgd',
                 std_ANSYS_Folder = "c:\\Program Files\\ANSYS Inc",
                **kwargs):
        """
        Class containing all functions and data about a specific .bgi file
        """
        super(Geometry, self).__init__()
        
        self.parameters = parameters
        
        self.defaultfilePath = defaultfilePath
        self.output_jsonPath = output_jsonPath
        self.output_bgiPath = output_bgiPath
        self.output_unmodified_bgiPath = output_unmodified_bgiPath
        self.output_bgdPath = output_bgdPath
        self.output_unmodified_bgdPath = output_unmodified_bgdPath

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
            if self.parameters.print_conversion_output:
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

    def modify_dict_numOfBlades(self, numOfBlades, modify_numOfBlades, data_dict):
        '''
        Modifies the default geometry, descripted in a json file, accordingly to
        the object and the definition of the parametrization by inserting the curve data points 
        in a new json file which is the output of the function.
        '''
        modified_Dict = data_dict
        if modify_numOfBlades:
            modified_Dict["Model"]["NumMainBlades"] = str(numOfBlades)
            return modified_Dict

    def modify_dict_blade(self, Blade_definition, curve_points_list_blade, data_dict, fibers):
        '''
        Modifies the default geometry, descripted in a json file, accordingly to
        the object and the definition of the parametrization by inserting the curve data points 
        in a new json file which is the output of the function.
        '''
        modified_Dict = data_dict
        if Blade_definition == 'beta-M%' and fibers == 'General_only_at_Hub':
            layers = [0]
            modified_Dict["Blade0"]["AngleDefinition"]['SpanwiseDistribution'] = 'General'
            for layer in layers:
                modified_Dict["Blade0"]["AngleDefinition"]["New AngleCurve"][layer]["New Segment"][0]["Data"]["data"] = curve_points_list_blade
                modified_Dict["Blade0"]["AngleDefinition"]["New AngleCurve"][layer]["DefinitionType"] = "BetaCurve"
                modified_Dict["Blade0"]["AngleDefinition"]["New AngleCurve"][layer]["HorizDim"] = "PercentMeridional"
        return modified_Dict
    
    def modify_dict_HubShroud(self, HubShroud_definition, data_dict):
        '''
        Modifies the default geometry, descripted in a json file, accordingly to
        the object and the definition of the parametrization by inserting the curve data points 
        in a new json file which is the output of the function.
        '''
        modified_Dict = data_dict
        if HubShroud_definition == 'xz':
            '''
            HubShroud_1D_dimensions = self.parameters['HubShroud_1D_dimensions']
            inducer_Hub_points = self.parameters['self.inducer_Hub_points']
            inducer_Shroud_points = self.parameters['inducer_Shroud_points']
            Hub_Shroud_curves_points = self.parameters['Hub_Shroud_curves_points']
            diffuser_Hub_points = self.parameters['diffuser_Hub_points']
            diffuser_Shroud_points = self.parameters['diffuser_Shroud_points']
            '''
            
            # Modifying Hub profile
            total_Hub_profile = self.parameters.total_Hub_profile

            modified_Dict["Meridional"]["HubCurve"]["New Segment"] = []
            
            for element in total_Hub_profile:
                if len(element) <= 10:
                    i = 0
                    while i in range(len(element)-1):
                        modified_Dict["Meridional"]["HubCurve"]["New Segment"].append({
                            "CurveType": "Spline",
                            "UpstreamControl": "Free",
                            "Data": {
                                "data": [ element[i] , element[i+1] ]
                            },
                            "DownstreamControl": "Free"
                        })
                        i+=1
                else:
                    modified_Dict["Meridional"]["HubCurve"]["New Segment"].append({
                        "CurveType": "Spline",
                        "UpstreamControl": "Free",
                        "Data": {
                            "data": element 
                        },
                        "DownstreamControl": "Free"
                    })

            
            # Modifying Shroud profile
            total_Shroud_profile = self.parameters.total_Shroud_profile
            
            modified_Dict["Meridional"]["ShroudCurve"]["New Segment"] = []
            
            j=0
            for element in total_Shroud_profile:
                if len(element) <= 10:
                    i = 0
                    while i in range(len(element)-1):
                        modified_Dict["Meridional"]["ShroudCurve"]["New Segment"].append({
                            "CurveType": "Spline",
                            "UpstreamControl": "Free",
                            "Data": {
                                "data": [ element[i] , element[i+1] ]
                            },
                            "DownstreamControl": "Free"
                        })
                        i+=1
                        j+=1
                else:
                    modified_Dict["Meridional"]["ShroudCurve"]["New Segment"].append({
                        "CurveType": "Spline",
                        "UpstreamControl": "Free",
                        "Data": {
                            "data": element 
                        },
                        "DownstreamControl": "Free"
                    })
                j+=1

            # Modifying inlet curve
            inlet_curve = self.parameters.inlet_curve
            modified_Dict["Meridional"]["InletCurve"]["New Segment"][0] = {
                        "CurveType": "Linear",
                        "Data": {
                            "data": inlet_curve 
                        },
                    }
            # Modifying exhaust curve
            exhaust_curve = self.parameters.exhaust_curve
            modified_Dict["Meridional"]["ExhaustCurve"]["New Segment"][0] = {
                        "CurveType": "Linear",
                        "Data": {
                            "data": exhaust_curve 
                        },
                    }
            
            # Modifying Leading Edge
            leading_edge_curve = self.parameters.leading_edge_curve
            modified_Dict["Meridional"]["LeadingEdgeCurve"]["New Segment"][0] = {
                        "CurveType": "Spline",
                        "UpstreamControl": "Free",
                        "Data": {
                            "data": leading_edge_curve 
                        },
                        "DownstreamControl": "Free"
                    }
            # Modifying Trailing Edge
            trailing_edge_curve = self.parameters.trailing_edge_curve
            modified_Dict["Meridional"]["TrailingEdgeCurve"]["New Segment"][0] = {
                        "CurveType": "Spline",
                        "UpstreamControl": "Free",
                        "Data": {
                            "data": trailing_edge_curve 
                        },
                        "DownstreamControl": "Free"
                    }

        return modified_Dict
    
    def modify_dict_thickness(self, thickness_curve, modify_Thickness, data_dict):
        '''
        Modifies the default geometry, descripted in a json file, accordingly to
        the object and the definition of the parametrization by inserting the curve data points 
        in a new json file which is the output of the function.
        '''
        modified_Dict = data_dict
        if modify_Thickness:
            modified_Dict["Blade0"]["ThicknessDefinition"]["New ThicknessCurve"][0]["HorizDim"] = "PercentMeridional"
            modified_Dict["Blade0"]["ThicknessDefinition"]["New ThicknessCurve"][0]["New Segment"][0]["Data"]["data"] = thickness_curve
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
                data_indent = '    ' * (indent_level)  # One additional level for data points inside "Data"

                if isinstance(data, dict):
                    for key, value in data.items():
                        if isinstance(value, dict):
                            if key in ["Case", "PlusData", "Model", "Equations", "Defaults", "Meridional", "HubCurve", "Data"]:
                                file.write(f"{indent}Begin {key}\n")
                                write_bji(value, indent_level + 1)
                                file.write(f"{indent}End {key}\n\n")
                            else:
                                if "Blade" in key:
                                    name_key = key[:-1]
                                else:
                                    name_key = key
                                file.write(f"{indent}New {name_key}\n")
                                write_bji(value, indent_level + 1)
                                file.write(f"{indent}End {name_key}\n\n")

                        elif isinstance(value, list):
                            for item in value:
                                if isinstance(item, dict):
                                    if key.startswith("New"):
                                        file.write(f"{indent}{key}\n")
                                        write_bji(item, indent_level + 1)
                                        file.write(f"{indent}End {key.split()[1]}\n")
                                    else:
                                        file.write(f"{indent}Begin {key}\n")
                                        write_bji(item, indent_level + 1)
                                        file.write(f"{indent}End {key}\n")
                                else:
                                    # Adjust indentation specifically for Data section points
                                    if key == 'data':
                                        item = tuple(item)
                                        file.write(f"{data_indent}{item}\n")  # Use data_indent (one additional level)
                                    else:
                                        file.write(f"{indent}{item}\n")

                        elif value is None:
                            file.write(f"{indent}{key}\n")

                        else:
                            file.write(f"{indent}{key}={value}\n")

                elif isinstance(data, list):
                    for item in data:
                        file.write(f"{indent}{item}\n")

            write_bji(json_data)

    def convert_bgi_to_bgd(self, output_bgiPath, output_bgdPath, ANSYSfolderPath = "c:\\Program Files\\ANSYS Inc"):
        '''
        Runs terminal's commands to execute BladeBatch from BladeGen in order to run
        the .bgi file and obtain a .bgd
        '''

        # Setting the path for the ANSYS folder
        path_command = f'''set path=%path%;"{ANSYSfolderPath}\\v242\\aisol\\BladeModeler\\BladeGen"'''
        
        # Prepare the command to run BladeBatch
        blade_batch_command = f'BladeBatch {output_bgiPath} {output_bgdPath}'
        
        # Combine commands into a single command string for the terminal
        full_command = f'cmd /c "{path_command} && {blade_batch_command}"'
        
        # Run the command in the terminal
        result = subprocess.run(full_command, shell=True, capture_output=True, text=True)

        # Print the output and errors (if any)
        if self.parameters.print_conversion_output:
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)

        # Check if the command was successful
        if result.returncode == 0:
            print("Conversion bgi->bgd completed successfully.")
            return True
        else:
            print("An error occurred during the conversion bgi->bgd.")
            print(f"Error: result.retuncode = {result.returncode}")
            return None

    def create_modified_geometry(self):
        DataList = self.readfile(filePath =  self.defaultfilePath)
        DataDict = self.convert_list_to_dict(DataList)
        ModDataDict = self.modify_dict_numOfBlades(self.parameters.numOfBlades, self.parameters.modify_numOfBlades, DataDict)
        ModDataDict = self.modify_dict_blade(self.parameters.Beta_definition, self.parameters.Beta_M_bezier_curve_points, DataDict, self.parameters.fibers)
        ModDataDict = self.modify_dict_HubShroud(self.parameters.HubShroud_definition, ModDataDict)
        ModDataDict = self.modify_dict_thickness(self.parameters.thickness_curve, self.parameters.modify_Thickness, ModDataDict)
        self.save_json(self.output_jsonPath, ModDataDict)
        self.convert_json_to_bgi(self.output_jsonPath, self.output_bgiPath)
        
        self.convert_bgi_to_bgd(self.output_bgiPath, self.output_bgdPath, ANSYSfolderPath = self.std_ANSYS_Folder)
        return
    
    def create_unmodified_json_geometry(self):
        DataList = self.readfile(filePath = self.defaultfilePath)
        if self.parameters.print_conversion_output:
            print(DataList)
        DataDict = self.convert_list_to_dict(DataList)
        self.save_json(self.output_jsonPath, DataDict)
        return
    
    def create_unmodified_bgi_geometry(self):
        DataList = self.readfile(filePath =  self.defaultfilePath)
        UnModDataDict = self.convert_list_to_dict(DataList)
        self.save_json(self.output_jsonPath, UnModDataDict)
        self.convert_json_to_bgi(self.output_jsonPath, self.output_unmodified_bgiPath)
        self.convert_bgi_to_bgd(self.output_bgiPath, self.output_unmodified_bgdPath, ANSYSfolderPath = self.std_ANSYS_Folder)
        return