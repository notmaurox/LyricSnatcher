# import libraries
import urllib2
from bs4 import BeautifulSoup
import requests
import ast

artist_name = "Earl Sweatshirt"

dibbsurl = 'https://genius.com/Earl-sweatshirt-sunday-lyrics'
uClient = requests.get(dibbsurl, verify=False)
data = uClient.content

f = open("GeniusHTTP2.txt", "a")
f.write(data)
f.close()


# query the website and return the html to the variable page
page = data
# parse the html using beautiful soup and store in variable `soup`
soup = BeautifulSoup(page, 'html.parser')

pageText = soup.get_text()

print pageText

songInfoDict = {}

for item in pageText.split("\n"):
    if "var TRACKING_DATA" in item:
        data = item.split(" = ")[1].replace("};","}")
        evalReady = data.replace("\"","").replace("}","").replace("{","")
        evalReadyArr = evalReady.split(",") 
        print evalReady
        for element in evalReadyArr:
            elementItems = element.split(":")
            songInfoDict[elementItems[0]] = elementItems[1]
print "XXX"
print songInfoDict["Title"]
print "XXX"


f = open("GeniusText2.txt", "a")
f.write(pageText.encode('utf-8'))
f.close()

# for line in pageText:
#     print line
#     if artist_name in line:
#         print line




















