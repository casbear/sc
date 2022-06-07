
from bs4 import BeautifulSoup
import requests
import re
import sqlite3
from sqlite3 import Error
import urllib.parse

#===============================================================================DATABASE SETUP

connection = sqlite3.connect('wikipedia.db')
cur = connection.cursor()

command1 = """CREATE TABLE IF NOT EXISTS
    article(Title TEXT, Link TEXT)"""

cur.execute(command1)

#===============================================================================SCRAPER

def getHTMLdocument(url):

    response = requests.get(url)

    return response.text

toScrape = "https://pl.wikipedia.org/wiki/Portal:Historia"
HTMLdocument = getHTMLdocument(toScrape)
soup = BeautifulSoup(HTMLdocument, 'html.parser')

connectQueue = []
titleList = []
i = 0

while len(connectQueue) <= 3000:

    for link in soup.find_all('a', attrs={'href': re.compile("^/wiki/")}):
    
        url = link.get('href')
        fullUrl = "https://pl.wikipedia.org" + url #getting full link to article
        connectQueue.append(fullUrl)


    connectQueue = list(set(connectQueue))

    soup = BeautifulSoup(getHTMLdocument(connectQueue[i]), 'html.parser')   

    print("-----------------------------------------------------------------------------------------\n\n\n",
         connectQueue[i],"\n pages jumped:", i ,"\n articles collected:", len(connectQueue) , 
          "\n\n\n-----------------------------------------------------------------------------------------\n", end="")
    

    i += 1

#================================================================================

for i in connectQueue:

        #taking title from encoded link
    encodedTitle = i
    decodedTitle = urllib.parse.unquote(encodedTitle)
    finishedTitle = decodedTitle.removeprefix("https://pl.wikipedia.org/wiki/")
    finishedTitle = finishedTitle.replace("_", " ")
    finishedTitle = finishedTitle.replace("'", " ")

        #inserting to database
    insert = "INSERT INTO article VALUES('" + str(finishedTitle) + "','" + str(i) + "')"
    cur.execute(insert)

    
connection.commit()
