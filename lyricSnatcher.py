# import libraries
import urllib2
from bs4 import BeautifulSoup
import requests
import ast
import sys
import os
import re

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

with open(sys.argv[1],"r") as inFile:
    
    artist_name = inFile.readline().replace("\n","")
    dirName = artist_name.replace(" ","_") + "_Songs"
    
    if not os.path.exists(dirName):
        os.mkdir(dirName)
    else:
        os.chdir(dirName)  
    
    line = inFile.readline().strip()

    while line:
        
        print "Downloading lyrics from: " + line
        
        uClient = requests.get(line, verify=False)
        data = uClient.content

        # query the website and return the html to the variable page
        page = data
        # parse the html using beautiful soup and store in variable `soup`
        soup = BeautifulSoup(page, 'html.parser')

        pageText = soup.get_text()
        
        # print pageText.encode('utf-8')

        songInfoDict = {}
        dictFilled = False
        foundLyrics = False
        inVerse = False
        lyricLines = -1
        fileHeader = ""
        fileBody = ""
        bodyLength = 0

        for item in pageText.split("\n"):
            if lyricLines >= 0:
                lyricLines+=1
            if "var TRACKING_DATA" in item:
                data = item.split(" = ")[1].replace("};","}")
                evalReady = data.replace("}","").replace("{","")
                evalReady = re.sub("[^\"],\"","\",\"",evalReady) #need split without breaking artists or 
                evalReadyArr = evalReady.split("\",\"") 
                for element in evalReadyArr:
                    elementClean = element.replace("\"","")
                    elementItems = elementClean.split(":")
                    songInfoDict[elementItems[0]] = elementItems[1]
                dictFilled = True
                lyricStartKey = songInfoDict["Title"]+" Lyrics"
            if foundLyrics == True and "More on Genius" in item:
                foundLyrics = False
            if dictFilled == True and lyricStartKey in item and lyricLines == -1:
                    foundLyrics = True
                    lyricLines+=1
                    
                    outFileName = songInfoDict["Primary Artist"].replace(" ","_")+"_"+songInfoDict["Title"].replace(" ","_")+"_"+"Lyrics.txt"
                    outFileName = outFileName.replace("<","_lessThan_").replace(">","_greaterThan_").replace(":","_colon_").replace("\"","_dubQuote_").replace("/","_fwdSlash_").replace("|","_bar_").replace("?","_questionMrk_").replace("*","_star_")
                    f = open(outFileName, "w")
                    fileHeader+= songInfoDict["Primary Artist"]+ "\n"
                    fileHeader+= songInfoDict["Primary Album"] + "\n"
                    fileHeader+= songInfoDict["Title"] + "\n"
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
                    fileBody = fileBody + item + "\n"
                    if "[" not in item:
                        bodyLength += 1
        fileHeader+= str(bodyLength) + "\n"
        fileHeader+="xxxxx" + "\n"
        f.write(fileHeader.encode('utf-8'))
        f.write(fileBody.encode('utf-8'))
        f.close()
        line = inFile.readline().strip()   





















