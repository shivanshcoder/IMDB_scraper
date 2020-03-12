
from IMDB_scraper import * 
from DataBase import connectDB, WORK_CATEGORY
from mysql.connector import Error
import json
 
class Person(object):
	"""
		Handles the Persons
	"""


	def __init__(self, id):
		"""
			@desc: Basic Constructor of the class
			@param: None
			@return: None
		"""

		self.id = id
		self.id_str = "000000" + str(id)
		self.name = ""
		self.works = {}
		self.relations = {}

		#add other misc data later on!
		self.imagePath = ""


	def commitDB(self):
		"""
			@desc: Saves or Updates the data of the person in the Database
			@param: None
			@return: None
		"""		
		dbConn = connectDB()
		dbCursor = dbConn.cursor()

		query = "INSERT INTO person VALUES(%s, %s, %s) ON DUPLICATE KEY UPDATE misc=%s"
		misc = { "imagePath":	self.imagePath	}
		data = (self.id, self.name,misc,misc , )

		dbCursor.execute(query,data)
		dbConn.commit()
		dbConn.close()


	def checkInDB(self, loadData=False):
		"""
			@desc: Checks if the data of person exists in the DB
			@param: loadData defines whether to fill the class members or not
			@return: True if the data exists in DB
		"""
		try:
			dbConn = connectDB()
			dbCursor = dbConn.cursor()

			dbCursor.execute("SELECT * FROM person WHERE id=%s", (self.id, ))

			result = dbCursor.fetchone()

			#No record found for the person
			if result == None:
				return False

			if loadData:
				#Fill the Data from the DB
				self.name = result[1]
				misc_data = json.loads(result[2])

				self.imagePath = misc_data["imagePath"]
				self.knownFor = misc_data["knownFor"]
				self.works = misc_data["works"]


		except Error as Err:
			print(Err)
			return False


	def scrapeData(self, forceCheck=False):
		"""
			@desc: Scrapes the Data from the Website
			@param: forceCheck(Forcefully check from Web)
			@return: None
		"""
		#Scrape the data only if it is not available on Database

		#Check for data in Database
		if self.checkInDB() and not forceCheck:
			return

		#Get the BeautifulSoup Object
		html = urlopen("https://www.imdb.com/name/nm"+self.id_str)
		self.bsObj = BeautifulSoup(html)


		self.name = self.bsObj.find("title").getText()

		#Get the image source
		self.imagePath = bsObj.find("div", {"class":"image"}).a.img.attrs["src"]

		#Get the Known For titles!
		self.knownFor = []
		temp = bsObj.findAll("a", {"class":"knownfor-ellipsis"})
		for t in temp:
			knownFor.append(t.attrs["href"].split('/')[2][2:])


		#Get the Work!
		workCategory = []

		
		workCategory = bsObj.find("div", {"id": "filmography"}).findAll("div", {"class": "head"})

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

