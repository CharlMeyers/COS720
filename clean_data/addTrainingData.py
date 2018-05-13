import csv
import zipfile

small_file = "F:/UserData/My Documents/Coding Stuff/COS720/output/cleaned_data_numerical/output/cleaned_data_numerical_small.csv"
big_file = "F:/UserData/My Documents/Coding Stuff/COS720/output/cleaned_data_numerical/output/cleaned_data_numerical.csv"

small_training_file = "output/cleaned_data_numerical-training_small.csv"
big_training_file = "output/cleaned_data_numerical_training.csv"

small_zip_file = "output/cleaned_data_numerical-training_small.zip"
big_zip_file = "output/cleaned_data_numerical_training.zip"

def addAndWriteTrainingData(inFile, outFile):
    print("Adding training data to file....")
    with open(inFile) as csvFile:
        reader = csv.DictReader(csvFile)
        data = [r for r in reader]
        dataLength = len(data)
        for index in range(dataLength):
            subject = data[index]['Subject']
            to = int(data[index]['X-To'])
            cc = int(data[index]['X-cc'])
            bcc = int(data[index]['X-bcc'])

            moreBccThanTo = round((cc / bcc) * 100, 2)
            moreBccThanCc = round((to / bcc) * 100, 2)
            moreTo = False
            moreCc = False

            subjectLength = len(subject)
            countSpecialCharactersInSubject = subject.count("!") + subject.count("$")
            countUpperCaseCharactersInSubject = 0

            for s in subject:
                if(s.isupper()):
                    countUpperCaseCharactersInSubject += 1

            containsSpecialChars = False
            upperWholeOfSubject = False

            if moreBccThanCc < 30.00:                
                moreCc = True

            if moreBccThanTo < 30.00:
                moreTo = True

            if countSpecialCharactersInSubject >= 1:
                containsSpecialChars = True

            if subjectLength != 0 and countUpperCaseCharactersInSubject == subjectLength:                      
                upperWholeOfSubject = True            

            possibleSpam = moreCc or moreTo or containsSpecialChars or upperWholeOfSubject

            data[index]['Special-Chars-Subject'] = countSpecialCharactersInSubject                        
            data[index]['Count-Uppercase-Chars-Subject'] = countUpperCaseCharactersInSubject
            data[index]['Cc-Less-Than-Bcc'] = moreBccThanCc
            data[index]['To-Less-Than-Bcc'] = moreBccThanTo
            data[index]['Cc-Less'] = moreCc
            data[index]['To-Less'] = moreTo
            data[index]['Subject-Length'] = subjectLength
            data[index]['Possibly-Malicious-Spam'] = containsSpecialChars or upperWholeOfSubject
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