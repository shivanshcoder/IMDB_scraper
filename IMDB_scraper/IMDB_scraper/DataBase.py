import sqlite3
import mysql.connector
from enum import Enum


DATABASE_NAME = "IMDB_scraper"

# Tables with their corresponding queries 
TABLES = {

	#	Defines a table which stores the data regarding the persons on the website
	#	misc stores the miscellanous data regarding the person
	"person": 
		"""CREATE TABLE person(
			id MEDIUMINT UNSIGNED PRIMARY KEY, 
			name VARCHAR(140) NOT NULL,
			misc JSON
			)""",

	#	Defines a table which stores the realtionships between the person with respect to a particular work in a common title 
	"relations":
		"""CREATE TABLE relations(
			src_id MEDIUMINT UNSIGNED NOT NULL,
			des_id MEDIUMINT UNSIGNED NOT NULL,
			work_id TINYINT UNSIGNED NOT NULL,
			score SMALLINT UNSIGNED DEFAULT 1,
			FOREIGN KEY(work_id) REFERENCES work_category(id)
			)""",

	#	Defines a table which stores the data regarding the person who worked in a given title
	"work":
		"""CREATE TABLE work(
			title_id INT UNSIGNED NOT NULL,
			person_id MEDIUMINT UNSIGNED NOT NULL,
			work_id TINYINT UNSIGNED ,
			FOREIGN KEY (work_id) REFERENCES work_category(id)
			)""",
	
	#	Defines a table which stores the data regarding the title on the website
	#	misc stores the miscellanous data regarding the title
	"title":
		"""CREATE TABLE title(
			id INT UNSIGNED PRIMARY KEY,
			name VARCHAR(255) NOT NULL,
			misc JSON
		)""",


	#	Defines a table which stores the various work categories available on the website
	"work_category":
		"""CREATE TABLE work_category(
			id TINYINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
			name VARCHAR(100) UNIQUE
		)""",

	#	Defines a table which stores the pending persons to be scraped
	"persons_to_scrape":
		"CREATE TABLE persons_to_scrape(id MEDIUMINT UNSIGNED PRIMARY KEY, priority TINYINT UNSIGNED DEFAULT 1)",

	"titles_to_scrape":
		"CREATE TABLE titles_to_scrape(id MEDIUMINT UNSIGNED PRIMARY KEY, priority TINYINT UNSIGNED DEFAULT 1)",
		
}

TABLES_LIST = [
	"work_category",
	"person",
	"relations",
	"work",
	"title",
	"persons_to_scrape",
	"titles_to_scrape"
	]

WORK_CATEGORY = {}

class WorkCategory:
	pass

def connectDB():
	db_conn =  mysql.connector.connect(
		host="localhost",
		user="root",
		passwd="ROOT#321", 
		database="imdb_scraper"
	)

	return db_conn


# Checks for the Database and all the necessary tables for the scraper
def checkScraperDB():

	#Return if the checking has already been done
	if hasattr(checkScraperDB, "checkedDB"):
		return 
	else:
		checkScraperDB.checkedDB = True

	db_conn =  mysql.connector.connect(
		host="localhost",
		user="root",
		passwd="ROOT#321"
	)


	#Creates the table if it doesn't exist
	def create_table_if_not_exists(db_cursor, table_name):
		try:
			db_cursor.execute("SELECT * from {} LIMIT 1".format(table_name))
			
			#db_cursor.execute("SELECT * from %s LIMIT 1",(table_name,))
			cc = db_cursor.fetchone()

		except mysql.connector.Error as Err:
			#print(Err)
			db_cursor.execute(TABLES[table_name])

	try:
		#Try using the DATABASE
		db_cursor = db_conn.cursor()
		db_cursor.execute("USE "+ DATABASE_NAME )

	except mysql.connector.Error as err:
		#Create the DATABASE and use it
		db_cursor.execute("CREATE DATABASE "+ DATABASE_NAME)
		db_cursor.execute("USE "+ DATABASE_NAME)

	finally:

		for tables in TABLES_LIST:
			create_table_if_not_exists(db_cursor, tables)

	db_conn.close()

def fillWorkCategory():
	dbConn = connectDB()
	dbCursor = dbConn.cursor()

	dbCursor.execute("SELECT * FROM work_category")
	temp = dbCursor.fetchall()
	for t in temp:
		WORK_CATEGORY[t[1]] = t[0]


def iniDB():

	try:
		checkScraperDB()
		fillWorkCategory()

	except:
		print("Error occured During Database Initialization")



def getTopPersons(num = 5):
	"""
		@desc: 
			Returns a list of ids of persons which are yet to be scraped from web
		@param:
			(num) Number of ids to be retrieved from the DB
		@return:
			list of numerical ids
	"""

	dbConn = connectDB()
	dbCursor = dbConn.cursor()
	try:
		dbCursor.execute("SELECT id FROM persons_to_scrape ORDER BY priority DESC LIMIT %s", (num,))
	except mysql.connector.Error as Err:
		print(Err)
		return []

	personList = []
	for d in dbCursor:
		personList.append(d[0])

	dbConn.close()
	return personList

def getTopTitles(num = 5):
	"""
		@desc: 
			Returns a list of ids of titles which are yet to be scraped from web
		@param:
			(num) Number of ids to be retrieved from the DB
		@return:
			list of numerical ids
	"""
	dbConn = connectDB()
	dbCursor = dbConn.cursor()

	try:
		dbCursor.execute("SELECT id FROM titles_to_scrape ORDER BY priority DESC LIMIT %s", (num,))
	except mysql.connector.Error as Err:
		print(Err)
		return []

	titleList = []
	for d in dbCursor:
		titleList.append(d[0])
	dbConn.close()
	return titleList 


