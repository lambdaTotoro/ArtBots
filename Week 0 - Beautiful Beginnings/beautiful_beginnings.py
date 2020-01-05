from mastodon import Mastodon
from PIL import Image, ImageDraw, ImageFont

import os
import random
import re
import time
import urllib.request

# Set up Mastodon
mastodon = Mastodon(
    access_token = 'token.secret',
    api_base_url = 'https://botsin.space'
)

with open("beautiful.txt") as file1:
    with open("beginnings.txt") as file2:

        # Find random new Wikipedia article title

        url = "https://en.wikipedia.org/w/index.php?title=Special:NewPages&offset=&limit=100&namespace=0&tagfilter=&username=&size-mode=min&size=&wpFormIdentifier=newpagesform&hidebots=1"
        newsites = urllib.request.urlopen(url)
        mybytes = newsites.read()
        site = mybytes.decode("utf8")
        newsites.close()
        
        regex = 'class=\"mw-newpages-pagename\" title=\"([^()<–>&%#;:]+)\">'
        articles = re.findall(regex,site)
        title = random.choice(articles)

        # Find random adjective and noun from list

        adjective = random.choice(file1.readlines()).strip()
        noun = random.choice(file2.readlines()).strip()

        # Create Text

        article = "a "
        if (adjective[0] in "aeiou") or (adjective in ["honest"]):
            article = "an "

        text1 = "What " + article + adjective
        text2 = noun + " for"
        text3 = title + "!"

        text = text1 + "\n" + text2 + "\n" + text3

        # Create Image

        icolour = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        time.sleep(1.337)
        tcolour = (random.randint(0,255), random.randint(0,255), random.randint(0,255))

        if not os.path.exists('imgs'):
            os.makedirs('imgs')
        counter = len(os.listdir("imgs"))
        filename = str(counter) + ".png"

        size = 1
        fnt = ImageFont.truetype("NimbusMonoPS-Regular.otf", size)
        while max(fnt.getsize(text1)[0],fnt.getsize(text2)[0],fnt.getsize(text3)[0]) < 480:
            size += 1
            fnt = ImageFont.truetype("NimbusMonoPS-Regular.otf", size)

        size -= 1
        fnt = ImageFont.truetype("NimbusMonoPS-Regular.otf", size)

        dummy = Image.new(mode = "RGB", size = (500,500))
        ddraw = ImageDraw.Draw(dummy)
        (w,h) = ddraw.textsize(text, font = fnt)
        
        image = Image.new(mode = "RGB", size = (500,h + 25), color = icolour)
        draw = ImageDraw.Draw(image)
        draw.text((10,10), text, font = fnt, fill = tcolour)
        image.save("imgs/" + filename)

        # Post to Mastodon
        media = mastodon.media_post("imgs/" + filename)
        status = "(" + counter + ") " + text1 + " " + text2 + " " + text3
        mastodon.status_post(status, media_ids=media)
