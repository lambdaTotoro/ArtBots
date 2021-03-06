import datetime
import random
import os 
import sys

from mastodon import Mastodon

import regular_perspectives

# Set up Mastodon
mastodon = Mastodon(
    access_token = 'token.secret',
    api_base_url = 'https://botsin.space'
)

assert(len(sys.argv) == 2)
today = str(datetime.date.today())

if sys.argv[1] == "generate":
	regular_perspectives.approximate()
	
elif sys.argv[1] == "post":
	filename = None
	while (filename is None) or (filename == "target.png") or (filename == "approximation.png"):
		files = os.listdir("./days/" + today)
		filename =  random.choice(files)
	
	media = mastodon.media_post("./days/" + today + "/" + filename)
	mastodon.status_post("Here is a new perspective!", media_ids=media)
	os.remove("./days/" + today + "/" + filename)
	
elif sys.argv[1] == "resolve":
	# Post to Mastodon
	media1  = mastodon.media_post("./days/" + today + "/target.png")
	media2  = mastodon.media_post("./days/" + today + "/approximation.png")
	status1 = "All images today where based on this picture (left).\n"
	status2 = "The 'best' approximation was this (right)."
	mastodon.status_post(status1 + status2, media_ids=[media1,media2])
else:
	print("[Error] Unknown argument:", sys.argv[1])
