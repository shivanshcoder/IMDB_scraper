import mysql.connector
import random

dbConn =  mysql.connector.connect(
		host="localhost",
		user="root",
		passwd="ROOT#321", 
		database="testdb"
	)

dbCursor = dbConn.cursor()

for i in range(10000, 1000000):
	try:
		for j in range(0, random.randint(0,50)):
			dbCursor.execute("INSERT INTO movie_cast VALUES(%s, %s, %s)", (i, random.randint(0, max(i, 51)), "actor"))

	except:
		continue
	print("Saving Data i: "+ str(i))
	dbConn.commit()