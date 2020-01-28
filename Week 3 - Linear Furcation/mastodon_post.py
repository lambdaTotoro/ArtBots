import datetime
import random
import os 
import sys

from mastodon import Mastodon

import linear_furcation

# Set up Mastodon
mastodon = Mastodon(
    access_token = 'token.secret',
    api_base_url = 'https://botsin.space'
)

fn = None
fn = regular_perspectives.approximate()

b1 = "A new linear furcation has arrived:"
b2 = "I approximated this for y'all:"
b3 = "Time for some new content!"
b4 = "New image, new art!"
b5 = "My algorithms have produced this here art:"

blurbs = [b1,b2,b3,b4,b5]
	
if (os.path.isfile("./imgs/" + fn))
	
	media = mastodon.media_post("./imgs/" + fn)
	mastodon.status_post(random.choice(blurbs), media_ids=media)
