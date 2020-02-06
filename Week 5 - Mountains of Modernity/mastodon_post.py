import os

from mastodon import Mastodon

import mountains_of_modernity

# Set up Mastodon
mastodon = Mastodon(
    access_token = 'token.secret',
    api_base_url = 'https://botsin.space'
)

fn = None
mrange = mountains_of_modernity.mountain_range()

fn = mrange[0]
counter = mrange[1]
	
if os.path.isfile("./imgs/" + fn):
	media = mastodon.media_post("./imgs/" + fn)
	mastodon.status_post(f"({counter}) Here are some more mountains!", media_ids=media)
