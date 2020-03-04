import os

from mastodon import Mastodon

import walks_of_life

# Set up Mastodon
mastodon = Mastodon(
    access_token = 'token.secret',
    api_base_url = 'https://botsin.space'
)

fn = None
mrange = walks_of_life.new_walk()

fn = mrange[0]
counter = mrange[1]
	
if os.path.isfile("./imgs/" + fn):
	media = mastodon.media_post("./imgs/" + fn)
	mastodon.status_post(f"({counter}) It's a new life, it's a new walk!", media_ids=media)
