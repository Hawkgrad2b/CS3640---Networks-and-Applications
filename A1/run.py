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

# This block will try to run through the array of string commands
if len(sys.argv) == 2:
    
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

    for command in commands:
        f.write(f"\nCommand: {' '.join(command)}\n")
        
        # Try to run the current command as a subprocess
        try:
            result = subprocess.run(command, capture_output=True, text=True)
            f.write(result.stdout)

        # If the current command fails to run, write the error message corresponding to current command name
        except subprocess.CalledProcessError as e:
            error_message = f"[error] {command[0]} failed with the return code as: {result.stdout} {str(e)}\n"
            print(error_message)
            f.write(error_message)

        # Specified formatting after each command is attempted to run
        f.write("\n*****\n")

# If there is not a suficient amount of arguments passed into the program, print error message
elif len(sys.argv) == 1:
    f.write("[Error] No IP or Website was provided as an input to the command-line\n")
    print("[Error] Please enter an IP or Website address as an input into command-line\n")

# If there are too many arguments passed into the program, print error message
elif len(sys.argv) > 2:
    f.write("[Error] Too many parameters were enter as an input into the command-line\n")
    print("[Error] Too many parameters were enter as an input into the command-line\n")

# Close the output.txt file and print to the terminal
f.close()
print("commands executed and output saved to output.txt")
