import json
import unittest
import os
import requests

#
# Your name:
# Who you worked with:
#


# Make sure you create an API key at http://www.omdbapi.com/apikey.aspx
# Assign that to the variable API_KEY
API_KEY = ""

def read_cache(CACHE_FNAME):
    """
    This function reads from the JSON cache file and returns a dictionary from the cache data.
    If the file doesn't exist, it returns an empty dictionary.
    """
    try:
        cache_file = open(CACHE_FNAME, 'r', encoding="utf-8") # Try to read the data from the file
        cache_contents = cache_file.read()  # If it's there, get it into a string
        CACHE_DICTION = json.loads(cache_contents) # And then load it into a dictionary
        cache_file.close() # Close the file, we're good, we got the data in a dictionary.
        return CACHE_DICTION
    except:
        CACHE_DICTION = {}
        return CACHE_DICTION

def write_cache(CACHE_FNAME, CACHE_DICT):
    """
    This function encodes the cache dictionary (CACHE_DICT) into JSON format and
    writes the JSON to the cache file (CACHE_FNAME) to save the search results.
    """
    pass

def create_request_url(title):
    """
    This function prepares and returns the request url for the API call.

    The documentation of the API parameters is at http://www.omdbapi.com/

    Make sure you provide the following parameters besides the title when preparing the request url:
    1. type: one of movie, series, episode
    2. plot: set to short
    3. r: set to json

    Example of a request URL for movie title The Dark Knight:
    http://www.omdbapi.com/?apikey=xxxxxxxxxx&t=The Dark Knight&type=movie&plot=short&r=json

    The API key has been blurred out since one shouldn't share API keys publicly
    """
    pass

def get_data_with_caching(title, CACHE_FNAME):
    """
    This function uses the passed movie title to first generate a request_url (using the create_request_url function).
    It then checks if this url is in the dictionary returned by the function read_cache.
    If the request_url exists as a key in the dictionary, it should print "Using cache for <title>"
    and return the results for that request_url.

    If the request_url does not exist in the dictionary, the function should print "Fetching data for <title>"
    and make a call to the OMDB API to get the movie data.

    If data is found for the movie, it should add them to a dictionary (key is the request_url, and value is the results)
    and write out the dictionary to a file using write_cache.

    In certain cases, the OMDB API may return a response for the request_url
    but it may not contain any data for the movie: {"Response":"False","Error":"Movie not found!"}
    DO NOT WRITE THIS DATA TO THE CACHE FILE! Print "Movie Not Found" and return None

    If there was an exception during the search (for reasons such as no network connection, etc),
    it should print out "Exception" and return None.
    """
    pass

def top_ten_movies(rating_key, CACHE_FNAME):
    """
    The function calls read_cache() to get the movie data stored in the cache file.
    It analyzes the dictionary returned by read_cache() and sorts the movies in the dictionary
    on the basis of the rating key (either imdb or metacritic).
    It returns a list of tuples. The first item in each tuple is the movie title,
    and the second item is the value of the rating key.

    For example, if the key = imdbRating, the function will return top-ten movies ranked by their imdb rating.
    If the key = Metacritic, the function will return top-ten movies ranked by their metacritic score
    """
    pass

#######################################
############ EXTRA CREDIT #############
#######################################
def movie_list(genre, CACHE_FNAME):
    """
    The function calls read_cache() to get the movie data stored in the cache file.
    It analyzes the dictionary returned by read_cache() to identify all the movies that
    belong to the specified genre and returns a list of those movies.
    """
    pass

class TestHomework7(unittest.TestCase):
    def setUp(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.CACHE_FNAME = dir_path + '/' + "cache_movie.json"
        self.movie_list = ["The Dark Knight", "Rashomon", "The Seventh Seal", "Train to Busan", "Raging Bull", "Random character", "Once Upon a Time... in Hollywood","Joker", "1917", "Memento", "Spirited Away", "Finding Nemo", "Gandhi", "Lagaan"]
        self.API_KEY = API_KEY
        self.cache = read_cache(self.CACHE_FNAME)

    def test_write_cache(self):
        dict = read_cache(self.CACHE_FNAME)
        write_cache(self.CACHE_FNAME, self.cache)
        dict2 = read_cache(self.CACHE_FNAME)
        self.assertEqual(dict2, self.cache)

    def test_create_request_url(self):
        for m in self.movie_list:
            self.assertIn("apikey={}".format(self.API_KEY),create_request_url(m))
            self.assertIn("t={}".format(m),create_request_url(m))
            self.assertIn("type=movie",create_request_url(m))
            self.assertIn("plot=short",create_request_url(m))
            self.assertIn("r=json",create_request_url(m))

    def test_get_data_with_caching(self):
        for m in self.movie_list:
            dict_returned = get_data_with_caching(m, self.CACHE_FNAME)
            if dict_returned:
                self.assertEqual(type(dict_returned), type({}))
                self.assertIn(create_request_url(m),read_cache(self.CACHE_FNAME))
            else:
                self.assertIsNone(dict_returned)
        self.assertEqual(json.loads(requests.get(create_request_url(self.movie_list[0])).text),read_cache(self.CACHE_FNAME)[create_request_url(self.movie_list[0])])
        self.assertIsNone(get_data_with_caching(self.movie_list[5], self.CACHE_FNAME))
        self.assertNotIn(create_request_url(self.movie_list[5]), read_cache(self.CACHE_FNAME))

    def test_top_ten_movie(self):
        self.assertLessEqual(len(top_ten_movies("imdbRating",self.CACHE_FNAME)),10)
        self.assertLessEqual(top_ten_movies("imdbRating",self.CACHE_FNAME)[0][1],10)
        self.assertLessEqual(len(top_ten_movies("Metascore",self.CACHE_FNAME)),10)
        self.assertLessEqual(top_ten_movies("Metascore",self.CACHE_FNAME)[0][1],100)
        self.assertEqual(type(top_ten_movies("imdbRating",self.CACHE_FNAME)),type([]))
        self.assertEqual(type(top_ten_movies("Metascore",self.CACHE_FNAME)),type([]))
        self.assertEqual(type(top_ten_movies("Metascore",self.CACHE_FNAME)[0][1]),type(0.0))

    ######## EXTRA CREDIT #########
    # Keep this commented out if you do not attempt the extra credit
    # def test_movie_list(self):
    #     self.assertEqual(type(movie_list("Comedy",self.CACHE_FNAME)), type([]))
    #     self.assertIn("The Dark Knight", movie_list("Thriller",self.CACHE_FNAME))
    #     self.assertIn("The Dark Knight", movie_list("Action",self.CACHE_FNAME))
    #     self.assertIn("Train to Busan", movie_list("Horror",self.CACHE_FNAME))
    #     self.assertIn("Rashomon", movie_list("Mystery",self.CACHE_FNAME))

def main():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    CACHE_FNAME = dir_path + '/' + "cache_movie.json"

    # You can add new movies, change the movies here for testing!

    # Fetch the data for Inception.
    # The data should be requested from the API if this is the first time you are running the program
    # or if you haven't deleted the cache!
    data1 = get_data_with_caching('Inception', CACHE_FNAME)
    data2 = get_data_with_caching('Inception', CACHE_FNAME)
    print("________________________")

    # Getting the data for Parasite
    # The data should be requested from the API if this is the first time you are running the program
    # or if you haven't deleted the cache!
    data1 = get_data_with_caching('Parasite', CACHE_FNAME)
    data2 = get_data_with_caching('Parasite', CACHE_FNAME)
    print("________________________")

    # Getting the data for Ladybird
    # The data should be requested from the API if this is the first time you are running the program
    # or if you haven't deleted the cache!
    data1 = get_data_with_caching('Ladybird', CACHE_FNAME)
    data2 = get_data_with_caching('Ladybird', CACHE_FNAME)
    print("________________________")

    print("Top 10 movies in the cache by imdb rating")
    print(top_ten_movies("imdbRating",CACHE_FNAME))
    print("________________________")

    print("Top 10 movies in the cache by metacritic score")
    print(top_ten_movies("Metascore",CACHE_FNAME))
    print("________________________")

    # Extra Credit
    # Keep the statements commented out if you do not attempt the extra credit
    print("Thriller movies in the cache:")
    print(movie_list("Thriller",CACHE_FNAME))
    print("________________________")

    print("Action movies in the cache:")
    print(movie_list("Action",CACHE_FNAME))
    print("________________________")

if __name__ == "__main__":
    main()
    # You can comment this out to test with just the main function,
    # But be sure to uncomment it and test you pass the unittests before you submit!
    unittest.main(verbosity=2)
