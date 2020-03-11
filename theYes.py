from bs4 import BeautifulSoup
from collections import defaultdict
import argparse
import lxml #for speed
import urllib.request
import re
import sys

data_dict = defaultdict(list)

def crawler(url):
    """ Takes in the url of a page containing 50 movies (1 to 50, 51 to 100, ... 951 to 100)
        from the list of top 1000 movies on IMDB then feeds the data movie by movie into
        the data_extractor function where relevant data is extracted for storage
    """
    current_page = urllib.request.urlopen(url)

    page_soup = BeautifulSoup(current_page, "lxml")
    movies = page_soup.find_all('div', class_ = 'lister-item mode-advanced')

    for movie in movies:
        data_extractor(movie)



def data_extractor(movie):
    """ Extracts relevant data for each movie using CSS selectors and adds it
        in tuple format (keyword, title) to the list movie_data.
        Ex:
            For the movie titled "Saving Private Ryan" (1998) directed by Steven Spielberg
            and starring Tom Hanks - appends ("saving", "Saving Private Ryan"),
            ("private", "Saving Private Ryan"), ("ryan", "Saving Private Ryan"), ("1998", "Saving Private Ryan"),
            ("steven", "Saving Private Ryan"), ("spielberg", "Saving Private Ryan"), ("tom", "Saving Private Ryan"),
            ("hanks", "Saving Private Ryan"), etc. to the list movie_data.
    """
    movie_data = []

    title = movie.h3.a.text
    for word in title.split():
        movie_data.append((word.lower(), title))

    ranking = movie.h3.span.text[:-1]
    movie_data.append((ranking, title))

    year = movie.find("span", {"class": "lister-item-year text-muted unbold"}).text[1:-1]
    movie_data.append((year, title))

    certificate_rating = movie.find("span", {"class": "certificate"})
    if certificate_rating:
        movie_data.append((certificate_rating.text.lower(), title))

    user_rating = movie.find("meta", {"itemprop": "ratingValue"})["content"]
    movie_data.append((user_rating, title))

    genre_list = movie.find("span", {"class": "genre"}).text.strip().split(", ")
    for genre in genre_list:
        movie_data.append((genre.lower(), title))

    metascore = movie.find("span", {"class": "metascore favorable"})
    if metascore:
        movie_data.append((metascore.text.strip(), title))

    people_list = [person.text for person in movie.find("p", {"class": ""}).findAll("a")]
    for person in people_list:
        name_split = person.lower().split()
        for partial_name in name_split:
            movie_data.append((partial_name, title))

    store_data(movie_data)

def store_data(movie_data):
    """ Receives a list of tuples (movie_data) in the format (keyword, title) and
        adds the data accordingly to the matching key in defaultdict (data_dict).
        Ex:
            movie_data = [("steven", "Saving Private Ryan"), ("spielberg", "Saving Private Ryan")]
        --> data_dict = {"steven": ["Saving Private Ryan"], "spielberg": ["Saving Private Ryan"]}

        Then, when another movie's data is passed in containing a Steven Spielberg
        movie such as Schindler's List, the data_dict is updated as such:

            movie_data = [("steven", "Schindler's List"), ("spielberg", "Schindler's List")]
        --> data_dict = {"steven": ["Saving Private Ryan", "Schindler's List"],
                            "spielberg": ["Saving Private Ryan", "Schindler's List"]}

        And so on until the keys "steven" and "spielberg" contain the list of all
        Steven Spielberg movies.
    """
    for k, v in movie_data:
        data_dict[k].append(v)

def query(to_query):
    """ Takes in the input string of items to query by, converts them to a list of keywords
        then returns values from the data_dict only if they are contained in all the keywords.

        Ex:
            keywords = "hanks spielberg 1998" will return only ["Saving Private Ryan"],
        but keywords = "hanks spielberg 1874" will return an empty list.
    """
    # print("Size of dict in bytes:")
    # print(sys.getsizeof(data_dict))
    word_list = to_query.lower().split()
    result_list = []
    for word in word_list:
        if not result_list:
            result_list = data_dict[word]
        else:
            result_list = [x for x in result_list if x in data_dict[word]]
    return result_list

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("keywords", type=str, help="Enter any combination (must enter at least 1) of the following separated by spaces: cast members, directors, genres, release year, metascore (0 to 100), user rating (0.0 to 10.0), certificate rating (R, PG-13, etc.), and/or rank (1 to 1000)", nargs = "+")

    args = parser.parse_args()

    to_query = " ".join(args.keywords)

    print("Please wait while we retrieve the data from IMDB...")
    start = 1
    while start <= 951:
        print("Retrieving movies %d to %d..." % (start, start + 49))
        crawler("https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&start={}&ref_=adv_prv".format(start))
        start += 50
    print("Done!")

    result = query(to_query)
    print(result)
