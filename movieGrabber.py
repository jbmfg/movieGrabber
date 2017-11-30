#!/usr/bin/env python3.5

import requests, json
import urllib.parse

def getConfigs():
    with open("/home/jbg/.scripts/movieGrabberConfig.json", "r") as f:
        params = json.load(f)
    f.close()
    return params


def nzbsSearch(movie, apiKey):
    url = 'http://nzbs.org/api?apikey=' + apiKey + '&o=json&t=search&cat=2000&q=' + movie + '&maxage=1000'
    url = url.replace(" ", "%20")
    headers = {"User-Agent":"python requests"}
    results = requests.get(url, headers=headers)
    return results.json()

def send2sab(url, movie, sab_key, sab_addr):
    sendUrl = "http://{0:s}:8080/sabnzbd/api?apikey={1:s}&mode=addurl&name={2:s}&cat=movies&priority=-1&nzbname={3:s}"\
            .format(sab_addr, sab_key, urllib.parse.quote_plus(url), movie)
    return requests.get(sendUrl)

def interface():
    params = getConfigs()
    movie = input("What movie are you looking for?\n")
    results = nzbsSearch(movie, params["api"])
    availMovies = [[i["title"], i["link"], int(i["enclosure"]["@attributes"]["length"])] for i in results["channel"]["item"]]
    # str(round(int(i['size'])/1024000000, 2))+'Gb')
    for x,i in enumerate(availMovies):
        print ("{0:d} - {1:s} - {2:s}".format(x, i[0], str(round(i[2]/1024000000, 2))))
    movieNo = int(input("Which would you like to download?\n"))
    return send2sab(availMovies[movieNo][1], availMovies[movieNo][0], params["sab_key"], params["sab_address"])
	
interface()
