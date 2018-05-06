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


def shuffleHeaderWithXHeader(input, header, xHeader, everyCountChar, amountToMove):
	result = [i for i in input if header.replace(" ", "").lower() in i.lower() and "Subject:".lower() not in i.lower()]
	if len(result) >= 2:
		headerEmailAddress = result[0].split(header)[1].replace("\n", "")
		headerEmailAddressIndexInInput = input.index(result[0])
		result[0] = header + shiftString(headerEmailAddress, everyCountChar, amountToMove) + "\n"

		xHeaderResult = result[1].split(xHeader)[1]
		xHeaderResultIndexInInput = input.index(result[1])
		leftAngularBracketPosition = xHeaderResult.find("<") #Find position of <
		rightAngularBracketPosition = xHeaderResult.find(">") #Find position of >
		if leftAngularBracketPosition != -1:
			xHeaderResultName = xHeaderResult[:leftAngularBracketPosition-1].lower().replace('\"', '').replace(" ", "").replace("\n", "")
			xHeaderResultEmail = xHeaderResult[leftAngularBracketPosition+1:rightAngularBracketPosition]
			xHeaderResultRestOfString = xHeaderResult[rightAngularBracketPosition+1:]
			shiftedxHeaderResultName = '\"' + shiftString(xHeaderResultName, everyCountChar, amountToMove) + '\"'
			shiftedxHeaderResultEmail = "<" + shiftString(xHeaderResultEmail, everyCountChar, amountToMove) + ">"
			result[1] = xHeader + shiftedxHeaderResultName + " " + shiftedxHeaderResultEmail + xHeaderResultRestOfString
			if "\n" not in result[1]:
				result[1] = result[1] + "\n"
		else:
			xHeaderResultName = xHeaderResult.lower().replace(" ", "").replace("\n", "")
			result[1] = xHeader + shiftString(xHeaderResultName, everyCountChar, amountToMove)
			if "\n" not in result[1]:
				result[1] = result[1] + "\n"

		input[headerEmailAddressIndexInInput] = result[0]
		input[xHeaderResultIndexInInput] = result[1]

	return input

def shuffleBccAndCc(input, everyCountChar, amountToMove):
	ccResult = [i for i in input if "cc:" in i.lower() and "bcc:" not in i.lower()]
	if len(ccResult) > 1:
		headerEmailAddress = ccResult[0].split("Cc: ")[1].replace("\n", "")
		headerEmailAddressIndexInInput = input.index(ccResult[0])
		ccResult[0] = "Cc: " + shiftString(headerEmailAddress, everyCountChar, amountToMove) + "\n"

		xHeaderResult = ccResult[1].split("X-cc: ")[1]
		xHeaderResultIndexInInput = input.index(ccResult[1])
		leftAngularBracketPosition = xHeaderResult.find("<") #Find position of <
		rightAngularBracketPosition = xHeaderResult.find(">") #Find position of >
		if leftAngularBracketPosition != -1:
			xHeaderResultName = xHeaderResult[:leftAngularBracketPosition-1].lower().replace('\"', '').replace(" ", "").replace("\n", "")
			xHeaderResultEmail = xHeaderResult[leftAngularBracketPosition+1:rightAngularBracketPosition]
			xHeaderResultRestOfString = xHeaderResult[rightAngularBracketPosition+1:]
			shiftedxHeaderResultName = '\"' + shiftString(xHeaderResultName, everyCountChar, amountToMove) + '\"'
			shiftedxHeaderResultEmail = "<" + shiftString(xHeaderResultEmail, everyCountChar, amountToMove) + ">"
			ccResult[1] = "X-cc: " + shiftedxHeaderResultName + " " + shiftedxHeaderResultEmail + xHeaderResultRestOfString
			if "\n" not in ccResult[1]:
				ccResult[1] = ccResult[1] + "\n"
		else:
			xHeaderResultName = xHeaderResult.lower().replace(" ", "").replace("\n", "")
			ccResult[1] = "X-cc: " + shiftString(xHeaderResultName, everyCountChar, amountToMove)
			if "\n" not in ccResult[1]:
				ccResult[1] = ccResult[1] + "\n"

		input[headerEmailAddressIndexInInput] = ccResult[0]
		input[xHeaderResultIndexInInput] = ccResult[1]

	bccResult = [i for i in input if "bcc:" in i.lower()]
	if len(bccResult) > 1:
		headerEmailAddress = bccResult[0].split("Bcc: ")[1].replace("\n", "")
		headerEmailAddressIndexInInput = input.index(bccResult[0])
		bccResult[0] = "Bcc: " + shiftString(headerEmailAddress, everyCountChar, amountToMove) + "\n"

		xHeaderResult = bccResult[1].split("X-bcc: ")[1]
		xHeaderResultIndexInInput = input.index(bccResult[1])
		leftAngularBracketPosition = xHeaderResult.find("<") #Find position of <
		rightAngularBracketPosition = xHeaderResult.find(">") #Find position of >
		if leftAngularBracketPosition != -1:
			xHeaderResultName = xHeaderResult[:leftAngularBracketPosition-1].lower().replace('\"', '').replace(" ", "").replace("\n", "")
			xHeaderResultEmail = xHeaderResult[leftAngularBracketPosition+1:rightAngularBracketPosition]
			xHeaderResultRestOfString = xHeaderResult[rightAngularBracketPosition+1:]
			shiftedxHeaderResultName = '\"' + shiftString(xHeaderResultName, everyCountChar, amountToMove) + '\"'
			shiftedxHeaderResultEmail = "<" + shiftString(xHeaderResultEmail, everyCountChar, amountToMove) + ">"
			bccResult[1] = "X-bcc: " + shiftedxHeaderResultName + " " + shiftedxHeaderResultEmail + xHeaderResultRestOfString
			if "\n" not in bccResult[1]:
				bccResult[1] = bccResult[1] + "\n"
		else:
			xHeaderResultName = xHeaderResult.lower().replace(" ", "").replace("\n", "")
			bccResult[1] = "X-bcc: " + shiftString(xHeaderResultName, everyCountChar, amountToMove)
			if "\n" not in bccResult[1]:
				bccResult[1] = bccResult[1] + "\n"

		input[headerEmailAddressIndexInInput] = bccResult[0]
		input[xHeaderResultIndexInInput] = bccResult[1]

	return input

def shuffleXHeader(input, xHeader, everyCountChar, amountToMove):
	result = [i for i in input if xHeader.replace(" ", "").lower() in i.lower()]
	if len(result) >= 1:
		xHeaderResult = result[0].split(xHeader)[1]
		xHeaderResultIndexInInput = input.index(result[0])
		leftAngularBracketPosition = xHeaderResult.find("<") #Find position of <
		rightAngularBracketPosition = xHeaderResult.find(">") #Find position of >
		if leftAngularBracketPosition != -1:
			xHeaderResultName = xHeaderResult[:leftAngularBracketPosition-1].lower().replace('\"', '').replace(" ", "").replace("\n", "")
			xHeaderResultEmail = xHeaderResult[leftAngularBracketPosition+1:rightAngularBracketPosition]
			xHeaderResultRestOfString = xHeaderResult[rightAngularBracketPosition+1:]
			shiftedxHeaderResultName = '\"' + shiftString(xHeaderResultName, everyCountChar, amountToMove) + '\"'
			shiftedxHeaderResultEmail = "<" + shiftString(xHeaderResultEmail, everyCountChar, amountToMove) + ">"
			result[0] = xHeader + shiftedxHeaderResultName + " " + shiftedxHeaderResultEmail + xHeaderResultRestOfString
			if "\n" not in result[0]:
				result[0] = result[0] + "\n"
		else:
			xHeaderResultName = xHeaderResult.lower().replace(" ", "").replace("\n", "")
			result[0] = xHeader + shiftString(xHeaderResultName, everyCountChar, amountToMove)
			if "\n" not in result[0]:
				result[0] = result[0] + "\n"

		input[xHeaderResultIndexInInput] = result[0]

	return input

def anonymiseSenderAndReceiver(input, everyCountChar, amountToMove):
	print(input)
	input = shuffleHeaderWithXHeader(input, "From: ", "X-From: ", everyCountChar, amountToMove)
	input = shuffleHeaderWithXHeader(input, "To: ", "X-To: ", everyCountChar, amountToMove)
	input = shuffleBccAndCc(input, everyCountChar, amountToMove)

	return input


def removeHeader(input, header):
	result = [i for i in input if header.replace(" ", "").lower() in i.lower()]
	if len(result) >= 1:
		xHeaderResultIndexInInput = input.index(result[0])
		result[0] = ""

		input[xHeaderResultIndexInInput] = result[0]

	return input

def removeUnneededHeaders(input):
	input = removeHeader(input, "X-Folder:")
	input = removeHeader(input, "X-FileName:")
	input = removeHeader(input, "X-Origin:")

	return input