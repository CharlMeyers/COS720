#!/usr/bin/python
import os
import shutil
import sys

def removeBody(infile):
	emailHeaderLines = []
	for line in infile:
		if line != "\n":
			emailHeaderLines.append(line)
		else:
			return emailHeaderLines


def search_directory(directory, outputDirectory):
	for root, directories, files in os.walk(directory):
		outputPath = os.path.join(outputDirectory, root[len(directory)+1:])		
		if not os.path.isdir(outputPath):
			os.mkdir(outputPath)		
		print("Anonymising ", root, end="\r")
		for file in os.listdir(root):
			filePath = os.path.join(root,file)
			outputFilePath = os.path.join(outputPath,file)
			if os.path.isfile(filePath):
				with open(filePath, "r") as fileToCopy:					
					with open(outputFilePath, "w+") as fileToWrite:
						removedBodyFromEmail = removeBody(fileToCopy)
						fileToWrite.writelines(removedBodyFromEmail)





search_directory('F:/UserData/My Documents/Coding Stuff/maildir/allen-p', 'F:/UserData/My Documents/Coding Stuff/anonymisedMail')


