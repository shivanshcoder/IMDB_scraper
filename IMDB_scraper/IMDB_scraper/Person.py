from urllib.request import urlopen

from bs4 import BeautifulSoup
from DataBase import connectDB, WORK_CATEGORY, fillWorkCategory
import mysql
import json
import time
 
class Person(object):
	"""
		Handles the Persons
	"""


	def __init__(self, id):
		"""
			@desc: Basic Constructor of the class
			@param: (id) uniqiue numeric to identify a particual person
			@return: None
		"""

		self.id = id
		self.id_str = "000000" + str(id)
		self.name = ""
		self.works = {}
		self.relations = {}
		self.knownFor = []
		self.presentInDB = False
		#add other misc data later on!
		self.imagePath = ""


	def commitDB(self):
		"""
			@desc: 
				Saves or Updates the data of the person in the Database
				Deletes the person from the list of to be scraped people
			@param: None
			@return: None
		"""		
		dbConn = connectDB()
		dbCursor = dbConn.cursor()

		#Save the new Work Category if any in the DB
		#We need to commit the works before because the tables use foreign key constraint
		for works in self.works:
			if not works in WORK_CATEGORY:
				dbCursor.execute("INSERT INTO work_category(name) VALUES(%s) ",(works,))	
		dbConn.commit()



		#Save the Data in the person in DB
		query = "INSERT INTO person VALUES(%s, %s, %s) ON DUPLICATE KEY UPDATE misc=%s"
		misc = { 
			"imagePath"	:self.imagePath,
			"knownFor"	:self.knownFor
		}
		data = (self.id, self.name,json.dumps(misc),json.dumps(misc), )
		dbCursor.execute(query,data)
		

		if not self.presentInDB:
			#Save the Work in the DB also 
			query = "INSERT INTO work VALUES(%s, %s, %s) ON DUPLICATE KEY UPDATE person_id=%s"
			query2 = "INSERT INTO titles_to_scrape VALUES(%s,100) ON DUPLICATE KEY UPDATE priority=priority+1"
			fillWorkCategory()
			for works in self.works:

				for titles in self.works[works]:
					dbCursor.execute(query, (titles, self.id, WORK_CATEGORY[works], self.id ))
					dbCursor.execute(query2, (titles,))





		#Delete the entry of this person from persosn_to_scrape DB
		dbCursor.execute("UPDATE persons_to_scrape SET priority=0 WHERE id=%s", (self.id,))

		dbConn.commit()
		dbConn.close()


	def checkInDB(self, loadData=True, loadWorks=True, loadRelations=True):
		"""
			@desc: Checks if the data of person exists in the DB
			@param: 
				(loadData) defines whether to fill the basic Data
				(loadRelations) defines whether to fill the relations data in the object
				(loadWorks) defines whether to fill the works data in the object
			@return: True if the data exists in DB
		"""
		try:
			dbConn = connectDB()
			dbCursor = dbConn.cursor()

			dbCursor.execute("SELECT * FROM person WHERE id=%s", (self.id, ))

			result = dbCursor.fetchone()

			#No record found for the person
			if result == None:
				dbConn.close()
				return False
			self.presentInDB = True
			dbCursor.execute("UPDATE persons_to_scrape SET priority=0 WHERE id=%s", (self.id,))
			dbConn.commit()

			if loadData:
				#Fill the Data from the DB
				self.name = result[1]
				misc_data = json.loads(result[2])

				self.imagePath = misc_data["imagePath"]
				self.knownFor = misc_data["knownFor"]

			if loadRelations:
				dbCursor.execute("SELECT des_id, work_id, score FROM relations WHERE src_id=%s", (self.id,))
				data1 = dbCursor.fetchall()

				dbCursor.execute("SELECT src_id, work_id, score FROM relations WHERE des_id=%s", (self.id,))
				data2 = dbCursor.fetchall()

				data = data1 + data2

				for temp in data:
					self.relations[temp[1]] = temp[2]

			if loadWorks:
				query = """	SELECT work.title_id, work_category.name FROM work
							INNER JOIN work_category ON work.work_id=work_category.id
							WHERE work.person_id=%s
						"""
				dbCursor.execute(query, (self.id,))
				data = dbCursor.fetchall()
				for d in data:
					if d[1] not in self.works:
						self.works[d[1]] = []
					self.works[d[1]].append(d[0])

			dbConn.close()
			return True
		except mysql.connector.Error as Err:
			print(Err)
			return False


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

		#Get the BeautifulSoup Object
		html = urlopen("https://www.imdb.com/name/nm"+self.id_str)
		bsObj = BeautifulSoup(html)

		self.name = bsObj.find("h1", {"class":"header"}).span.getText()
		#Get the image source
		imagePath = bsObj.find("div", {"class":"image"})
		if imagePath != None:
			self.imagePath = ""

		#Get the Known For titles!
		
		temp = bsObj.findAll("a", {"class":"knownfor-ellipsis"})
		for t in temp:
			self.knownFor.append(t.attrs["href"].split('/')[2][2:])


		#Get the Work!
		workCategory = []

		tempWorkCategory =[]
		tempworkCategory = bsObj.find("div", {"id": "filmography"}).findAll("div", {"class": "head"})
		for w in tempworkCategory:
			workCategory.append(w.attrs['data-category'])

		works = bsObj.find("div", {"id": "filmography"}).findAll("div", {"class": "filmo-category-section"})

		for w in range(0, len(workCategory)):
			workTitles = works[w].findAll("div", {"class": "filmo-row"})
			self.works[workCategory[w]] = []
			for wt in workTitles:
				self.works[workCategory[w]].append(wt.attrs['id'].split('-')[1][2:])


	def fillNeighbours(self):
		
		for movie in self.movies:

			#sending a mutable list to hold the movie name
			movieName = []
			actors_list = GetCastIDs(movie, movieName)
			print("Getting actors of movie "+ movieName[0])

			for actor in actors_list:
				if actor in self.neighbour_actors:

					self.neighbour_actors[actor] += 1
				else:
					self.neighbour_actors[actor] = 1

