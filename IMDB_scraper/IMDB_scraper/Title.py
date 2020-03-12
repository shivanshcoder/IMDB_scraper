from urllib.request import urlopen

from bs4 import BeautifulSoup
from DataBase import connectDB 
from mysql.connector import Error
import json



class Title(object):
	"""
		Handles the titles
	
	"""


	def __init__(self, id):
		"""
			@desc: Basic Constructor of the class
			@return: None
			@params: id(id of the title)
		"""
		self.id = id

		#String id should have a length of atleast 7 digits so appending 6 zeroes
		#Extra sarting zeroes don't have effect on imdb
		self.id_str = "000000" + str(id)

		self.name = ""

		self.imagePath = ""

		self.castCrew = {}


	def checkInDB(self, loadData=False):
		"""
			@desc: Checks if the data of title exists in the DB
			@param: loadData defines whether to fill the class members or not
			@return: True if the data exists in DB
		"""
		try:
			dbConn = connectDB()
			dbCursor = dbConn.cursor()

			dbCursor.execute("SELECT * FROM title WHERE id=%s", (self.id, ))

			result = dbCursor.fetchone()

			#No record found for the person
			if result == None :
				return False
			

			if loadData:
				#Fill the Data from the DB
				self.name = result[1]
				misc_data = json.loads(result[2])

				self.castCrew = misc_data["castCrew"]
				self.imagePath = misc_data["imagePath"]


		except Error as Err:
			print(Err)
			return False


	def scrapeCastCrew(self, bsObj, loadData=False):
		"""
			@desc:
				Scrapes the Data from web and can save it in the object members
			@params:
				bsObj: BeautifulSoup Object which has the title page
				loadData: bool object defining whether should it load data in object members
			@return:
				None

		"""

		mainData = bsObj.find("div", {"class":"fullcredits_content"})
		

		#Get Cast Credits
		castListTable = mainData.find("table", {"class": "cast_list"})


		cast = []
		for sibling in bsObj.find("table", {"class":"cast_list"}).tr.next_siblings:
	
			#There is '\n' after every tag
			if sibling =='\n':
				continue
			
			if not 'class' in sibling.attrs:
				continue

			temp = sibling.td.next_sibling.next_sibling


			id = temp.a.attrs['href'].split('/')[2][2:]

			cast.append(int(id))
		self.castCrew["cast"] = cast

		pass


	def scrapeData(self):
		"""
			@desc: Scrapes the Data from the Web
			@param: None
			@return: None
		"""
		try:
			dbConn = connectDB() 
			dbCursor = dbConn.cursor()

			dbCursor.execute("SELECT * FROM movies WHERE id = %s", (self.id_str, ))

			result = dbCursor.fetchone()

			if result == None:
				#Need to be scraped from WEB
				html = urlopen("https://www.imdb.com/title/tt"+str(self.id_str)+"/fullcredits")
				bsObj = BeautifulSoup(html)
				
				self.name = bsObj.find("h3", {"itemprop": "name" }).a.getText()

				self.__scrapeCastCrew(bsObj)

				dbCursor.execute("INSERT INTO movies VALUES(%s, %s, %s)", (self.id, self.name, json.dumps(self.cast_crew)))
			
				dbConn.commit()
				dbConn.close()
			else:
				self.id = result[0]
				self.id_str = "000000" + str(self.id)
				self.name = result[1]
				self.castCrew = json.loads(result[2])

			
		except Error as Err:
			#maybe catch some DB exceptions
			print(Err)
			pass


	def commit(self):
		
		db_conn = connectDB()

		db_cursor = db_conn.cursor()

		#Check if movie already exists in DB
		db_cursor.execute("SELECT * FROM movie_cast WHERE movie_id = {}".format(self.id))

		for cast in db_cursor:
			db_cursor.execute("INSERT INTO movie_cast VALUES({}, {})".format(self.id, cast))
