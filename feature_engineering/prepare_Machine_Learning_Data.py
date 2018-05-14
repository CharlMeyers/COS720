import csv
import random
import string
import mmap

 
with open('cleaned_data_numerical_training.csv') as File:  
	with open('blacklistedIpAddresses.txt', 'rb', 0) as file, \
		mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as s:
		rows = []
		reader = csv.DictReader(File)
		for row in reader:
			blacklistedIpAddressFound = False
			possiblyMalicious = row['Possibly-Malicious']
			if s.find(str.encode(row['Received1'])) != -1:
        			blacklistedIpAddressFound = True
			elif s.find(str.encode(row['Received2'])) != -1:
        			blacklistedIpAddressFound = True
			elif s.find(str.encode(row['From-IP'])) != -1:
        			blacklistedIpAddressFound = True
			if possiblyMalicious == 'False':
				if blacklistedIpAddressFound == True:
					possiblyMalicious = True
			rows.append({'To': row['To'],'X-To': row['X-To'],'X-cc': row['X-cc'],'X-bcc': row['X-bcc'],'Cc': row['Cc'],'Bcc': row['Bcc'],'Possibly-Spam-Subject': row['Possibly-Malicious-Spam'],'Blacklisted-IP-Address': blacklistedIpAddressFound,'Possibly-Malicious': possiblyMalicious})

with open('output/data_for_decision_tree.csv', 'w') as csvfile:
    fieldnames = ['To','X-To','X-cc','X-bcc','Cc','Bcc','Possibly-Spam-Subject','Blacklisted-IP-Address','Possibly-Malicious']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)


    
