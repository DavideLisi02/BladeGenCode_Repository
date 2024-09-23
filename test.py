import os
import json
import re

def change_to_script_directory():
    # Get the directory of the currently running script
    script_directory = os.path.dirname(os.path.abspath(__file__))
    
    # Change the current working directory to the script's directory
    os.chdir(script_directory)
    
    print(f"Current working directory changed to: {script_directory}")

change_to_script_directory()

def read_bgi_file(file_path):
    """
    Reads the content of a .bgi file and returns it as a list of lines.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return lines

def parse_bgi_to_dict(lines):
    """
    Converts the list of lines from the .bgi file into a structured dictionary.
    This version supports infinitely nested subsections using a stack,
    including handling multiple segments under a subsection.
    """
    data_dict = {}
    stack = []  # Stack to handle nested sections/subsections
    current_data = []  # For storing (x, y) or other data points
    current_subsection = None  # To track the current subsection

    for line in lines:
        line = line.strip()
        print(f"Analyzed line = #{line}#")

        if line.startswith("Begin"):
            section_name = line.split()[1]
            new_section = {}
            if stack:
                # Add the new section to the current section at the top of the stack
                parent_section = stack[-1]
                parent_section[section_name] = new_section
            else:
                # This is a top-level section
                data_dict[section_name] = new_section
            stack.append(new_section)  # Push the new section onto the stack
            current_subsection = None  # Reset current_subsection on new section

        elif line.startswith("End"):
            if current_subsection and stack:
                # Store the current data into the subsection's data
                parent_section = stack[-1]
                if "data" not in parent_section[current_subsection]:
                    parent_section[current_subsection]["data"] = []  # Initialize data list
                parent_section[current_subsection]["data"].extend(current_data)  # Append data
                current_data = []  # Reset current data for the next segment
            # Pop the section off the stack when it ends
            stack.pop()
            if stack:  # Reset current_subsection when not at the top level
                current_subsection = None

        elif "=" in line:
            # Handle key=value lines
            key, value = line.split("=", 1)
            if stack:
                current_section = stack[-1]
                if current_subsection:
                    # Initialize the subsection if it doesn't exist
                    if current_subsection not in current_section:
                        current_section[current_subsection] = {}
                    current_section[current_subsection][key.strip()] = value.strip()
                else:
                    # Add the key-value pair to the current section
                    current_section[key.strip()] = value.strip()
            else:
                print(f"Warning: Key-value pair found outside of any section: {line}")

        elif "(" in line and ")" in line:
            # Handle data points in the form (x, y)
            current_data.append(re.findall(r"\((.*?)\)", line)[0])

        elif "New" in line:
            # Handle new subsections (e.g., New Segment, New AngleCurve, etc.)
            subsection_name = line
            new_subsection = {}
            if stack:
                current_section = stack[-1]
                if subsection_name not in current_section:
                    current_section[subsection_name] = []  # Initialize list for multiple segments
                current_section[subsection_name].append(new_subsection)  # Add new subsection
                current_subsection = subsection_name  # Track the current subsection
            stack.append(new_subsection)  # Push the new subsection onto the stack

        elif line == '':
            # Ignore empty lines
            continue

        else:
            # Handle any other plain lines
            if stack:
                current_section = stack[-1]
                current_section[line] = None  # Add line as key with None value
            else:
                print(f"Warning: Unrecognized line found outside of any section: {line}")

    return data_dict

def save_dict_as_json(data_dict, output_file):
    """
    Saves the dictionary into a JSON file.
    """
    with open(output_file, 'w') as json_file:
        json.dump(data_dict, json_file, indent=4)

def convert_json_to_bji(json_file, bji_file):
    """
    Reads a JSON file and converts it into a .bji format
    that preserves specific formatting.
    """
    with open(json_file, 'r') as file:
        json_data = json.load(file)

    with open(bji_file, 'w') as file:
        def write_bji(data, indent_level=0):
            indent = '    ' * indent_level  # Use 4 spaces for indentation
            for key, value in data.items():
                if isinstance(value, dict):
                    # Begin a new section
                    file.write(f"{indent}Begin {key}\n")
                    write_bji(value, indent_level + 1)
                    file.write(f"{indent}End {key}\n\n")  # Adding a blank line after the section

                elif isinstance(value, list):
                    # Handle lists of items (like segments)
                    for index, item in enumerate(value):
                        file.write(f"{indent}New {key}\n")
                        write_bji(item, indent_level + 1)
                        file.write(f"{indent}End {key}\n\n")  # Blank line after each item

                elif key == "data":
                    # Handle the data points under a subsection
                    for point in value:
                        file.write(f"{indent}({', '.join(map(str, point))})\n")

                else:
                    # Write key=value pairs
                    file.write(f"{indent}{key} = {value}\n")

        write_bji(json_data)

if __name__ == "__main__":
    # Step 1: Read the .bgi file
    bgi_file_path = 'defaultBGI\\default00.bgi'  # Change this to your actual file path
    lines = read_bgi_file(bgi_file_path)
    
    # Step 2: Convert the list to dictionary
    data_dict = parse_bgi_to_dict(lines)
    
    # Step 3: Save the dictionary as JSON
    json_file_path = 'output_data.json'
    save_dict_as_json(data_dict, json_file_path)
    
    # Step 4: Convert JSON to DJI (optional, depends on your DJI format requirements)
    dji_file_path = 'output_data.dji'
    convert_json_to_bji(json_file_path, dji_file_path)
    
    print("Conversion completed successfully!")
