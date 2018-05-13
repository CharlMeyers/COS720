import os;
import re;
import date_calculations;
import zipfile;
import socket;
import tldextract;

rootEmailDir = "../../fabricated_emails";
foldersToExplore = [{"user": "", "path": rootEmailDir}];
filesToProcess = [];
domainIpArray = {};
addedFromId = False;
addedMessageIdServer = False;

csvFile = open("output/host_ip_map.csv", "r");
print("Reading host-ip map...", end='', flush=True);
csvLines = csvFile.readlines();
print(" Done\nIPs found: " + str(len(csvLines)));
csvFile.close();

for r, csvRecord in enumerate(csvLines):
	if r == 0:
		continue;

	domainIpMap = csvRecord.rstrip('\n').split(',');

	domainIpArray[domainIpMap[0]] = domainIpMap[1];

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
	csvLine["email path"] = emailPath.replace("\"", "").replace(",", "+")[len(rootEmailDir) + 1:];

	for line in emailLines:
		line = line.rstrip('\n');

		if line == "":
			break;

		headerInLine, separatorInLine, valueInLine = line.partition(":");

		if separatorInLine == "" or headerPattern.match(headerInLine):
			previousHeader = list(csvLine.keys())[-1];

			if previousHeader == "email path":
				print("ERROR in file: " + csvLine["email path"]);
				continue;

			valueInLine = headerInLine + separatorInLine + valueInLine;
			valueInLine = valueInLine.replace("\"", "").replace(",", "+");
			csvLine[previousHeader] = csvLine[previousHeader] + " " + valueInLine.strip();
		else:
			if headerInLine == "Date":
				csvLine[headerInLine] = date_calculations.convertTimestamp(valueInLine.replace("\"", "").replace(",", "+").strip());
			elif headerInLine == "Received1":
				valueInLine = valueInLine[4:];
				valueInLine = valueInLine[:valueInLine.find(" ")];
				csvLine[headerInLine] = valueInLine.replace("\"", "").replace(",", "+").strip();
			elif headerInLine == "Received2":
				valueInLine = valueInLine[valueInLine.find("[") + 1:valueInLine.find("]")];
				csvLine[headerInLine] = valueInLine.replace("\"", "").replace(",", "+").strip();
			elif headerInLine == "Message-ID":
				beforeAt, at, afterAt = valueInLine.partition("@");

				if at == "":
					afterAt = beforeAt + ">";

				csvLine["Message-ID-Server"] = afterAt[:-1].replace("\"", "").replace(",", "+").strip();
				csvLine[headerInLine] = valueInLine.replace("\"", "").replace(",", "+").strip();

				if not addedMessageIdServer:
					headers.append("Message-ID-Server");
					addedMessageIdServer = True;
			elif headerInLine == "From":
				beforeAt, at, fromDomain = valueInLine.partition("@");
				domainExtract = tldextract.extract(fromDomain);
				fromDomain = domainExtract.domain + "." + domainExtract.suffix;
				csvLine["From-IP"] = "";

				try:
					csvLine["From-IP"] = domainIpArray[fromDomain];
				except KeyError:
					print("\rCouldn't find ip for " + fromDomain + " in local cache.");
					try:
						csvLine["From-IP"] = socket.gethostbyname(fromDomain);
					except socket.gaierror as e:
						csvLine["From-IP"] = fromDomain;

					domainIpArray[fromDomain] = csvLine["From-IP"];

				csvLine[headerInLine] = valueInLine.replace("\"", "").replace(",", "+").strip();

				if not addedFromId:
					headers.append("From-IP");
					addedFromId = True;
			else:
				csvLine[headerInLine] = valueInLine.replace("\"", "").replace(",", "+").strip();

			foundHeader = False;

			for header in headers:
				if headerInLine == header:
					foundHeader = True;
					break;

			if not foundHeader:
				headers.append(headerInLine);
				print("\rFound new header: " + headerInLine + " in file: " + csvLine["email path"]);
				print("\rReading emails progress: " + str(round(i / len(filesToProcess) * 100, 2)) + "%", end='', flush=True);

	csvLine["File-size"] = os.path.getsize(emailPath);
	csvFileContent.append(csvLine);
	email.close();

	if i % 1000 == 0:
		print("\rReading emails progress: " + str(round(i / len(filesToProcess) * 100, 2)) + "%", end='', flush=True);

	# if i / len(filesToProcess) * 100 > 0.1:
	# 	break;

print("\rReading emails progress: " + str(round(i / len(filesToProcess) * 100, 2)) + "%", end='', flush=True);
print("\nCompiling CSV file...", end='', flush=True);
csvFile = open("output/cleaned_data.csv", "w");
csvFileSmall = open("output/cleaned_data_small.csv", "w");
line = "";

for header in headers:
 	line += header + ",";

csvFile.write(line[:-1] + "\n");
csvFileSmall.write(line[:-1] + "\n");

for i, contentMap in enumerate(csvFileContent):
	line = "";
	skipRow = False;

	for header in headers:
		try:
			if header == "To" and contentMap[header] == "":
				skipRow = True;

			line += contentMap[header] + ",";
		except KeyError:
			line += ",";

	if skipRow == False:
		csvFile.write(line[:-1] + "\n");

		if i < 100:
			csvFileSmall.write(line[:-1] + "\n");

csvFile.close();
csvFileSmall.close();
csvFile = open("output/host_ip_map_tmp.csv", "w");
csvFile.write("host,ip\n");

for i, domainIpMap in enumerate(domainIpArray):
	csvFile.write(domainIpMap[0] + "," + domainIpMap[1] + "\n");

csvFile.close();
print(" Done\nWriting host-ip mapping file...", end='', flush=True);
csvFile = open("output/host_ip_map.csv", "w");
csvFile.write("host,ip\n");

for i, domainIpKey in enumerate(domainIpArray.keys()):
	csvFile.write(domainIpKey + "," + domainIpArray[domainIpKey] + "\n");

csvFile.close();
print(" Done.\nZipping large file...", end='', flush=True);
zf = zipfile.ZipFile("output/cleaned_data.zip", mode="w");

try:
	zf.write("output/cleaned_data.csv", compress_type=zipfile.ZIP_DEFLATED);
finally:
	zf.close();

print(" Done");
print("Zipping small file...", end='', flush=True);
zf = zipfile.ZipFile("output/cleaned_data_small.zip", mode="w");

try:
	zf.write("output/cleaned_data_small.csv", compress_type=zipfile.ZIP_DEFLATED);
finally:
	zf.close();

print(" Done");
print("Zipping host-ip map...", end='', flush=True);
zf = zipfile.ZipFile("output/host_ip_map.zip", mode="w");

try:
	zf.write("output/host_ip_map.csv", compress_type=zipfile.ZIP_DEFLATED);
finally:
	zf.close();

print(" Done");