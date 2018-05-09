import csv
import random
import string
 
with open('cleaned_data.csv') as File:  
    rows = []
    received1 = 'by 10.79.39.198 with SMTP id '
    received2SecondPart = ' [137.215.98.179]) by mx.google.com with ESMTPS id '
    received2ThirdPart = ' (version=TLS1_2 cipher=AES128-GCM-SHA256 bits=128/128); '
    reader = csv.DictReader(File)
    for row in reader:
	fromServer = row['From'].split("@",1)[1]
	received2FirstPart = 'from ' + fromServer + ' (' + fromServer
	idDate = row['Date']
	idDate = idDate.replace('-', '.')
	idDate = idDate.replace(':', '.')
	idDate = idDate.replace('T', '.')
	id1 = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
	id1 += '; '
	id2 = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(14))
	id2 += '.' + idDate
        rows.append({'Message-ID': row['Message-ID'],'Date': row['Date'],'From': row['From'],'To': row['To'],'Subject': row['Subject'],'X-From': row['X-From'],'X-To': row['X-To'],'X-Mailer': '','Received1': received1 + id1 + row['Date'],'Received2': received2FirstPart + received2SecondPart + id2 + received2ThirdPart + row['Date']})

with open('data_for_machine_learning.csv', 'w') as csvfile:
    fieldnames = ['Message-ID','Date','From','To','Subject','X-From','X-To','X-Mailer','Received1','Received2']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
    
