from urllib.request import urlopen

from bs4 import BeautifulSoup
from DataBase import connectDB 
import mysql
import json

import time

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
				dbConn.close()
				return False
			
			dbCursor.execute("UPDATE titles_to_scrape SET priority=0 WHERE id=%s", (self.id,))
			#dbCursor.execute("DELETE FROM titles_to_scrape WHERE id=%s",(self.id,))
			dbConn.commit()
			if loadData:
				#Fill the Data from the DB
				self.name = result[1]
				misc_data = json.loads(result[2])

				self.imagePath = misc_data["imagePath"]
			dbConn.close()
			return True
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

		mainData = bsObj.find("div", {"id":"fullcredits_content"})
		
		mainTables = mainData.findAll("table")
		casts = []
		#Each table contains the the cast crew data
		for table in mainTables:
			
			temp = table.findAll("td", {"class": "name"})

			if temp == []:
				temp = table.findAll("td", {"class":"primary_photo"})

			for t in temp:
				casts.append(t.a.attrs['href'].split('/')[2][2:])

		self.castCrew = casts


	def scrapeData(self, forceCheck=False):
		"""
			@desc: 
				Scrapes the Data from the Website
			@param: 
				(forceCheck) whether to Forcefully check from Web
			@return: None
		"""

		#Check for data in Database
		if self.checkInDB() and not forceCheck:
			return

		html = urlopen("https://www.imdb.com/title/tt"+str(self.id_str)+"/fullcredits")
		bsObj = BeautifulSoup(html)

		self.name = bsObj.find("h3", {"itemprop": "name" }).a.getText()

		imagePath = bsObj.find("img", {"class":"poster"})
		if imagePath:
			self.imagePath = imagePath.attrs['src']
		self.scrapeCastCrew(bsObj)


	def commitDB(self):
		"""
			@desc: 
				Saves or Updates the data of the title in the Database
				Deletes the title from the list of to be scraped title
			@param: None
			@return: None
		"""

		dbConn = connectDB()
		dbCursor = dbConn.cursor()

		#Save the data in title in DB
		query = "INSERT INTO title VALUES(%s, %s, %s) ON DUPLICATE KEY UPDATE misc=%s"
		misc = {
			"imagePath" : self.imagePath	
		}
		data = (self.id, self.name, json.dumps(misc), json.dumps(misc), )
		dbCursor.execute(query, data)

		for cast in self.castCrew:
			dbCursor.execute("INSERT INTO persons_to_scrape VALUES(%s, 100) ON DUPLICATE KEY UPDATE priority=priority+1", (cast, ))
		
		#Delete the entry of this person from persosn_to_scrape DB
		dbCursor.execute("DELETE FROM titles_to_scrape WHERE id=%s",(self.id,))
		dbConn.commit()
		dbConn.close()
