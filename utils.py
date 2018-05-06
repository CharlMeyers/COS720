import os
import sys

def printList(string, list):
	output = string

	for item in list:
		output += "{"
		output += item
		output += "}, "

	output += "\n"

	print(output)

def log(string, parameters):
	if os.name == "nt":
		print(os.system("cls"))
	else:
		sys.stdout.write("\003[K")

	print(string, parameters, end="\r")