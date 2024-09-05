#run.py python script file for assingment 1

import subprocess
import sys
import os

HAWKID = "wplucas"
NAME = "William Lucas"

output_file_path = "output.txt"

#Starts the output.txt file with hawkid and name
with open(output_file_path, "w") as f:
    f.write(f"{HAWKID}\n{NAME}\n")

def execute_command(command):
    try:
        result = subprocess.run(command, shell=False, capture_output=True, text=True)

        with open(output_file_path, "a") as f:
            f.write(f"\nCommand: {' '.join(command)}\n")
            
            if result.returncode == 0:
                f.write(result.stdout)
            else:
                raise Exception(result.stderr)
            f.write("\n*****\n")
    except Exception as e:
        error_message = f"[error] {command[0]} failed: {str(e)}\n"

        print(error_message)
        with open(output_file_path, "a") as f:
            f.write(error_message)

if len(sys.argv) < 2:
    error_message = "[Error] No input provided. Please provide a target for ping and traceroute. \n"
    print(error_message)
    with open(output_file_path, "a") as f:
        f.write(error_message)
    sys.exit(1)

input_target = sys.argv[1]

commands = [
        ["date"],
        ["whoami"],
        ["ifconfig"],
        ["ping", input_target, "-c","10"],
        ["traceroute", input_target, "-m","10"]
]

for command in commands:
    execute_command(command)

print("commands executed and output saved to output.txt")
