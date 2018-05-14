import os;

mainPath = "../maildir";

emailFile = open("user_email_map.py", "w");
emailFile.write("user_email_map = {\n");

for user in os.listdir(mainPath):
	userPath = mainPath + "/" + user;
	userSentPath = userPath + "/sent_items/";

	try:
		sentFileNames = os.listdir(userSentPath);

		for emailName in sentFileNames:
			emailPath = userSentPath + emailName;
			if os.path.isdir(emailPath):
				continue;
			email = open(emailPath,"r");
			emailLines = email.readlines();

			for line in emailLines:
				line = line.rstrip('\n');

				if line == "":
					break;
				if line.startswith("From: "):
					header, sep, email = line.partition(" ");						
					emailFile.write("\t\"" + user + "\": \"" + email + "\",\n");
					break;

			break;
	except FileNotFoundError as e:
		userSentPath = userPath + "/sent/";

		try:
			sentFileNames = os.listdir(userSentPath);

			for emailName in sentFileNames:
				emailPath = userSentPath + emailName;
				if os.path.isdir(emailPath):
					continue;
				email = open(emailPath,"r");
				emailLines = email.readlines();

				for line in emailLines:
					line = line.rstrip('\n');

					if line == "":
						break;
					if line.startswith("From: "):
						header, sep, email = line.partition(" ");
						shuffledEmail = anonymiser.shuffleEmailAddress(email);						
						emailFile.write("\t\"" + user + "\": \"" + shuffledEmail + "\",\n");
						break;

				break;
		except FileNotFoundError as e:
			emailFile.write("\t\"" + user + "\": \"\",\n");

emailFile.write("}\n");
emailFile.close();
