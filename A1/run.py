#run.py python script file for assingment 1
# Used the websites https://docs.python.org/3/library/subprocess.html and
# https://www.geeksforgeeks.org/python-subprocess-module/ 
# for better understanding on subprocess module

import subprocess
import sys
import os

HAWKID = "wplucas"
NAME = "William Lucas"

output_file_path = "output.txt"

# Set the file path to output.txt to the variable f to write into
f = open('output.txt', 'w')

# Starts the output.txt file with hawkid and name
f.write(f"{HAWKID}\n{NAME}\n")

# Checks to make sure there is a suficient amount of arguments passed into the program
if len(sys.argv) < 2:
    error_message = "[Error] No input provided. Please provide a target for ping and traceroute. \n"
    print(error_message)
    f.write(error_message)
    sys.exit(1)

# Takes the target given from the user in the command line to, will be used for ping and traceroute
target = sys.argv[1]

# The commands that will be executed when run.py is run with a given target
commands = [
        ["date"],
        ["whoami"],
        ["ifconfig"],
        ["ping", target, "-c","10"],
        ["traceroute", target, "-m","10"],
    ]

# This block will try to run through the array of string commands
try:
    for command in commands:
        f.write(f"\nCommand: {' '.join(command)}\n")
        
        # Try to run the current command as a subprocess
        try:
            result = subprocess.run(command, capture_output=True, text=True)
            f.write(result.stdout)

        # If the current command fails to run, write the error message corresponding to current command name
        except subprocess.CalledProcessError as e:
            error_message = f"[error] {command[0]} failed: {str(e)}\n"
            print(error_message)
            f.write(error_message)

        # Specified formatting after each command is attempted to run
        f.write("\n*****\n")

# Close the output.txt file and print to the terminal
finally:
    print("commands executed and output saved to output.txt")
