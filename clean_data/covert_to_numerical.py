import os;
import zipfile;

csvFileContent = [];
contentTypeArray = [];
mimeTypeArray = [];
transferEncodingArray = [];
messageIdArray = [];

csvFile = open("output/cleaned_data.csv", "r");
print("Reading CSV lines...", end='', flush=True);
csvLines = csvFile.readlines();
print(" Done\nEmails found: " + str(len(csvLines)));
csvFile.close();
headers = [];

for r, csvRecord in enumerate(csvLines):
	csvRecord = csvRecord.rstrip('\n').split(',');

	if r == 0:
		headers = csvRecord;
		continue;

	csvMap = {};

	for i, field in enumerate(csvRecord):
		csvMap[headers[i]] = csvRecord[i];

	# Process Content-Type
	found = False;

	for i, contenttype in enumerate(contentTypeArray):
		if contenttype == csvMap["Content-Type"]:
			csvMap["Content-Type"] = i;
			found = True;
			break;

	if found == False:
		contentTypeArray.append(csvMap["Content-Type"]);
		csvMap["Content-Type"] = len(contentTypeArray) - 1;

	# Process Mime-Version
	found = False;

	for i, mimeType in enumerate(mimeTypeArray):
		if mimeType == csvMap["Mime-Version"]:
			csvMap["Mime-Version"] = i;
			found = True;
			break;

	if found == False:
		mimeTypeArray.append(csvMap["Mime-Version"]);
		csvMap["Mime-Version"] = len(mimeTypeArray) - 1;

	# Process Content-Transfer-Encoding
	found = False;

	for i, transferEncoding in enumerate(transferEncodingArray):
		if transferEncoding == csvMap["Content-Transfer-Encoding"]:
			csvMap["Content-Transfer-Encoding"] = i;
			found = True;
			break;

	if found == False:
		transferEncodingArray.append(csvMap["Content-Transfer-Encoding"]);
		csvMap["Content-Transfer-Encoding"] = len(transferEncodingArray) - 1;

	# Process Message-ID-Server
	found = False;

	for i, messageId in enumerate(messageIdArray):
		if messageId == csvMap["Message-ID-Server"]:
			csvMap["Message-ID-Server"] = i;
			found = True;
			break;

	if found == False:
		messageIdArray.append(csvMap["Message-ID-Server"]);
		csvMap["Message-ID-Server"] = len(messageIdArray) - 1;

	# Recipient count
	csvMap["To"] = len(csvMap["To"].split("+"));
	csvMap["Cc"] = len(csvMap["Cc"].split("+"));
	csvMap["Bcc"] = len(csvMap["Bcc"].split("+"));
	csvMap["X-To"] = len(csvMap["X-To"].split("+"));
	csvMap["X-cc"] = len(csvMap["X-cc"].split("+"));
	csvMap["X-bcc"] = len(csvMap["X-bcc"].split("+"));

	csvFileContent.append(csvMap);
		
	if r % 1000 == 0:
		print("\rReading emails progress: " + str(round((r + 1) / len(csvLines) * 100, 2)) + "%", end='', flush=True);

print("\rReading emails progress: " + str(round((r + 1) / len(csvLines) * 100, 2)) + "%", end='', flush=True);






print("\nCompiling CSV file...", end='', flush=True);
csvFile = open("output/cleaned_data_numerical.csv", "w");
line = "";

# headers = ["Message-ID", "Date", "From", "To", "Subject", "X-From", "X-To", "X-Mailer", "Received1", "Received2"];

for header in headers:
 	line += header + ",";

csvFile.write(line[:-1] + "\n");

for i, contentMap in enumerate(csvFileContent):
	line = "";
	skipRow = False;

	for header in headers:
		try:
			if header == "To" and contentMap[header] == "":
				skipRow = True;

			line += str(contentMap[header]) + ",";
		except KeyError:
			line += ",";

	if skipRow == False:
		csvFile.write(line[:-1] + "\n");

csvFile.close();
print(" Done");
print("Compiling lookup file...", end='', flush=True);
csvFile = open("output/numerical_look_up.csv", "w");
line = "";

for header in ["header", "value", "index"]:
 	line += header + ",";

csvFile.write(line[:-1] + "\n");

for i, contentType in enumerate(contentTypeArray):
	csvFile.write("Content-Type," + contentType + "," + str(i) + "\n");

for i, mimeType in enumerate(mimeTypeArray):
	csvFile.write("Mime-Version," + mimeType + "," + str(i) + "\n");

for i, transferEncoding in enumerate(transferEncodingArray):
	csvFile.write("Content-Transfer-Encoding," + transferEncoding + "," + str(i) + "\n");

for i, messageId in enumerate(messageIdArray):
	csvFile.write("Message-ID-Server," + messageId + "," + str(i) + "\n");

csvFile.close();

print(" Done");
print("Zipping file...", end='', flush=True);
zf = zipfile.ZipFile("output/cleaned_data_numerical.zip", mode="w");

try:
	zf.write("output/cleaned_data_numerical.csv", compress_type=zipfile.ZIP_DEFLATED);
finally:
	zf.close();

print(" Done");
print("Zipping lookup file...", end='', flush=True);
zf = zipfile.ZipFile("output/numerical_look_up.zip", mode="w");

try:
	zf.write("output/numerical_look_up.csv", compress_type=zipfile.ZIP_DEFLATED);
finally:
	zf.close();

print(" Done");