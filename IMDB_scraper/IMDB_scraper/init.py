from DataBase import iniDB, getTopPersons, getTopTitles
from Person import Person
from Title import Title
import time
import datetime

iniDB()

def startScraping():
	print(datetime.datetime.now())
	persons = []
	titles = []
	personi = 0
	titlei = 0
	#Number of ids to retrieve
	numIds = 10

	while(True):
		
		if len(persons) == 0:
			persons = getTopPersons(numIds)
			
		if len(titles) == 0:
			titles = getTopTitles(numIds)

		for personID in persons:
			print(personID)

			start = time.time()
			person = Person(personID)

			if not person.checkInDB(False, False, False):
				print("checked DB")
				personi+=1
				person.scrapeData()

				person.commitDB()
				end = time.time()
				
				print("{} scraping person {} : {}".format(personi, person.name, (end-start)))

		persons = []


		for titleID in titles:
			
			print(titleID)
			#start = time.time()
			title = Title(titleID)

			if not title.checkInDB(False):
				titlei+=1
				title.scrapeData()

				title.commitDB()

				end = time.time()
				print("{} scraping title {} : {}".format(titlei, title.name, (end-start)))

		titles = []
		

while(True):
	startScraping()
	try:
		pass
	except:
		print("Some Error Occured")
		continue