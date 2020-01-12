# Week 1: Variations on Variations

This is the ArtBot for the first full week of 2020. It creates images
that are inspired by the series "Variations" of the 

In particular, this picture:

![Variations, Max Bill](https://www.markanto.de/media/image/38/c8/e4/max-bill-variation1-4113_0_600x600.jpg)

The program picks a number n between 5 and 8 and calculates the
coordinates of an n-gon. Then, those of an (n-1)-gon that shares
a (random) side with the n-gon, and so on, all the way down to the
triangle. The n-gon is also rotated by a random angle and all polygons
are filled with a single colour that is randomly chosen from a list of
colours I deemed workable in this context.

In this current version "2.0" of this bot, it also generates a "trace"
of the image, detailing which dimensions and which random numbers were
used in the creation process, so you can mention the Mastodon bot with 
a valid trace if you like a picture but would like it just a bit
differetly.
