import random
import re
import urllib.request

with open("beautiful.txt") as file1:
    with open("beginnings.txt") as file2:

        url = "https://en.wikipedia.org/w/index.php?title=Special:NewPages&offset=&limit=100&namespace=0&tagfilter=&username=&size-mode=min&size=&wpFormIdentifier=newpagesform&hidebots=1"
        newsites = urllib.request.urlopen(url)
        mybytes = newsites.read()
        site = mybytes.decode("utf8")
        newsites.close()
        
        regex = 'class=\"mw-newpages-pagename\" title=\"([^()<–>&%#;:]+)\">'
        articles = re.findall(regex,site)
        title = random.choice(articles)

        adjective = random.choice(file1.readlines()).strip()
        noun = random.choice(file2.readlines()).strip()

        print("What a", adjective, noun, "for", title + "!")
