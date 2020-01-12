from mastodon import Mastodon

import variations

# Set up Mastodon
mastodon = Mastodon(
    access_token = 'token.secret',
    api_base_url = 'https://botsin.space'
)

# Generate with default parameters:
(filename,trace,counter) = variations.variation()

# Post to Mastodon
media  = mastodon.media_post("imgs/" + filename)
status = "Variation No. " + str(counter) + "\nTrace: " + trace
mastodon.status_post(status, media_ids=media)
