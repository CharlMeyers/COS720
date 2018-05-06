def getNumDaysOfMonth(month, year):
	if month == 1:
		return 31;
	elif month == 2:
		if year % 4 != 0:
			return 28;
		elif year % 100 != 0:
			return 29;
		elif year % 400 != 0:
			return 28;
		else:
			return 29;
	elif month == 3:
		return 31;
	elif month == 4:
		return 30;
	elif month == 5:
		return 31;
	elif month == 6:
		return 30;
	elif month == 7:
		return 31;
	elif month == 8:
		return 31;
	elif month == 9:
		return 30;
	elif month == 10:
		return 31;
	elif month == 11:
		return 30;
	elif month == 12:
		return 31;

def convertTimestamp(timestamp):
	timestamp = timestamp[5:];
	day, sepearator, timestamp = timestamp.partition(" ");
	month, sepearator, timestamp = timestamp.partition(" ");
	year, sepearator, timestamp = timestamp.partition(" ");
	hour, sepearator, timestamp = timestamp.partition(":");
	minute, sepearator, timestamp = timestamp.partition(":");
	second, sepearator, timestamp = timestamp.partition(" ");
	timezone, sepearator, timestamp = timestamp.partition(" ");

	day = int(day);
	year = int(year);
	hour = int(hour);
	minute = int(minute);
	second = int(second);
	sign = timezone[:1];
	timezone = int(timezone[1:3]);

	if month == "Jan":
		month = 1;
	elif month == "Feb":
		month = 2;
	elif month == "Mar":
		month = 3;
	elif month == "Apr":
		month = 4;
	elif month == "May":
		month = 5;
	elif month == "Jun":
		month = 6;
	elif month == "Jul":
		month = 7;
	elif month == "Aug":
		month = 8;
	elif month == "Sep":
		month = 9;
	elif month == "Oct":
		month = 10;
	elif month == "Nov":
		month = 11;
	elif month == "Dec":
		month = 12;

	if sign == "-":
		hour -= timezone;

		if hour < 0:
			hour = 24 + hour;
			day -= 1;

			if day == 0:
				month -= 1;
				
				if month == 0:
					month = 12;
					year = year - 1;
				
				day = getNumDaysOfMonth(month, year);
	else:
		hour += timezone;

		if hour >= 24:
			hour = hour - 24;
			day += 1;

			if day > getNumDaysOfMonth(month, year):
				day = 1;
				month += 1;
				
				if month > 12:
					month = 1;
					year = year + 1;

	if day < 10:
		day = "0" + str(day);
	else:
		day = str(day);
	if month < 10:
		month = "0" + str(month);
	else:
		month = str(month);
	year = str(year);
	if hour < 10:
		hour = "0" + str(hour);
	else:
		hour = str(hour);
	if minute < 10:
		minute = "0" + str(minute);
	else:
		minute = str(minute);
	if second < 10:
		second = "0" + str(second);
	else:
		second = str(second);

	return year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second;
	