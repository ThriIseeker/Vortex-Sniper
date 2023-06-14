import os
import subprocess

# Path to the requirements.txt file
requirements_file = "requirements.txt"

def install_modules():
    # Install modules using pip
    subprocess.check_call(["pip", "install", "-r", requirements_file])

def delete_self():
    # Get the absolute path of the current script
    script_path = os.path.abspath(__file__)

    # Delete the script file
    os.remove(script_path)

if __name__ == "__main__":
    install_modules()
    delete_self()
