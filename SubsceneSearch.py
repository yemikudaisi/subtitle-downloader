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

