from urllib.request import urlopen

from bs4 import BeautifulSoup

titleName = "tt4244998" #Alpha 2018

actorName = "nm10406540"

def GetMovieList(actorName):
	movie_list = []

	html = urlopen("https://www.imdb.com/name/"+actorName)
	bsObj = BeautifulSoup(html)
	
	movies_div = bsObj.find("div", {"class": "filmo-category-section"})
	movie_list.append(movies_div.div.attrs["id"].split('-')[-1])

	for sibling in movies_div.div.next_siblings:
		if sibling == '\n':
			continue

		movie_list.append(sibling.attrs["id"].split('-')[-1])

	#for titleName in movie_list:
	#	titleName = titleName

	return movie_list


def GetCast(titleName):
	our_array = {}
	html = urlopen("https://www.imdb.com/title/"+titleName+"/fullcredits?")
	bsObj = BeautifulSoup(html)
	tabls = bsObj.find("table", {"class":"cast_list"})

	for sibling in bsObj.find("table", {"class":"cast_list"}).tr.next_siblings:

		#There is '\n' after every tag
		if sibling =='\n':
			continue

		#Don't get names of the uncredited Actors
		if(sibling.td.attrs['class'] == ['castlist_label']):
			break

		temp = sibling.td.next_sibling.next_sibling
		name = temp.get_text()
		name = name.replace('\n','')
		id = temp.a.attrs['href'][8:-1]
		our_array[id] = name[1:-1]

	return our_array
	
def GetCastIDs(titleName):
	our_array = []
	html = urlopen("https://www.imdb.com/title/"+titleName+"/fullcredits?")
	bsObj = BeautifulSoup(html)
	tabls = bsObj.find("table", {"class":"cast_list"})

	for sibling in bsObj.find("table", {"class":"cast_list"}).tr.next_siblings:

		#There is '\n' after every tag
		if sibling =='\n':
			continue

		#Don't get names of the uncredited Actors
		if(sibling.td.attrs['class'] == ['castlist_label']):
			break

		temp = sibling.td.next_sibling.next_sibling
		id = temp.a.attrs['href'][8:-1]
		our_array.append(id)

	return our_array


#movie_list = GetMovieList(actorName)

#for movie in movie_list:
#	cast_list = GetCastIDs(movie)
#	print(movie)
#	print(cast_list)
#2240346 Kodi

