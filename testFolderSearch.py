#!/usr/bin/python
import os
import shutil


def search_directory(directory, outputDirectory):	
	for root, directories, files in os.walk(directory):		
		outputPath = os.path.join(outputDirectory, root[len(directory)+1:])		
		if not os.path.isdir(outputPath):
			os.mkdir(outputPath)
		print("Anonymising ", root)		
		for file in os.listdir(root):
			filePath = os.path.join(root,file)
			outputFilePath = os.path.join(outputPath,file)
			if os.path.isfile(filePath):
				with open(filePath, "r") as fileToCopy:
					fileToCopyContent = fileToCopy.read()
					# with open(outputFilePath, "w+") as file_to_write:
					# 	file_to_write.write(fileToCopyContent)
					print(fileToCopy.find("\n\r"))
		




search_directory('F:/UserData/My Documents/Coding Stuff/maildir/allen-p', 'F:/UserData/My Documents/Coding Stuff/anonymisedMail')


