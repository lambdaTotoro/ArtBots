import math
import os
import random

import numpy as np

from PIL import Image, ImageDraw
from skimage.io import imsave

def possibilities(arr, p, m):
	(x,y) = p
	ps = []
	
	p1 = ((x+1) % m,y % m)
	p2 = ((x-1) % m,y % m)
	p3 = (x % m, (y+1) % m)
	p4 = (x % m, (y-1) % m)
	
	for q in [p1,p2,p3,p4]:
		if not arr[q]:
			ps.append(q)
	
	return ps
	
def next_colour(c,cd):

	dr = random.randint(-cd,cd)
	dg = random.randint(-cd,cd)
	db = random.randint(-cd,cd)
	
	red   = max(0,min(c[0] + dr,255))
	green = max(0,min(c[1] + dg,255))
	blue  = max(0,min(c[2] + db,255))
	
	return (red,green,blue)

def new_walk(sz = 1000, cw = 100, bc = (0,0,0), bw = 5, cdelta = 40):
	
	somegray = random.randint(50,150)
	bg = (somegray,somegray,somegray)
	
	image = Image.new(mode = "RGB", size = (sz,sz), color = bg)
	draw  = ImageDraw.Draw(image)
	
	# Draw Grid
	
	draw.line([(0,0),(sz,0)], bc, bw*2)
	draw.line([(0,0),(0,sz)], bc, bw*2)
	draw.line([(sz,sz),(sz,0)], bc, bw*2)
	draw.line([(sz,sz),(0,sz)], bc, bw*2)
	
	squares = 1
	
	for x in range(1,sz):
		if (x % cw == 0):
			ln = [(x,0),(x,sz)]
			draw.line(ln, bc, bw)
			squares += 1
	
	for y in range(1,sz):
		if (y % cw == 0):
			ln = [(0,y),(sz,y)]
			draw.line(ln, bc, bw)
	
	# Walk
	
	field = np.zeros((squares,squares), 'bool')	
	free = True
	steps = random.randint(round(0.25*squares*squares), round(0.5*squares*squares))
	
	current_x = random.randint(0,squares-1)
	current_y = random.randint(0,squares-1)
	current_colour = (random.randint(30,225),random.randint(30,225),random.randint(30,225))
	
	ps = possibilities(field, (current_x, current_y), squares)
	imgarr = np.array(image)
		
	while (free and steps > 0):
		
		for fx in range(max(0,current_x * cw), min(sz,(current_x+1) * cw)):
			for fy in range(max(0,current_y * cw), min(sz,(current_y+1) * cw)):
				for ch in range(3):
					imgarr[fx][fy][ch] = current_colour[ch]
			
		field[current_x][current_y] = True
		
		(current_x,current_y) = random.choice(ps)
		current_colour = next_colour(current_colour,10)
		
		steps -= 1
		ps = possibilities(field, (current_x, current_y), squares)
		free = ps != []
	
	# Redraw Grid
	
	image = Image.fromarray(imgarr)
	draw  = ImageDraw.Draw(image)
	
	draw.line([(0,0),(sz,0)], bc, bw*2)
	draw.line([(0,0),(0,sz)], bc, bw*2)
	draw.line([(sz,sz),(sz,0)], bc, bw*2)
	draw.line([(sz,sz),(0,sz)], bc, bw*2)
	
	for x in range(1,sz):
		if (x % cw == 0):
			ln = [(x,0),(x,sz)]
			draw.line(ln, bc, bw)
	
	for y in range(1,sz):
		if (y % cw == 0):
			ln = [(0,y),(sz,y)]
			draw.line(ln, bc, bw)
	
	# Save image
	
	if not os.path.exists('imgs'):
		os.makedirs('imgs')
		
	if not os.path.exists('imgs/counter.txt'):
		cfile = open('imgs/counter.txt', 'w+')
		cfile.write(str(1))
		cfile.close()

	cfile = open('imgs/counter.txt')
	counter  = int(cfile.readline()) + 1
	cfile.close()
	
	cfile = open('imgs/counter.txt', 'w+')
	cfile.write(str(counter))
	cfile.close()
	
	filename = str(counter) + ".png"
	image.save('imgs/' + filename)
	
	return (filename, counter)
