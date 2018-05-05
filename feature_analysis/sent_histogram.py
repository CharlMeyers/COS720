import os;
import xlsxwriter;
from dateutil.parser import parse;

excelFile = xlsxwriter.Workbook("./output/sent_emails.xlsx");
graphSheet = excelFile.add_worksheet("Graphs");
statsSheet = excelFile.add_worksheet("DescriptiveStatistics");
emailCountsSheet = excelFile.add_worksheet("EmailCounts");
emailCountsSheet.write_row("A1", ["User", "Number of sent emails"]);
sentTimeSheet = excelFile.add_worksheet("SentTime");
sentTimeSheet.write_row("A1", ["Hour", "Count"]);
contentTypeSheet = excelFile.add_worksheet("ContentType");
contentTypeSheet.write_row("A1", ["Type", "Count"]);
mimeTypeSheet = excelFile.add_worksheet("MimeType");
mimeTypeSheet.write_row("A1", ["Type", "Count"]);
transferEncodingSheet = excelFile.add_worksheet("TransferEncoding");
transferEncodingSheet.write_row("A1", ["Type", "Count"]);
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

for i, user in enumerate(os.listdir("../maildir")):
	userPath = "../maildir/" + user;
	userSentPath = userPath + "/sent/";

	try:
		sentFileNames = os.listdir(userSentPath);
		print(user + " sent " + str(len(sentFileNames)) + " emails.");
		emailCountsSheet.write_row("A" + str(i + 2), [user, len(sentFileNames)]);

		for j, emailName in enumerate(sentFileNames):
			emailPath = userSentPath + emailName;
			if os.path.isdir(emailPath):
				continue;
			email = open(emailPath,"r");
			emailLines = email.readlines();

			for line in emailLines:
				line = line.rstrip('\n');

				if line == "":
					break;
				if line.startswith("Date: "):
					date = parse(line[6:]);
					timeArray[int(f"{date:%H}")] = (timeArray[int(f"{date:%H}")][0], timeArray[int(f"{date:%H}")][1] + 1);
				if line.startswith("Content-Type: "):
					found = False;

					for c, contenttype in enumerate(contentTypeArray):
						if contenttype[0] == line[14:]:
							contentTypeArray[c] = (contentTypeArray[c][0], contentTypeArray[c][1] + 1);
							found = True;
							break;

					if found == False:
						contentTypeArray.append((line[14:],1));
				if line.startswith("Mime-Version: "):
					found = False;

					for m, mimeType in enumerate(mimeTypeArray):
						if mimeType[0] == line[14:]:
							mimeTypeArray[m] = (mimeTypeArray[m][0], mimeTypeArray[m][1] + 1);
							found = True;
							break;

					if found == False:
						mimeTypeArray.append((line[14:],1));
				if line.startswith("Content-Transfer-Encoding: "):
					found = False;

					for e, transferEncoding in enumerate(transferEncodingArray):
						if transferEncoding[0] == line[27:]:
							transferEncodingArray[e] = (transferEncodingArray[e][0], transferEncodingArray[e][1] + 1);
							found = True;
							break;

					if found == False:
						transferEncodingArray.append((line[27:],1));

			email.close();
	except FileNotFoundError as e:
		print(user + " sent 0 emails.");
		emailCountsSheet.write_row("A" + str(i + 2), [user, 0]);

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

# Write some forumals
statsSheet.write_row("A1", ["Max", "=MAX(EmailCounts!$B$2:$B$" + str(i + 2) + ")"]);
statsSheet.write_row("A2", ["Min", "=MIN(EmailCounts!$B$2:$B$" + str(i + 2) + ")"]);
statsSheet.write_row("A3", ["Average", "=AVERAGE(EmailCounts!$B$2:$B$" + str(i + 2) + ")"]);

#Create histogram
chart = excelFile.add_chart({"type": "column"});
chart.add_series({
    "name":       "=EmailCounts!$B$1",
    "categories": "=EmailCounts!$A$2:$A$" + str(i + 2),
    "values":     "=EmailCounts!$B$2:$B$" + str(i + 2),
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

#Create Radar chart
chart = excelFile.add_chart({"type": "radar"});
chart.add_series({
    "name":       "=SentTime!$B$1",
    "categories": "=SentTime!$A$2:$A$" + str(t + 2),
    "values":     "=SentTime!$B$2:$B$" + str(t + 2),
});

chart.set_title ({
	"name": "Number of emails sent during each hour",
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
graphSheet.insert_chart("A31", chart, {"x_offset": 25, "y_offset": 10, "x_scale": 2, "y_scale": 2});

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
graphSheet.insert_chart("A61", chart, {"x_offset": 25, "y_offset": 10, "x_scale": 2, "y_scale": 2});

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
graphSheet.insert_chart("A91", chart, {"x_offset": 25, "y_offset": 10, "x_scale": 2, "y_scale": 2});

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
graphSheet.insert_chart("A121", chart, {"x_offset": 25, "y_offset": 10, "x_scale": 2, "y_scale": 2});

excelFile.close();
