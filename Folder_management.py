import os
import shutil

output_jsonfolder_settings = 'modifiedJSON'
output_bgifolder_settings = 'modifiedBGI'
output_unmodified_bgifolder_settings = 'unmodifiedBGI'
output_bgdfolder_settings = 'modifiedBGD'
output_unmodified_bgdfolder_settings = 'unmodifiedBGD'

def Create_Folder(Path):
    """Creates a new folder at the specified path.

    Args:
        Path: The path where the new folder should be created.

    Returns:
        True if the folder was created successfully, False otherwise.
    """
    try:
        os.makedirs(Path, exist_ok=True)  # exist_ok=True prevents error if folder already exists
        return True
    except OSError as e:
        print(f"Error creating folder: {e}")
        return False

def Copy_File(initial_position, final_position):
    """Copies a file from the initial position to the final position.

    Args:
        initial_position: The path of the file to be copied.
        final_position: The path where the file should be copied.

    Returns:
        True if the file was copied successfully, False otherwise.
    """
    try:
        shutil.copy2(initial_position, final_position) # copy2 preserves metadata
        return True
    except FileNotFoundError:
        print("File not found. Please check the file path.")
        return False
    except shutil.Error as e:
        print(f"Error copying file: {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False

def Create_Project_Folder(Project_Name = "Database_Test_1",
                          Project_Folder = "D:\Davide",
                          default_geometry_path = 'defaultBGI\\LUS_General_OnlySpan0_Copy.bgi',
                          output_jsonfolder = output_jsonfolder_settings,
                          output_bgifolder = output_bgifolder_settings,
                          output_unmodified_bgifolder = output_unmodified_bgifolder_settings,
                          output_bgdfolder = output_bgdfolder_settings,
                          output_unmodified_bgdfolder = output_unmodified_bgdfolder_settings):
    
    Projec_Folder_path = f"{Project_Folder}\\{Project_Name}"
    Create_Folder(Projec_Folder_path)
    Create_Folder(f"{Projec_Folder_path}\\defaultBGI")
    Copy_File(default_geometry_path,f"{Projec_Folder_path}\\defaultBGI")
    Create_Folder(f"{Projec_Folder_path}\\{output_jsonfolder}")
    Create_Folder(f"{Projec_Folder_path}\\{output_bgifolder}")
    Create_Folder(f"{Projec_Folder_path}\\{output_unmodified_bgifolder}")
    Create_Folder(f"{Projec_Folder_path}\\{output_bgdfolder}")
    Create_Folder(f"{Projec_Folder_path}\\{output_unmodified_bgdfolder}")

    return Projec_Folder_path

def copy_bgd_for_simulation(starting_path, final_path):
    """Lists all files in starting_path and copies .bgd files to final_path using Copy_File."""

    if not os.path.exists(starting_path):
        print(f"Error: Starting path '{starting_path}' does not exist.")
        return

    if not os.path.exists(final_path):
        os.makedirs(final_path)

    for filename in os.listdir(starting_path):
        if filename.endswith(".bgd"):
            source_path = os.path.join(starting_path, filename)
            destination_path = os.path.join(final_path, filename)
            if Copy_File(source_path, destination_path):
                print(f"Copied '{filename}' to '{final_path}'")
