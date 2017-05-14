import bs4
import requests
from movie import Movie

def search_movie_subtitle(url_name):
    
    url = 'https://subscene.com/subtitles/title?q='+url_name
    result = requests.get(url)
    result.raise_for_status()
    soup = bs4.BeautifulSoup(result.text,"html.parser")

    movies = []
    for div in soup.findAll('div', attrs={'class':'title'}):
        temp = Movie(div.find('a').contents[0],div.find('a')['href'])
        movies.append(temp)
    return movies

"""
find subtitle for a movie base on assigned language
At the this point it is expected that the language will have been assigned
if language has not been set the movie class will return english (which is the default)
"""
def search_subtitle_language(movie):
    url = 'https://subscene.com/subtitles/'+movie.slug()+'/'+movie.language
    result = requests.get(url)
    result.raise_for_status()
    soup = bs4.BeautifulSoup(result.text,"html.parser")
    movies = []
    for div in soup.findAll('div', attrs={'class':'title'}):
        temp = Movie(div.find('a').contents[0],div.find('a')['href'])
        movies.append(temp)
    return movies

