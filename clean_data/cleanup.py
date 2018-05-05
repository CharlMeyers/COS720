import os;
import re;

foldersToExplore = [{"user": "", "path": "../maildir"}];
filesToProcess = [];

while len(foldersToExplore) != 0:
	currentMap = foldersToExplore.pop(0);
	currentFolder = currentMap["path"];
	print("Exploring folder: " + currentFolder);
	insertIndex = 0;

	for folder in os.listdir(currentFolder):
		if os.path.isdir(currentFolder + "/" + folder):
			user = currentMap["user"];

			if user == "":
				user = folder;

			foldersToExplore.insert(insertIndex, {"user": user, "path": currentFolder + "/" + folder});
			insertIndex += 1;
		else:
			filesToProcess.append({"user": user, "path": currentFolder + "/" + folder});

print("Found " + str(len(filesToProcess)) + " emails.");
headers = ["user", "email path"];
csvFileContent = [];
headerPattern = re.compile('^\s.*$');

for i, emailMap in enumerate(filesToProcess):
	emailPath = emailMap["path"];
	email = open(emailPath,"r");
	emailLines = email.readlines();
	csvLine = {"user": emailMap["user"].replace("\"", "").replace(",", "+")};
	csvLine["email path"] = emailPath.replace("\"", "").replace(",", "+");

	for line in emailLines:
		line = line.rstrip('\n');

		if line == "":
			break;

		headerInLine, separatorInLine, valueInLine = line.partition(":");

		if separatorInLine == "" or headerPattern.match(headerInLine):
			previousHeader = list(csvLine.keys())[-1];

			if previousHeader == "email path":
				print("ERROR in file: " + emailPath);
				continue;

			valueInLine = headerInLine + separatorInLine + valueInLine;
			valueInLine.replace("\"", "").replace(",", "+");
			oldValue = csvLine[previousHeader];
			csvLine[previousHeader] = oldValue + " " + valueInLine.strip();
		else:
			csvLine[headerInLine] = valueInLine.replace("\"", "").replace(",", "+").strip();
			foundHeader = False;

			for header in headers:
				if headerInLine == header:
					foundHeader = True;
					break;

			if not foundHeader:
				headers.append(headerInLine);
				print("\rFound new header: " + headerInLine + " in file: " + emailPath);

	csvFileContent.append(csvLine);
	email.close();
	print("\rReading emails progress: " + str(round(i / len(filesToProcess) * 100, 2)) + "%", end='', flush=True);

print("\nCompiling CSV file...");
csvFile = open("output/cleaned_data.csv", "w");
line = "";

for header in headers:
 	line += header + ",";

csvFile.write(line[:-1] + "\n");

for contentMap in csvFileContent:
	line = "";

	for header in headers:
		try:
			line += contentMap[header] + ",";
		except KeyError:
			line += ",";

	csvFile.write(line[:-1] + "\n");

csvFile.close();
print("Done");