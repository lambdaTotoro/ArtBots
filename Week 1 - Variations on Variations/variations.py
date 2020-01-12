import math
import os
import random

from PIL import Image, ImageDraw

# Some Geometric Functions we'll need later.

# Standard euclidean distance between two points on the plane.
def distance(p1,p2):
	return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

# Intersection points of two circles.
def get_intersections(x0, y0, r0, x1, y1, r1):
	d = distance((x1,y1), (x0,y0))

	# non intersecting
	if d > r0 + r1 :
		return None
	# One circle within other
	if d < abs(r0-r1):
		return None
	# coincident circles
	if d == 0 and r0 == r1:
		return None
	else:
		a=(r0**2-r1**2+d**2)/(2*d)
		h=math.sqrt(r0**2-a**2)
		x2=x0+a*(x1-x0)/d
		y2=y0+a*(y1-y0)/d
		x3=x2+h*(y1-y0)/d
		y3=y2-h*(x1-x0)/d

		x4=x2-h*(y1-y0)/d
		y4=y2+h*(x1-x0)/d

		return [(x3, y3), (x4, y4)]

def find_center(p1, p2, ps, radius):
	i1 = get_intersections(p1[0], p1[1], radius, p2[0], p2[1], radius)

	assert(i1 is not None)
	assert(len(i1) == 2)

	xs = list(map((lambda tp:tp[0]), ps))
	ys = list(map((lambda tp:tp[1]), ps))

	x_avg = sum(xs) / len(xs)
	y_avg = sum(ys) / len(ys)

	d1 = distance(i1[0], (x_avg,y_avg))
	d2 = distance(i1[1], (x_avg,y_avg))

	if d1 < d2:
		center = i1[0]
	else:
		center = i1[1]

	return center

def variation_by_trace(trace):
	valid = True
	elems = trace.split("-")

	n = int(elems.pop(0))
	valid = valid and (n < 9) and (n > 4)

	resolution = int(elems.pop)
	valid = valid and (resolution >= 100)

	winkel = int(elems.pop(0))
	valid = valid and (winkel >= 0) and (winkel <= 360)

	indices = []
	for i in range(0,n-3):
		indices.append(int(elems.pop(0)))

	colours = []
	for j in range(0,n-2):
		colours.append(int(elems.pop(0)))

	valid = valid and (len(elems) == 0)

	if valid:
		return variation(px = resolution, max_poly = n, deg = winkel,
                                      inds = indices, cols = colours)
	else:
		return None

def variation(px = None, max_poly = None, deg = None, 
                             inds = None, cols = None):

	# Setup and bookkeeping
	n = 3 + random.randint(2,6) if max_poly is None else max_poly
	
	# String to identify this particular image by.
	trace = str(n) + "-"

	gons = []
	sz   = 1000 if px is None else px

	if inds is not None:
		assert(len(inds) == n-3)

	if cols is not None:
		assert(len(cols) == n-2)

	# counting variable so I don't have to think up formulas.
	j = 0

	# Calculate Polygon Coordinates
	for m in range(n,2,-1):
		gon = []
		if m == n:
			radius = 0.95 * (sz / 2)
			winkel = random.randint(0,359) if deg is None else deg
			trace  = trace + str(winkel) + "-"
			theta  = math.radians(winkel) # Angles almost always in radians.

			for k in range(0,m):
				x = (sz / 2) + (radius * math.cos(2 * math.pi * k/m + theta))
				y = (sz / 2) + (radius * math.sin(2 * math.pi * k/m + theta))
				gon.append((round(x),round(y)))

			gons.append(gon)

		else:

			old   = gons[-1]
			index = random.randint(0,len(old)-1) if inds is None else inds[j]
			trace = trace + str(index) + "-"
			j += 1

			p1 = old[index-1] # Works even when index is 0. Thank you, python!
			p2 = old[index]

			# Calculating radius of polygon from one of its edges.
			length = distance(p1,p2)
			radius = length / (2 * math.sin(math.pi / m))
			
			center = find_center(p1,p2,old,radius)

			champ  = float('inf')
			theta  = 0
			factor = 1000.0	# This is big because time spent on each image is
											# not very important, but neat fit of polygons is!

			for w in range(0,360 * int(factor)):
				a = center[0] + (radius * math.cos(math.radians(w/factor)))
				b = center[1] + (radius * math.sin(math.radians(w/factor)))

				if distance((a,b), p1) < champ:
					theta = math.radians(w/factor)
					champ = distance((a,b), p1)

			for k in range(0,m):
				x = center[0] + (radius * math.cos(2 * math.pi * k/m + theta))
				y = center[1] + (radius * math.sin(2 * math.pi * k/m + theta))
				gon.append((round(x),round(y)))

			gons.append(gon)

	# Create Image

	colours = ["gray", "black", "red", "maroon", "olive", "green", "teal",
							"blue", "navy", "fuchsia", "purple", "deeppink",
							"darkorange", "orangered", "gold", "indigo",
							"springgreen", "lightseagreen"]

	white = (255,255,255)
	image = Image.new(mode = "RGB", size = (sz,sz), color = white)
	draw  = ImageDraw.Draw(image)

	# Assign colours to polygons
	used   = []
	colour = ""
	for gon in gons:
		if cols is not None:
			colour = colours[j]
			used.append(colour)
			j += 1
			trace = trace + str(j) + "-"
		else:
			c_index = random.randint(0,len(colours)-1)
			colour  = colours[c_index] 
			while colour in used:
				c_index = random.randint(0,len(colours)-1)
				colour  = colours[c_index]
			trace = trace + str(c_index) + "-"  
			used.append(colour)
		
		draw.polygon(gon, fill = colour)

	# Save Image
	if not os.path.exists('imgs'):
		os.makedirs('imgs')

	counter  = len(os.listdir('imgs'))
	filename = str(counter) + ".png"
	image.save('imgs/' + filename)

	trace = trace + str(sz)

	print("Generated " + filename + " successfully! Trace:", trace)
	return (filename, trace, counter)
