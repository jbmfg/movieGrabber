__author__ = 'GLXJBG0'
import urllib.request
import urllib.parse
import json
# example url http://nzbs.org/api?apikey=03afdd144efe61abca5275bab593720f&t=search&cat=2000&q=yellow
api_key = ''
sab_apikey = ''

def create_url():
    search_term = input('What movie are you looking for?\n')
    search_term = search_term.replace(" ", "%20")
    url = 'http://nzbs.org/api?apikey=' + api_key + '&o=json&t=search&cat=2000&q=' + search_term + '&maxage=1000'
    return url


def get_movies(url):
    r = urllib.request.urlopen(url)
    r = r.read().decode('utf-8')
    movies = json.loads(r)
    movie_dict = []
    for items in movies['channel']['item']:
        movie_dict.append({'Title': items['title'],
                           'category': items['category'],
                           'size': items['attr'][2]['@attributes']['value'],
                           'url': items['enclosure']['@attributes']['url']})
    return movie_dict


def send2sab(url, title):
    # mode=addurl&name=http://www.example.com/example.nzb&pp=3&script=customscript.cmd&cat=Example&priority=-1&nzbname=NiceName
    url = 'http://192.168.0.12:8080/sabnzbd/api?apikey=' + sab_apikey + '&mode=addurl&name=' + url + '&cat=movies&priority=-1&nzbname=' + title
    r = urllib.request.urlopen(url)
    r.read()


def main():
    movies = get_movies(create_url())
    for x, i in enumerate(movies):
        print(x, ' - ', i['Title'], i['category'], ' - ', str(round(int(i['size'])/1024000000, 2))+'Gb')
    selection = int(input('Which would you like to download?\n'))
    nzb = str(movies[selection]['url'])
    nzb = urllib.parse.quote_plus(nzb)
    send2sab(nzb, movies[selection]['Title'])

main()
