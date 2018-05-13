import os;
import re;
import errno;
import socket;
import random;
import string;
import tldextract;
from threading import Thread, Lock;
import threading;
import time;

rootEmailDir = "../../maildir";
foldersToExplore = [{"user": "", "path": rootEmailDir}];
filesToProcess = [];
domainIpArray = {};

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
	try:
		emailPath = emailMap["path"];
		email = open(emailPath,"r");
		emailLines = email.readlines();
		email.close();
		csvLine = {"user": emailMap["user"].replace("\"", "").replace(",", "+")};
		csvLine["email path"] = emailPath.replace("\"", "").replace(",", "+")[len(rootEmailDir) + 1:];

		for line in emailLines:
			line = line.rstrip('\n');

			if line == "":
				break;

			headerInLine, separatorInLine, valueInLine = line.partition(":");

			if separatorInLine == "" or headerPattern.match(headerInLine):
				continue;
			else:
				if headerInLine == "From":
					beforeAt, at, fromDomain = valueInLine.partition("@");
					domainExtract = tldextract.extract(fromDomain);
					fromDomain = domainExtract.domain + "." + domainExtract.suffix;
					csvLine["From-Domain"] = fromDomain;
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

					break;

		if i % 1000 == 0:
			print("\rReading emails progress: " + str(round(i / len(filesToProcess) * 100, 2)) + "%", end='', flush=True);
			csvFile = open("output/host_ip_map.csv", "w");
			csvFile.write("host,ip\n");

			for i, domainIpKey in enumerate(domainIpArray.keys()):
				csvFile.write(domainIpKey + "," + domainIpArray[domainIpKey] + "\n");

			csvFile.close();

		# if i / len(filesToProcess) * 100 > 0.1:
		# 	break;
	except Exception:
		print("\nError at file " + emailPath + "\n");
		raise;

print("\rReading emails progress: 100% " + threading.currentThread().getName());
print("\nSaving host-ip file...", end='', flush=True);

csvFile = open("output/host_ip_map.csv", "w");
csvFile.write("host,ip\n");

for i, domainIpKey in enumerate(domainIpArray.keys()):
	csvFile.write(domainIpKey + "," + domainIpArray[domainIpKey] + "\n");

csvFile.close();