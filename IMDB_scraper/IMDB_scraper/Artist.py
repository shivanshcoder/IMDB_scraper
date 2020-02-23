
from IMDB_scraper import GetCastIDs, GetMovieList 

class Artist(object):
    """description of class"""

    #id if the form nmxxxxxxxx don't remove nm prefix of the ID
    def __init__(self, id):
        self.movies = GetMovieList(id)
        self.neighbour_actors = {}
        self.fillNeighbours()


    def fillNeighbours(self):
        
        for movie in self.movies:
            actors_list = GetCastIDs(movie)

            for actor in actors_list:
                if actor in self.neighbour_actors:

                    self.neighbour_actors[actor] += 1
                else:
                    self.neighbour_actors[actor] = 1
    
obj = Artist("nm6040987")

print(len(obj.neighbour_actors))
print(obj.neighbour_actors)



