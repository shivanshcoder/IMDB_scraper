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
			id MEDIUMINT PRIMARY KEY, 
			name VARCHAR(140) NOT NULL,
			misc JSON
			)""",

	#	Defines a table which stores the realtionships between the person with respect to a particular work in a common title 
	"relations":
		"""CREATE TABLE relations(
			src_id MEDIUMINT NOT NULL,
			des_id MEDIUMINT NOT NULL,
			work_id TINYINT NOT NULL,
			score SMALLINT DEFAULT 1,
			UNIQUE(src_id, des_id),
			FOREIGN KEY(work_id) REFERENCES work_category(id)
			)""",

	#	Defines a table which stores the data regarding the person who worked in a given title
	"work":
		"""CREATE TABLE work(
			title_id INT NOT NULL,
			actor_id MEDIUMINT NOT NULL,
			work_id TINYINT ,
			UNIQUE(title_id, actor_id),
			FOREIGN KEY (work_id) REFERENCES work_category(id)
			)""",
	
	#	Defines a table which stores the data regarding the title on the website
	#	misc stores the miscellanous data regarding the title
	"title":
		"""CREATE TABLE title(
			id INT PRIMARY KEY,
			name VARCHAR(140) NOT NULL,
			misc JSON
		)""",


	#	Defines a table which stores the various work categories available on the website
	"work_category":
		"""CREATE TABLE work_category(
			id TINYINT PRIMARY KEY AUTO_INCREMENT,
			name VARCHAR(100)
		)""",

	#	Defines a table which stores the pending persons to be scraped
	"persons_to_scrape":
		"CREATE TABLE persons_to_scrape(id MEDIUMINT PRIMARY KEY)",

	"titles_to_scrape":
		"CREATE TABLE titles_to_scrape(id MEDIUMINT PRIMARY KEY)",
		
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

	else:

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





