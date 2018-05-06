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


def shuffleHeaderWithXHeader(input, header, xHeader, everyCountChar, amountToMove, excludeHeader=None):
	result = [i for i in input if header.replace(" ", "").lower() in i.lower() and (True if excludeHeader is None else excludeHeader.replace(" ", "").lower() not in i.lower())]	
	if len(result) > 1:
		headerEmailAddressIndexInInput = input.index(result[0])
		splitHeader = result[0].split(header)
		if len(splitHeader) > 1:			
			headerValue = splitHeader[1].replace("\n", "").replace("\t", "")
			emailAddresses = headerValue.split(", ")

			emailAddressesLength = len(emailAddresses)
			for i in range(emailAddressesLength):
				localPart = emailAddresses[i].split("@")
				if i != emailAddressesLength - 1:
					emailAddresses[i] = shiftString(localPart[0], everyCountChar, amountToMove)	+ "@" + localPart[1] + ", "
				else:
					emailAddresses[i] = shiftString(localPart[0], everyCountChar, amountToMove)	+ "@" + localPart[1]

			result[0] = header + "".join(emailAddresses) + "\n"

			xHeaderResultIndexInInput = input.index(result[1])
			xHeaderResult = result[1].split(xHeader)[1]
			if xHeaderResult.find("<") > -1 and xHeaderResult.find(">") > -1:
				xHeaderValues = xHeaderResult.split(">, ")
				xHeaderValuesLength = len(xHeaderValues)
				for i in range(xHeaderValuesLength):
					value = xHeaderValues[i]
					leftAngularBracketPosition = value.find("<") #Find position of <				
					
					name = value[:leftAngularBracketPosition-1].lower().replace('\"', '').replace(" ", "").replace("\n", "")
					email = value[leftAngularBracketPosition+1:].replace("\n", "")
					shiftedName = '\"' + shiftString(name, everyCountChar, amountToMove) + '\"'

					if leftAngularBracketPosition > -1:
						if email.find("@") > -1:
							localPart = email.split("@")								
							shiftedEmail = "<" + shiftString(localPart[0], everyCountChar, amountToMove) + "@" + localPart[1] + ">"
						else:
							shiftedEmail = "<" + shiftString(email, everyCountChar, amountToMove) + ">"
					else:
						if email.find("@") > -1:
							localPart = email.split("@")								
							shiftedEmail = shiftString(localPart[0], everyCountChar, amountToMove) + "@" + localPart[1]
						else:
							shiftedEmail = shiftString(email, everyCountChar, amountToMove)

					if i != xHeaderValuesLength - 1:
						xHeaderValues[i] = shiftedName + " " + shiftedEmail + ", "
					else:
						xHeaderValues[i] = shiftedName + " " + shiftedEmail

				result[1] = xHeader + "".join(xHeaderValues)

				if "\n" not in result[1]:
					result[1] = result[1] + "\n"
			else:
				xHeaderValues = xHeaderResult.lower().replace("\n", "").split(", ")
				xHeaderValuesLength = len(xHeaderValues)
				for i in range(xHeaderValuesLength):
					value = xHeaderValues[i].replace(" ", "")

					if value.find("@") > -1:
						localPart = value.split("@")
						shiftedValue = 	shiftString(localPart[0], everyCountChar, amountToMove) + "@" + localPart[1]
					else:
						shiftedValue = shiftString(value, everyCountChar, amountToMove)

					if i != xHeaderValuesLength - 1:
						xHeaderValues[i] = shiftedValue + ", "
					else:
						xHeaderValues[i] = shiftedValue

				result[1] = xHeader + "".join(xHeaderValues)
				if "\n" not in result[1]:
					result[1] = result[1] + "\n"

			input[headerEmailAddressIndexInInput] = result[0]
			input[xHeaderResultIndexInInput] = result[1]

	return input


def anonymiseSenderAndReceiver(input, everyCountChar, amountToMove):
	input = shuffleHeaderWithXHeader(input, "From: ", "X-From: ", everyCountChar, amountToMove, "Subject: ")
	input = shuffleHeaderWithXHeader(input, "To: ", "X-To: ", everyCountChar, amountToMove, "Subject: ")
	input = shuffleHeaderWithXHeader(input, "Cc: ", "X-cc: ", everyCountChar, amountToMove, "Bcc: ")
	input = shuffleHeaderWithXHeader(input, "Bcc: ", "X-bcc: ", everyCountChar, amountToMove)	

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