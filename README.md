# IMDB's Top 1000 Movies Query API

This API will crawl and index movie data from IMDB's top 1000 movies. Data it'll extract for every movie: movie title, directors, stars, genres, year of release, user rating (0.0 to 10.0), certificate rating (PG-13, PG, R, etc.), metascore (0 to 100), and IMDB rank (1 to 1000).

It'll then allow you to search for movies using any combination of the aforementioned data.

## Simplifying Assumptions

* Instead of crawling every movie page separately and extracting the relevant data from there, this API instead collects all its data from the detailed view page (which contains 50 movies). While this disables us from getting all the data points such as writers, the full credits (we are limited to only the directors and the top 4 cast members), companies, awards received, nominations, exact release date (we are limited to the release year), movie budget, soundtracks - it reduces the number of pages to crawl, and consequently the number of HTTP requests 50 fold, from 1000 (one request per movie) to 20 (one request per 50 movies). However, the data we are able to collect is beyond adequate as most users will want to query by directors, stars, and genres - and this API supports queries for data points much beyond just that. The mere increase in crawl speed resulting from the 50x reduction in the # of HTTP requests makes this sacrifice well worth it.

## Improvements

### Software Architecture

* Cache the Crawl: Since I was under a time constraint of 3 hours, I did not have time to structure this API so that it builds the database only for the first query and to query from a cached database for the subsequent queries. Therefore, the API has to re-crawl the webpages and rebuild the database every time a new query is submitted. Although I structured the crawling process to be very efficient, implementing a cached database would be the first and most obvious improvement to add onto this API.

* Orient the Objects: Could have created a separate class for crawler, web pages, movies - the modularity would allowed for easier troubleshooting and inheritance would have allowed for easier reuse of code. However, for the purposes of this coding exercise - I deemed this as not necessary.

### Scale

* Because I only had to crawl and index data for the top 1000 movies, I did not worry about memory scale. However, this API will perform well even if it had to store data for all 6.5 million movies on IMDB.
```
$ sys.getsizeof(data_dict)
295024
```
That is the # of bytes our data_dict takes up. Multiplying this number by 6,500 to scale for IMDB's entire movie database, we get 1917656000 bytes, which equates to 1.786 Gb. This isn't too bad, and most computers should be able to handle an in-memory data structure of this size. 32-bit computes have a theoretical RAM limit of 4 Gb, while 64-bit computers have a theoretical RAM limit of 16 Eb.

### Performance

* Apart from the fact that we rebuild the data_dict for every query, the lookup time couldn't be much faster than it is. As you'll see, the queries are nearly instant! I was able to achieve this due to the defaultdict implementation, where lookups are O(1) - so no matter how many terms there are in the query, the API will always return your movies with 100% accuracy and super sonic speed.

### Quality

* This API works with 100% accuracy and lookup time is super fast. Only issue is the lack of caching. If that issue is addressed, I can't think of any other improvements to the quality as it already performs very well.

## Getting Started

In order to use this API on your own machine, follow these steps:

### Prerequisites

You will need to install the packages in the requirements.txt file. To do so, run:

```
$ pip3 install -r requirements.txt
```

### Usage

After downloading the requirements, you use the API as such:

For all Tom Hanks and Steven Spielberg movies:
```
$ python3 theYes.py hanks spielberg
['Saving Private Ryan', 'Catch Me If You Can', 'Bridge of Spies']
```
For Hanks and Spielberg movies that are rated PG-13:
```
$ python3 theYes.py hanks spielberg PG-13
['Catch Me If You Can', 'Bridge of Spies']
```
For all movies released in 2008:
```
$ python3 theYes.py 2008
['The Dark Knight', 'WALL·E', 'A Wednesday', 'Gran Torino', 'Departures', 'Ip Man', 'Slumdog Millionaire', 'The Chaser', 'Let the Right One In', 'The Wrestler', 'In Bruges', 'Iron Man', 'The Boy in the Striped Pajamas', 'The Curious Case of Benjamin Button', 'Ponyo', 'Frost/Nixon', 'Changeling', 'The Wave', 'The Reader', 'The Hurt Locker', 'Seven Pounds', 'Synecdoche, New York', 'Kung Fu Panda']
```
For all movies rated 9.3:
```
$ python3 theYes.py 9.3
['The Shawshank Redemption']
```
For all movies that combine the genres biography, drama, and history:
```
$ python3 theYes.py biography drama history
["Schindler's List", 'Ayla: The Daughter of War', 'Braveheart', 'Amadeus', 'Downfall', 'The Message', 'Andrei Rublev', 'Hacksaw Ridge', '12 Years a Slave', 'Hotel Rwanda', 'Inherit the Wind', 'The Passion of Joan of Arc', "The King's Speech", 'Cinderella Man', 'Gandhi', "All the President's Men", 'Straight Outta Compton', 'The Lion in Winter', 'Hidden Figures', 'Glory', 'The Killing Fields', 'Frost/Nixon', 'The Last King of Scotland', 'Malcolm X', 'The Last Emperor', 'A Man for All Seasons']
```


## Built With

* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - Extracting Info from Web Pages using CSS Selectors
* [lxml](https://lxml.de/) - HTML Parser that is much faster than Python's builtin parser

## Authors

* **Mohammed Abu-Sharkh**

## License

This project is to be used/altered freely by anyone!

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
