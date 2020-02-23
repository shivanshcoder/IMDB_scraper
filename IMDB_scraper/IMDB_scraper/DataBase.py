import sqlite3

#conn = sqlite3.connect('imdb.db')


def createTable():
	conn = sqlite3.connect('store.db')

	#Creates the Table for storing Actor details
	conn.execute('''CREATE TABLE actors
					(ID INT PRIMARY KEY NOT NULL,
					NAME TEXT NOT NULL);''')
	
	conn.close()

def InsertData(id, name):
	conn = sqlite3.connect('store.db')

	cursor = conn.cursor()
	cursor.execute("INSERT INTO actors VALUES("+id+","+name+");")
	cursor.commit()

	conn.close()


def PrintTable():
	con = sqlite3.connect('store.db')

	con.execute("")

	con.close()