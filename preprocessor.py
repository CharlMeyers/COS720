import os
import shutil
import sys
import random
import anonymiser

def log(string, parameters):
	if os.name == "nt":
		print(os.system("cls"))
	else:
		sys.stdout.write("\003[K")

	print(string, parameters, end="\r")


def search_directory(directory, outputDirectory, shouldRemoveBody):
	everyCountChar = random.randint(3, 6)
	amountToMove = random.randint(3,5)	
	for root, directories, files in os.walk(directory):
		outputPath = os.path.join(outputDirectory, root[len(directory)+1:])		
		if not os.path.isdir(outputPath):
			os.mkdir(outputPath)
		
		log("Anonymising ", root)
		for file in os.listdir(root):
			filePath = os.path.join(root,file)
			outputFilePath = os.path.join(outputPath,file)
			if os.path.isfile(filePath):
				with open(filePath, "r") as fileToCopy:					
					with open(outputFilePath, "w+") as fileToWrite:						
						removedBodyFromEmail = anonymiser.removeBody(fileToCopy, shouldRemoveBody)						
						modifiedNamesAndSurnames = anonymiser.anonymiseSenderAndReceiver(removedBodyFromEmail, everyCountChar, amountToMove)
						fileToWrite.writelines(modifiedNamesAndSurnames)


search_directory('F:/UserData/My Documents/Coding Stuff/maildir/allen-p', 'F:/UserData/My Documents/Coding Stuff/anonymisedMail', True)
