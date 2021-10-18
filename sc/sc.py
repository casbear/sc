
from bs4 import BeautifulSoup
import requests
import re

import time

def getHTMLdocument(url):

    response = requests.get(url)

    return response.text

toScrape = "https://pl.wikipedia.org/wiki/Portal:Historia"

HTMLdocument = getHTMLdocument(toScrape)

soup = BeautifulSoup(HTMLdocument, 'html.parser')

connectQueue = []

i = 0
while connectQueue != 0:



    for link in soup.find_all('a', attrs={'href': re.compile("^/wiki/")}):

        fullUrl = "https://pl.wikipedia.org" + link.get('href')
        connectQueue.append(fullUrl)
        print(fullUrl)
        connectQueue = list(set(connectQueue))


    print("-----------------------------------------------------\n\n\n", connectQueue[i],"\n pages jumped:", i ,"\n articles collected:", len(connectQueue) ,"\n\n\n-----------------------------------------------------", end="")

    connectQueue = list(set(connectQueue))
    soup = BeautifulSoup(getHTMLdocument(connectQueue[i]), 'html.parser')

    i += 1

