from datetime import datetime
import csv
import time;
import sqlite3
import paho.mqtt.client as mqtt
global flag1
flag1 = 0
global flag2
flag2 = 0
log1 = list()
log2 = list()
conn = sqlite3.connect('fp.db')
client = mqtt.Client()
client.connect("130.255.185.100",1883,60)
client.subscribe("fp/log",1)
client.subscribe("fp/id",1)
c = conn.cursor()

#c.execute('''CREATE TABLE FINGERPRINTS(EnrollID INTEGER, NAME text, EMPLOYEEID INTEGER)''')
#c.execute('''CREATE TABLE TIMELOG(date text, weekday1 text, name text, emid text, time1 text, workinghrs text)''')


def on_message(client,userdata,message):
	global flag1
	global flag2
	i = 0
	localtime = time.asctime(time.localtime(time.time()))
	weekday2 = localtime[0:3]
	date2 = localtime[4:10]+','+localtime[20:24]
	time2 = localtime[11:19]	 
	Enrollid = message.payload
	id = message.payload
	a = len(id)
	print(a)
	print(Enrollid)
	if a>3 :
		for i in range(100):
			if i < a:
				if Enrollid[i] <> '/' and Enrollid[i] <> ',':
					i = i + 1
				elif Enrollid[i] == ',': 
					name = Enrollid[0:i]
					b = i
				else:	
					emid2 = Enrollid[b+1:i] 
					fpid = Enrollid[i+1:a]
					print(name)
					print(emid2)
					print(fpid)
					fl = float(fpid)
					idz = int(fl)
					c.execute("INSERT INTO FINGERPRINTS VALUES ('%d','%s','%s')" %(idz,name,emid2))
					conn.commit()
					for row in c.execute("SELECT * FROM FINGERPRINTS"):
						print(row)
	else:	
		log1.append(message.payload)
		log2 = set(log1)
		log1len = len(log1)
		log2len = len(log2)
		f2 = float(Enrollid)
		idz2 = int(f2)
		for row in c.execute("SELECT NAME FROM FINGERPRINTS WHERE EnrollID = '%d' " %(idz2) ):
			emname=row[0]
			print(emname)  
			client.publish('fp/name',emname,1)
		for row in c.execute("SELECT EMPLOYEEID FROM FINGERPRINTS WHERE EnrollID = '%d' " %(idz2) ):
                        empid=row[0]
		if log1len == log2len:
			c.execute("INSERT INTO TIMELOG VALUES ('%s','%s','%s','%s','%s','0.0')" %(date2,weekday2,emname,empid,time2))
			conn.commit()
			for row in c.execute("SELECT * FROM TIMELOG"):
				print(row)
			print("entry")
		else:
			for row in c.execute("SELECT time1 FROM TIMELOG WHERE date = '%s' AND emid = '%d' ORDER BY time1 DESC" %(date2,empid)):
				wh = row[0]
				print(wh)
				print(time2)
				FMT = '%H:%M:%S'
				tdelta = datetime.strptime(time2, FMT) - datetime.strptime(wh, FMT)
				print(tdelta)
				break 
			c.execute("INSERT INTO TIMELOG VALUES ('%s','%s','%s','%s','%s','%s')" %(date2,weekday2,emname,empid,time2,tdelta))
			whdetails = emname + ',' + str(tdelta)
			client.publish('fp/wh',whdetails,1)
			print(whdetails)
			print("exit")
			log1.remove(message.payload)
			log1.remove(message.payload)


		
client.on_message = on_message

while True:
	localtime = time.asctime(time.localtime(time.time()))
        weekday3 = localtime[0:3]
	if weekday3 == 'Sun':
		data = c.execute("SELECT * FROM TIMELOG")
		with open('Timelog.csv','wb') as f:
			writer = csv.writer(f)
			writer.writerrow(['Date', 'Weekday', 'Name', 'EmployeeID','Time','Workinghrs'])	
			writer.writerows(data) 
		c.execute("DELETE FROM TIMELOG")
	client.loop() 


