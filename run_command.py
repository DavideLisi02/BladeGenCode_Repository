import subprocess

def run_command(full_command, show_cmd=False):
    """Runs a command in the terminal, optionally showing the command prompt.

    Args:
        full_command: The command to run.
        show_cmd: Whether to show the command prompt window (True/False). Defaults to False.

    Returns:
        The return code of the command.
    """
    try:
        creationflags = 0  # Default: Don't show the window
        if show_cmd:
            creationflags = subprocess.CREATE_NEW_CONSOLE  # Show the window

        process = subprocess.Popen(full_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, creationflags=creationflags)
        stdout, stderr = process.communicate()
        if stdout:
            print(f"Command output:\n{stdout}")
        if stderr:
            print(f"Command error:\n{stderr}")
        return process.returncode
    except FileNotFoundError:
        print("Command not found. Please check the command and your system's PATH environment variable.")
        return 1
    except Exception as e:
        print(f"An error occurred: {e}")
        return 1