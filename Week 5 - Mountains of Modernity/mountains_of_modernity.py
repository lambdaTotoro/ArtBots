import math
import os
import random

import numpy as np

from PIL import Image, ImageDraw
from skimage.color import rgb2gray

# Standard euclidean distance between two points on the plane.
def distance(p1,p2):
	return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def calculate_equilateral_triangle(p1,p2):
	
	dist = distance(p1,p2)
	hght = math.sqrt((dist ** 2) - ((0.5 * dist) ** 2))
	
	# For now (?), all triangles have the same baseline.
	assert(p1[1] == p2[1])
	assert(p1[0] != p2[0])
	
	if p1[0] < p2[0]:
		p3 = (round(p1[0] + (0.5 * dist)), round(p1[1] - hght))
	else:
		p3 = (round(p2[0] + (0.5 * dist)), round(p2[1] - hght))
	
	return [p1,p2,p3]
	
def luminance(rgb):
    return (.299 * rgb[0]) + (.587 * rgb[1]) + (.114 * rgb[2])
	
def contrast(rgb1, rgb2):
	
	l1 = luminance(rgb1)
	l2 = luminance(rgb2)
	
	if l1 > l2:
		return ((l1 + 0.05) / (l2 + 0.05))
	else:
		return ((l2 + 0.05) / (l1 + 0.05))	

def subsumes(m1,m2):
	
	l1 = m1[0][0] if m1[0][0] < m1[0][1] else m1[0][1]
	r1 = m1[0][0] if m1[0][0] > m1[0][1] else m1[0][1]
	
	l2 = m2[0][0] if m2[0][0] < m2[0][1] else m2[0][1]
	r2 = m2[0][0] if m2[0][0] > m2[0][1] else m2[0][1]
	
	return (l1 < l2) and (r1 > r2)
	
def random_colour():
	
	r = random.randint(20,150)
	g = random.randint(20,150)
	b = random.randint(20,150)
	
	return (r,g,b)
	
def new_colour(used = None):
	
	if used == None:
		return random_colour()
	else:
		good_contrast = False
		threshold = 1.25
		rc = random_colour()
		
		steps = 10000
		
		# Look for a good contrast, but don't wait forever
		while (not good_contrast) and (steps > 0):
			
			rc = random_colour()
			steps -= 1
			good_contrast = True
			
			for colour in used:
				cont = contrast(colour,rc)
				if cont < threshold:
					good_contrast = False
					break
		
		return rc
	
def mountain_range(sz = 1200, n = None):
	
	bg    = new_colour()
	image = Image.new(mode = "RGB", size = (sz,sz), color = bg)
	draw  = ImageDraw.Draw(image)
	
	n = random.randint(3, 7) if n is None else n
	
	used = [bg]
	xs   = []
	mountains = []
	
	for _ in range(0,n):
		
		y = round(5/6 * sz)
		
		x1 = random.randint(round(1/6 * sz), round(5/6 * sz))
		good_x = False
		
		while not good_x:
			x1 = random.randint(round(1/6 * sz), round(5/6 * sz))
			good_x = True
			
			for u in xs:
				a = abs(x1 - u)
				if (a > 0) and (a < 100):
					good_x = False
					break 
		
		xs.append(x1)
		
		x2 = random.randint(round(1/6 * sz), round(5/6 * sz))
		good_x = False
		
		while (not good_x) or (x1 == x2):
			x2 = random.randint(round(1/6 * sz), round(5/6 * sz))
			good_x = True
			
			for u in xs:
				a = abs(x2 - u)
				if (a > 0) and (a < 100):
					good_x = False
					break
		
		xs.append(x2)
		
		mountains.append(calculate_equilateral_triangle((x1,y),(x2,y)))
	
	for _ in range(0,2*len(mountains)):
		for ind1, mountain in enumerate(mountains):
			for m in mountains[ind1:]:
				if subsumes(m,mountain):
					ind2 = mountains.index(m)
					mountains[ind1] = m
					mountains[ind2] = mountain 
					
		
	for m in mountains:
		nc = new_colour(used)
		used.append(nc)
		draw.polygon(m, fill = nc)
		
	if not os.path.exists('imgs'):
		os.makedirs('imgs')

	counter  = len(os.listdir('imgs'))
	filename = str(counter) + ".png"
	image.save('imgs/' + filename)
	
	return (filename, counter)
	
for _ in range(0,100):
	mountain_range()
