import subprocess

def run_command(full_command):
    """Runs a command in the terminal.

    Args:
        full_command: The command to run.
    """
    try:
        process = subprocess.Popen(full_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
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