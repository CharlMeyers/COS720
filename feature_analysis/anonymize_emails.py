import os;
import user_email_map_original;
# From https://pythonadventures.wordpress.com/tag/import-from-parent-directory/
def load_src(name, fpath):
    import imp;
    return imp.load_source(name, os.path.join(os.path.dirname(__file__), fpath))

load_src("anonymiser", "../anonymiser.py")
import anonymiser;

mainPath = "../maildir";

emailFile = open("user_email_map.py", "w");
emailFile.write("user_email_map = {\n");
userKeys = user_email_map_original.user_email_map.keys();

for user in userKeys:
	email = user_email_map_original.user_email_map[user];
	shuffledEmail = anonymiser.shuffleEmailAddress(email);	
	emailFile.write("\t\"" + user + "\": \"" + shuffledEmail + "\",\n");

emailFile.write("}\n");
emailFile.close();
