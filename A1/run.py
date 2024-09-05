import subprocess
import sys

# Handle incorrect # of arguments
if len(sys.argv) != 2:
	print("[Error] Incorrect number of arguments (only one hostname or"+
		" IP address allowed!)")
	sys.exit(1)

hawkid = "kprasai"
name = "Krisham Prasai"
commandSeparator = "\n*****\n"

# Title
with open("output.txt", "w") as file:
	file.write("hawkid: " + hawkid + "\nName: " + name)
	file.write(commandSeparator)

# Run, Write, and Print Commands
commands = [
	'date',
	'whoami',
	'ifconfig',
	'ping',
	'traceroute'
]

input = sys.argv[1]
for command in commands:
	try:
		if (command == 'ping'):
			result = subprocess.check_output(['ping', input, '-c', '10'],
							stderr=subprocess.STDOUT)
		elif (command == 'traceroute'):
			result = subprocess.check_output(['traceroute', input, '-m', '10'],
							stderr=subprocess.STDOUT)
		else:
			result = subprocess.check_output(command, stderr=subprocess.STDOUT)

		with open("output.txt", "a") as file:
			if (command == 'ping'):
				file.write(f"Command: ping {input} -c 10\n")
			elif (command == 'traceroute'):
				file.write(f"Command: traceroute {input} -m 10\n")
			else:
				file.write(f"Command: {command}\n")
			file.write(result.decode("utf-8"))
			file.write(commandSeparator)
	except subprocess.CalledProcessError as error:
		if (command == 'ping'):
			errorMessage = f"[Error] {command} {input} -c 10 failed: {error.output.decode('utf-8')}"
		elif (command =='traceroute'):
			errorMessage = f"[Error] {command} {input} -m 10 failed: {error.output.decode('utf-8')}"
		else:
			errorMessage = f"[Error] {command} failed: {error.output.decode('utf-8')}"

		print(errorMessage)
		# Write error to output.txt
		with open("output.txt", "a") as file:
			file.write(errorMessage)
			file.write(commandSeparator)
