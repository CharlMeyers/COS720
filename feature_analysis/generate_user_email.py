import os;
# From https://pythonadventures.wordpress.com/tag/import-from-parent-directory/
def load_src(name, fpath):
    import imp;
    return imp.load_source(name, os.path.join(os.path.dirname(__file__), fpath))

load_src("utils", "../utils.py");
import utils;
load_src("anonymiser", "../anonymiser.py")
import anonymiser;

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
					shuffledEmail = anonymiser.shuffleEmailAddress(email, utils.EVERY_COUNT_CHARACTERS, utils.AMOUNT_TO_MOVE_EVERY_CHARACTER);							
					emailFile.write("\t\"" + user + "\": \"" + shuffledEmail + "\",\n");
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
						shuffledEmail = anonymiser.shuffleEmailAddress(email, utils.EVERY_COUNT_CHARACTERS, utils.AMOUNT_TO_MOVE_EVERY_CHARACTER);						
						emailFile.write("\t\"" + user + "\": \"" + shuffledEmail + "\",\n");
						break;

				break;
		except FileNotFoundError as e:
			emailFile.write("\t\"" + user + "\": \"\",\n");

emailFile.write("}\n");
emailFile.close();
