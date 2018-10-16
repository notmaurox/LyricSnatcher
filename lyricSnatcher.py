# import libraries
import urllib2
from bs4 import BeautifulSoup
import requests

artist_name = "Earl Sweatshirt"

dibbsurl = 'https://genius.com/Odd-future-oldie-lyrics'
uClient = requests.get(dibbsurl, verify=False)
data = uClient.content

f = open("GeniusHTTP.txt", "a")
f.write(data)
f.close()


# query the website and return the html to the variable page
page = data
# parse the html using beautiful soup and store in variable `soup`
soup = BeautifulSoup(page, 'html.parser')

pageText = soup.get_text()

print pageText

f = open("GeniusText.txt", "a")
f.write(pageText.encode('utf-8'))
f.close()

# for line in pageText:
#     print line
#     if artist_name in line:
#         print line




















