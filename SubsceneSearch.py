import urllib
import bs4
import requests
from movie import Movie
from subtitle import Subtitle
from download_manager import download_file

def search_movie(url_name):
    
    url = 'https://subscene.com/subtitles/title?q='+url_name
    response = requests.get(url)
    response.raise_for_status()
    soup = bs4.BeautifulSoup(response.text,"html.parser")
    del response
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
def search_movie_subtitle(movie, language):
    url = 'https://subscene.com/subtitles/'+movie.slug()+'/'+language
    response = requests.get(url)
    response.raise_for_status()
    soup = bs4.BeautifulSoup(response.text,"html.parser")
    del response
    subtitles = []
    selection =soup.findAll('td', attrs={'class':'a1'})
    for td in selection:
        title = str(td.findAll('span', attrs={'class': None})[0].contents[0]).encode('utf-8').strip()
        url = str(td.find('a')['href']).strip()
        lang = str(td.find('span').contents[0]).encode('utf-8').strip()
        temp = Subtitle(title,url, lang)
        subtitles.append(temp)
    return subtitles

def download_movie_subtitle(subtitle, download_path):
    response = requests.get('https://subscene.com/'+subtitle.link)
    soup = bs4.BeautifulSoup(response.text,'html.parser')
    del response
    selection = soup.findAll('div', attrs={'class' : 'download'})
    for div in selection:
        # TODO Check for errors
        url = "http://subscene.com"+div.find('a')['href']
        print(url)
        download_file(url, download_path[0]+".zip")

    print("complete: "+str(len(selection))+" downloaded")

    

