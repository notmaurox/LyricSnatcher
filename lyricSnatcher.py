# import libraries
import urllib2
from bs4 import BeautifulSoup
import requests
import ast

artist_name = "Earl Sweatshirt"

dibbsurl = 'https://genius.com/Earl-sweatshirt-sunday-lyrics'
uClient = requests.get(dibbsurl, verify=False)
data = uClient.content

# query the website and return the html to the variable page
page = data
# parse the html using beautiful soup and store in variable `soup`
soup = BeautifulSoup(page, 'html.parser')

pageText = soup.get_text()


songInfoDict = {}
dictFilled = False
foundLyrics = False
inVerse = False
lyricLines = -1

for item in pageText.split("\n"):
    if lyricLines >= 0:
        lyricLines+=1
    if "var TRACKING_DATA" in item:
        data = item.split(" = ")[1].replace("};","}")
        evalReady = data.replace("\"","").replace("}","").replace("{","")
        evalReadyArr = evalReady.split(",") 
        for element in evalReadyArr:
            elementItems = element.split(":")
            songInfoDict[elementItems[0]] = elementItems[1]
        dictFilled = True
        lyricStartKey = songInfoDict["Title"]+" Lyrics"
    if foundLyrics == True and "More on Genius" in item:
        foundLyrics = False
    if dictFilled == True and lyricStartKey in item and lyricLines == -1:
            foundLyrics = True
            lyricLines+=1
            
            outFileName = songInfoDict["Primary Artist"].replace(" ","_")+"_"+songInfoDict["Title"].replace(" ","_")+"_"+"Lyrics.txt"
            f = open(outFileName, "w")
            f.write(songInfoDict["Primary Artist"].encode('utf-8') + "\n")
            f.write(songInfoDict["Primary Album"].encode('utf-8') + "\n")
            f.write(songInfoDict["Title"].encode('utf-8') + "\n")
            f.write("xxxxx" + "\n")
    elif foundLyrics == True:
        if "[" in item:
            itemSplit = item.split(": ")
            if len(itemSplit) > 1:
                if artist_name in itemSplit[1]:
                    inVerse = True
            elif artist_name == songInfoDict["Primary Artist"]:
                inVerse = True
        elif item == "":
            inVerse = False
        if inVerse == True:
            f.write(item.encode('utf-8')+"\n")

f.close()    





















