import os;
import xlsxwriter;
from dateutil.parser import parse;
import user_email_map;

excelFile = xlsxwriter.Workbook("./output/feature_analysis.xlsx");
graphSheet = excelFile.add_worksheet("Graphs");
statsSheet = excelFile.add_worksheet("DescriptiveStatistics");
emailSentCountsSheet = excelFile.add_worksheet("SentEmailCounts");
emailSentCountsSheet.write_row("A1", ["User", "Number of sent emails"]);
emailReceivedCountsSheet = excelFile.add_worksheet("ReceivedEmailCounts");
emailReceivedCountsSheet.write_row("A1", ["User", "Number of received emails"]);
sentTimeSheet = excelFile.add_worksheet("SentTime");
sentTimeSheet.write_row("A1", ["Hour", "Count"]);
contentTypeSheet = excelFile.add_worksheet("ContentType");
contentTypeSheet.write_row("A1", ["Type", "Count"]);
mimeTypeSheet = excelFile.add_worksheet("MimeType");
mimeTypeSheet.write_row("A1", ["Type", "Count"]);
transferEncodingSheet = excelFile.add_worksheet("TransferEncoding");
transferEncodingSheet.write_row("A1", ["Type", "Count"]);
messageIdSheet = excelFile.add_worksheet("MessageID");
messageIdSheet.write_row("A1", ["Type", "Count"]);
timeArray = [];
timeArray.append(("0:00:00", 0));
timeArray.append(("1:00:00", 0));
timeArray.append(("2:00:00", 0));
timeArray.append(("3:00:00", 0));
timeArray.append(("4:00:00", 0));
timeArray.append(("5:00:00", 0));
timeArray.append(("6:00:00", 0));
timeArray.append(("7:00:00", 0));
timeArray.append(("8:00:00", 0));
timeArray.append(("9:00:00", 0));
timeArray.append(("10:00:00", 0));
timeArray.append(("11:00:00", 0));
timeArray.append(("12:00:00", 0));
timeArray.append(("13:00:00", 0));
timeArray.append(("14:00:00", 0));
timeArray.append(("15:00:00", 0));
timeArray.append(("16:00:00", 0));
timeArray.append(("17:00:00", 0));
timeArray.append(("18:00:00", 0));
timeArray.append(("19:00:00", 0));
timeArray.append(("20:00:00", 0));
timeArray.append(("21:00:00", 0));
timeArray.append(("22:00:00", 0));
timeArray.append(("23:00:00", 0));
contentTypeArray = [];
mimeTypeArray = [];
transferEncodingArray = [];
sentCountArray = [];
receivedCountArray = [];
messageIdArray = [];

userKeys = user_email_map.user_email_map.keys();

for user in userKeys:
	sentCountArray.append((user, 0));
	receivedCountArray.append((user, 0));

csvFile = open("../clean_data/output/cleaned_data.csv", "r");
print("Reading CSV lines...", end='', flush=True);
csvLines = csvFile.readlines();
print(" Done\nEmails found: " + str(len(csvLines)));
csvFile.close();
csvHeader = [];

for r, csvRecord in enumerate(csvLines):
	# print("Processing record #" + str(r) + " out of " + str(len(csvLines)));
	# Parse line into map
	csvRecord = csvRecord.rstrip('\n').split(',');

	if r == 0:
		csvHeader = csvRecord;
		continue;

	csvMap = {};

	for f, field in enumerate(csvRecord):
		csvMap[csvHeader[f]] = csvRecord[f];

	# Process sent & received
	for u, user in enumerate(userKeys):
		if user_email_map.user_email_map[user] in csvMap["From"]:
			sentCountArray[u] = (sentCountArray[u][0], sentCountArray[u][1] + 1);
		elif user_email_map.user_email_map[user] in csvMap["To"]:
			receivedCountArray[u] = (receivedCountArray[u][0], receivedCountArray[u][1] + 1);
		elif user_email_map.user_email_map[user] in csvMap["Cc"]:
			receivedCountArray[u] = (receivedCountArray[u][0], receivedCountArray[u][1] + 1);
		elif user_email_map.user_email_map[user] in csvMap["Bcc"]:
			receivedCountArray[u] = (receivedCountArray[u][0], receivedCountArray[u][1] + 1);

	# Process date
	date = parse(csvMap["Date"]);
	timeArray[int(f"{date:%H}")] = (timeArray[int(f"{date:%H}")][0], timeArray[int(f"{date:%H}")][1] + 1);

	# Process Content-Type
	found = False;

	for c, contenttype in enumerate(contentTypeArray):
		if contenttype[0] == csvMap["Content-Type"]:
			contentTypeArray[c] = (contentTypeArray[c][0], contentTypeArray[c][1] + 1);
			found = True;
			break;

	if found == False:
		contentTypeArray.append((csvMap["Content-Type"],1));

	# Process Mime-Version
	found = False;

	for m, mimeType in enumerate(mimeTypeArray):
		if mimeType[0] == csvMap["Mime-Version"]:
			mimeTypeArray[m] = (mimeTypeArray[m][0], mimeTypeArray[m][1] + 1);
			found = True;
			break;

	if found == False:
		mimeTypeArray.append((csvMap["Mime-Version"],1));

	# Process Content-Transfer-Encoding
	found = False;

	for e, transferEncoding in enumerate(transferEncodingArray):
		if transferEncoding[0] == csvMap["Content-Transfer-Encoding"]:
			transferEncodingArray[e] = (transferEncodingArray[e][0], transferEncodingArray[e][1] + 1);
			found = True;
			break;

	if found == False:
		transferEncodingArray.append((csvMap["Content-Transfer-Encoding"],1));

	# Process Message-ID
	found = False;

	for d, messageId in enumerate(messageIdArray):
		if messageId[0] == csvMap["Message-ID-Server"]:
			messageIdArray[d] = (messageIdArray[d][0], messageIdArray[d][1] + 1);
			found = True;
			break;

	if found == False:
		messageIdArray.append((csvMap["Message-ID-Server"],1));
		
	if r % 1000 == 0:
		print("\rReading emails progress: " + str(round((r + 1) / len(csvLines) * 100, 2)) + "%", end='', flush=True);

print("\rReading emails progress: " + str(round((r + 1) / len(csvLines) * 100, 2)) + "%", end='', flush=True);
print("\nCompiling MS Excel report...", end='', flush=True);

# Write number of emails sent per user
for s, sentTuple in enumerate(sentCountArray):
	emailSentCountsSheet.write_row("A" + str(s + 2), [sentTuple[0], sentTuple[1]]);

# Write number of emails received per user
for r, receivedTuple in enumerate(receivedCountArray):
	emailReceivedCountsSheet.write_row("A" + str(r + 2), [receivedTuple[0], receivedTuple[1]]);

# Write number of emails sent each hour of day to sheet
for t, timeTuple in enumerate(timeArray):
	sentTimeSheet.write_row("A" + str(t + 2), [timeTuple[0], timeTuple[1]]);

# Write number of each content-type to sheet
for c, contentTypeTuple in enumerate(contentTypeArray):
	contentTypeSheet.write_row("A" + str(c + 2), [contentTypeTuple[0], contentTypeTuple[1]]);

# Write number of each mime-type to sheet
for m, mimeTypeTuple in enumerate(mimeTypeArray):
	mimeTypeSheet.write_row("A" + str(m + 2), [mimeTypeTuple[0], mimeTypeTuple[1]]);

# Write number of each Content-Transfer-Encoding to sheet
for e, transferEncodingTuple in enumerate(transferEncodingArray):
	transferEncodingSheet.write_row("A" + str(e + 2), [transferEncodingTuple[0], transferEncodingTuple[1]]);

# Write number of each message-id to sheet
for d, messageIdTuple in enumerate(messageIdArray):
	messageIdSheet.write_row("A" + str(d + 2), [messageIdTuple[0], messageIdTuple[1]]);

# Write some forumals
statsSheet.write_row("A1", ["Max Sent", "=MAX(SentEmailCounts!$B$2:$B$" + str(len(userKeys) + 1) + ")"]);
statsSheet.write_row("A2", ["Min Sent", "=MIN(SentEmailCounts!$B$2:$B$" + str(len(userKeys) + 1) + ")"]);
statsSheet.write_row("A3", ["Average Sent", "=AVERAGE(SentEmailCounts!$B$2:$B$" + str(len(userKeys) + 1) + ")"]);
statsSheet.write_row("A5", ["Max Received", "=MAX(ReceivedEmailCounts!$B$2:$B$" + str(len(userKeys) + 1) + ")"]);
statsSheet.write_row("A6", ["Min Received", "=MIN(ReceivedEmailCounts!$B$2:$B$" + str(len(userKeys) + 1) + ")"]);
statsSheet.write_row("A7", ["Average Received", "=AVERAGE(SentEmailCounts!$B$2:$B$" + str(len(userKeys) + 1) + ")"]);

#Create sent histogram
chart = excelFile.add_chart({"type": "column"});
chart.add_series({
    "name":       "=SentEmailCounts!$B$1",
    "categories": "=SentEmailCounts!$A$2:$A$" + str(len(userKeys) + 1),
    "values":     "=SentEmailCounts!$B$2:$B$" + str(len(userKeys) + 1),
});

chart.set_title ({
	"name": "Number of Email Sent by Each User",
    "name_font": {
    	"size": 24, 
    	"bold": True
	}
});
chart.set_x_axis({
	"name": "User",
    "name_font": {
    	"size": 18, 
    	"bold": True
	}
});
chart.set_y_axis({
	"name": "Number of Emails",
    "name_font": {
    	"size": 18, 
    	"bold": True
	}
});
graphSheet.insert_chart("A1", chart, {"x_offset": 25, "y_offset": 10, "x_scale": 5, "y_scale": 2});

#Create received histogram
chart = excelFile.add_chart({"type": "column"});
chart.add_series({
    "name":       "=ReceivedEmailCounts!$B$1",
    "categories": "=ReceivedEmailCounts!$A$2:$A$" + str(len(userKeys) + 1),
    "values":     "=ReceivedEmailCounts!$B$2:$B$" + str(len(userKeys) + 1),
});

chart.set_title ({
	"name": "Number of Email Received by Each User",
    "name_font": {
    	"size": 24, 
    	"bold": True
	}
});
chart.set_x_axis({
	"name": "User",
    "name_font": {
    	"size": 18, 
    	"bold": True
	}
});
chart.set_y_axis({
	"name": "Number of Emails",
    "name_font": {
    	"size": 18, 
    	"bold": True
	}
});
graphSheet.insert_chart("A31", chart, {"x_offset": 25, "y_offset": 10, "x_scale": 5, "y_scale": 2});

#Create Radar chart
chart = excelFile.add_chart({"type": "radar"});
chart.add_series({
    "name":       "=SentTime!$B$1",
    "categories": "=SentTime!$A$2:$A$" + str(t + 2),
    "values":     "=SentTime!$B$2:$B$" + str(t + 2),
});

chart.set_title ({
	"name": "Number of emails sent/received during the day",
    "name_font": {
    	"size": 24, 
    	"bold": True
	}
});
chart.set_x_axis({
	"name": "Hour",
    "name_font": {
    	"size": 18, 
    	"bold": True
	}
});
chart.set_y_axis({
	"name": "Count",
    "name_font": {
    	"size": 18, 
    	"bold": True
	}
});
graphSheet.insert_chart("A61", chart, {"x_offset": 25, "y_offset": 10, "x_scale": 2, "y_scale": 2});

#Create content type pie chart chart
chart = excelFile.add_chart({"type": "pie"});
chart.add_series({
    "name":       "=ContentType!$B$1",
    "categories": "=ContentType!$A$2:$A$" + str(c + 2),
    "values":     "=ContentType!$B$2:$B$" + str(c + 2),
});

chart.set_title ({
	"name": "Number of emails of each Content-Type",
    "name_font": {
    	"size": 24, 
    	"bold": True
	}
});
chart.set_x_axis({
	"name": "Content-Type",
    "name_font": {
    	"size": 18, 
    	"bold": True
	}
});
chart.set_y_axis({
	"name": "Count",
    "name_font": {
    	"size": 18, 
    	"bold": True
	}
});
graphSheet.insert_chart("A91", chart, {"x_offset": 25, "y_offset": 10, "x_scale": 2, "y_scale": 2});

#Create mime type pie chart chart
chart = excelFile.add_chart({"type": "pie"});
chart.add_series({
    "name":       "=MimeType!$B$1",
    "categories": "=MimeType!$A$2:$A$" + str(m + 2),
    "values":     "=MimeType!$B$2:$B$" + str(m + 2),
});

chart.set_title ({
	"name": "Number of emails of each MIME-Type",
    "name_font": {
    	"size": 24, 
    	"bold": True
	}
});
chart.set_x_axis({
	"name": "MIME-Type",
    "name_font": {
    	"size": 18, 
    	"bold": True
	}
});
chart.set_y_axis({
	"name": "Count",
    "name_font": {
    	"size": 18, 
    	"bold": True
	}
});
graphSheet.insert_chart("A121", chart, {"x_offset": 25, "y_offset": 10, "x_scale": 2, "y_scale": 2});

#Create transfer encoding pie chart chart
chart = excelFile.add_chart({"type": "pie"});
chart.add_series({
    "name":       "=TransferEncoding!$B$1",
    "categories": "=TransferEncoding!$A$2:$A$" + str(e + 2),
    "values":     "=TransferEncoding!$B$2:$B$" + str(e + 2),
});

chart.set_title ({
	"name": "Number of emails of each Transfer Encoding",
    "name_font": {
    	"size": 24, 
    	"bold": True
	}
});
chart.set_x_axis({
	"name": "Transfer Encoding",
    "name_font": {
    	"size": 18, 
    	"bold": True
	}
});
chart.set_y_axis({
	"name": "Count",
    "name_font": {
    	"size": 18, 
    	"bold": True
	}
});
graphSheet.insert_chart("A151", chart, {"x_offset": 25, "y_offset": 10, "x_scale": 2, "y_scale": 2});

#Create message-id pie chart chart
chart = excelFile.add_chart({"type": "pie"});
chart.add_series({
    "name":       "=MessageID!$B$1",
    "categories": "=MessageID!$A$2:$A$" + str(d + 2),
    "values":     "=MessageID!$B$2:$B$" + str(d + 2),
});

chart.set_title ({
	"name": "Number of emails of each Message-ID",
    "name_font": {
    	"size": 24, 
    	"bold": True
	}
});
chart.set_x_axis({
	"name": "Message-ID",
    "name_font": {
    	"size": 18, 
    	"bold": True
	}
});
chart.set_y_axis({
	"name": "Count",
    "name_font": {
    	"size": 18, 
    	"bold": True
	}
});
graphSheet.insert_chart("A181", chart, {"x_offset": 25, "y_offset": 10, "x_scale": 2, "y_scale": 2});

excelFile.close();
print(" Done");