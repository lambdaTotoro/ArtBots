# Week 0: Beautiful Beginnings

The first not-quite-a-week of the new year introduces the first ArtBot.
This one was mostly to learn the ropes of hosting and mastodon bot maintenance.

Here's what it does:

- Loads the Wikipedia page with recent article additions.
- Picks a random article of those and regexes out the title.
- Choses random elements from precomposed lists of positive adjectives and synonyms for "beginning".
- Creates an image that is just large enough for the text:  
  "What a(n) \<adjective\> \<synonym\> for \<title\>!"
- Posts that text with that image to Mastodon.
