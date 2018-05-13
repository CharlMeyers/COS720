import csv
import zipfile

small_file = "F:/UserData/My Documents/Coding Stuff/COS720/output/cleaned_data_numerical/output/cleaned_data_numerical_small.csv"
big_file = "F:/UserData/My Documents/Coding Stuff/COS720/output/cleaned_data_numerical/output/cleaned_data_numerical.csv"

small_training_file = "F:/UserData/My Documents/Coding Stuff/COS720/output/cleaned_data_numerical/output/cleaned_data_numerical-training_small.csv"
big_training_file = "F:/UserData/My Documents/Coding Stuff/COS720/output/cleaned_data_numerical/output/cleaned_data_numerical_training.csv"

small_zip_file = "F:/UserData/OneDrive/UniversiteitProjekte/COS720/Assignment/COS720/clean_data/output/cleaned_data_numerical-training_small.zip"
big_zip_file = "F:/UserData/OneDrive/UniversiteitProjekte/COS720/Assignment/COS720/clean_data/output/cleaned_data_numerical_training.zip"

def addAndWriteTrainingData(inFile, outFile):
    print("Adding training data to file....")
    with open(inFile) as csvFile:
        reader = csv.DictReader(csvFile)
        data = [r for r in reader]
        dataLength = len(data)
        for index in range(dataLength):
            fromIP = data[index]['From-IP']        
            subject = data[index]['Subject']
            to = int(data[index]['X-To'])
            cc = int(data[index]['X-cc'])
            bcc = int(data[index]['X-bcc'])

            moreBccThanTo = False
            moreBccThanCc = False
            validIP = False
            possibleSpamSubject = False

            if fromIP.replace(".", "").isdigit():
                validIP = True

            if round((cc / bcc) * 100, 2) < 30.00:
                moreBccThanCc = True

            if round((to / bcc) * 100, 2) < 30.00:
                moreBccThanTo = True

            if subject.find("!") > -1:
                possibleSpamSubject = True

            if subject.find("$") > -1:
                possibleSpamSubject = True

            if subject.isupper():
                possibleSpamSubject = True

            data[index]['Valid-IP'] = validIP

            possibleSpam = moreBccThanCc or moreBccThanTo or not validIP or possibleSpamSubject

            data[index]['Valid-IP'] = validIP
            data[index]['Possibly-Spam-Subject'] = possibleSpamSubject
            data[index]['Bcc-Larger-Than-CC'] = moreBccThanCc
            data[index]['Bcc-Larger-Than-To'] = moreBccThanTo
            data[index]['Possibly-Malicious'] = possibleSpam

        csvKeys = data[0].keys()

        print("Writing results to file...")
        with open(outFile, "w", newline='') as trainingCSv:    
            writer = csv.DictWriter(trainingCSv, csvKeys)
            writer.writeheader()
            writer.writerows(data)
        
        print('Done\n')

print('Adding training data to small sample...\n')
addAndWriteTrainingData(small_file, small_training_file)
print('Adding training data to big dataset...\n')
addAndWriteTrainingData(big_file, big_training_file)

print("Zipping files...\n")
print("Zipping large file...")
zf = zipfile.ZipFile(big_zip_file, mode="w")

try:
	zf.write(big_training_file, compress_type=zipfile.ZIP_DEFLATED)
finally:
	zf.close()

print("Zipping small file...")
zf = zipfile.ZipFile(small_zip_file, mode="w")

try:
	zf.write(small_training_file, compress_type=zipfile.ZIP_DEFLATED)
finally:
	zf.close()