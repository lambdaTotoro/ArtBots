from mastodon import Mastodon

import re
import variations

# Set up Mastodon
mastodon = Mastodon(
    access_token = 'token.secret',
    api_base_url = 'https://botsin.space'
)

# Fetch all notifications, only deal with mentions.
notifs   = mastodon.notifications()
mentions = list(filter(lambda n: n["type"] == "mention", notifs))

for notification in mentions:
	not_id = notification["id"]
  origin = notification["account"]
	talker = notification["account"]["acct"]
  toot   = notification["status"]["content"]
	replid = notification["status"]["id"]
	tr     = re.findall("Trace: (\d-(?:\d{1,3})-(?:\d-)+\d*)", toot)

	tr_exists = False
	if len(tr) >= 1:
		tr_exists = True

	# Generate appropriate reply image!
	if tr_exists:
		exit  = variations.variation_by_trace(tr[0])
		valid = exit is not None

		if valid:
			filename = exit[0]
			trace    = exit[1]
			counter  = exit[2]

	# Post reply to Mastodon
	if tr_exists:
		if valid:
			media  = mastodon.media_post("imgs/" + filename)
			status = "Here you go, " + talker + "!\nVariation No. " + str(counter) + "\nTrace: " + trace
			mastodon.status_post(status, media_ids=media, in_reply_to_id=replid)
		else:
			status = "Sorry, I can't see a valid trace in your toot!"
			mastodon.status_post(status, in_reply_to_id=replid)
	else:
		status = "Sorry, I don't know how to reply to that!"
		mastodon.status_post(status, in_reply_to_id=replid)
