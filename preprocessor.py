#!/usr/bin/python
import os
import shutil
import sys
import random

def removeBody(infile, shouldRemoveBody):
	emailHeaderLines = []
	for line in infile:
		if shouldRemoveBody and line != "\n":
			emailHeaderLines.append(line)
		elif not shouldRemoveBody:
			emailHeaderLines.append(line)
		else:
			return emailHeaderLines

	return emailHeaderLines


def shiftChar(string, position, amount):
	result = string
	stringLength = len(string)	
	if(position < stringLength):		
		charToMove = string[position]
		positionToMoveTo = position + 1 + amount
		if(positionToMoveTo > stringLength):
			positionToMoveTo = stringLength - 1
		result = string[:position] + string[position+1:positionToMoveTo] + charToMove + string[positionToMoveTo:]	
	return result


def shiftString(string, everyCountChar, amountToMove):
	amountOfCharsInString = int(len(string) / everyCountChar)
	shiftedString = string.split("\n")[0]
	for i in range(amountOfCharsInString):		
		shiftCharResult = shiftChar(shiftedString, everyCountChar*(i), amountToMove)		
		shiftedString = shiftCharResult[amountToMove:] + shiftCharResult[:amountToMove] #rotate string		

	return shiftedString


def anonymiseSenderAndReceiver(input, everyCountChar, amountToMove):		
	result = [i for i in input if "from:" in i.lower()]		
	fromEmail = result[0].split("From: ")[1].replace("\n", "")
	fromEmailIndexInInput = input.index(result[0])
	result[0] = "From: " + shiftString(fromEmail, everyCountChar, amountToMove) + "\n"

	x_from = result[1].split("X-From: ")[1]
	x_fromIndexInInput = input.index(result[1])
	leftAngularBracketPosition = x_from.find("<") #Find position of <
	rightAngularBracketPosition = x_from.find(">") #Find position of >	
	if leftAngularBracketPosition != -1:
		x_fromName = x_from[:leftAngularBracketPosition-1].lower().replace('\"', '').replace(" ", "").replace("\n", "")
		x_fromEmail = x_from[leftAngularBracketPosition+1:rightAngularBracketPosition]
		x_fromRestOfString = x_from[rightAngularBracketPosition+1:]
		shiftedX_FromName = '\"' + shiftString(x_fromName, everyCountChar, amountToMove) + '\"'
		shiftedX_FromEmail = "<" + shiftString(x_fromEmail, everyCountChar, amountToMove) + ">"
		result[1] = "X-From: " + shiftedX_FromName + " " + shiftedX_FromEmail + x_fromRestOfString + "\n"
	else:
		x_fromName = x_from.lower().replace(" ", "").replace("\n", "")
		result[1] = "X-From: " + shiftString(x_fromName, everyCountChar, amountToMove) + "\n"

	input[fromEmailIndexInInput] = result[0]
	input[x_fromIndexInInput] = result[1]

	return input


def search_directory(directory, outputDirectory, shouldRemoveBody):
	everyCountChar = random.randint(3, 6)
	amountToMove = random.randint(3,5)	
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
						removedBodyFromEmail = removeBody(fileToCopy, shouldRemoveBody)						
						modifiedNamesAndSurnames = anonymiseSenderAndReceiver(removedBodyFromEmail, everyCountChar, amountToMove)
						fileToWrite.writelines(modifiedNamesAndSurnames)


search_directory('F:/UserData/My Documents/Coding Stuff/maildir/allen-p', 'F:/UserData/My Documents/Coding Stuff/anonymisedMail', True)
print("Done")