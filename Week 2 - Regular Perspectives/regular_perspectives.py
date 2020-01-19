import datetime
import math
import os
import random
import shutil

from pathlib import Path
from PIL import Image, ImageDraw

from skimage import color
from skimage import io
from skimage import metrics

import numpy as np

def regularPolygon(center,radius,edges,angle):
	polygon = []
	theta = math.radians(angle)

	# Coordinates of regular polygon according to this:
	# https://stackoverflow.com/a/7198179/1953518
	for m in range(0,edges):
		x = radius * math.cos(2 * math.pi * (m/edges) + theta) + center[0]
		y = radius * math.sin(2 * math.pi * (m/edges) + theta) + center[1]
		
		# Rounded because we only have whole pixels.
		polygon.append((round(x),round(y)))

	return polygon

def randomImage():
	return io.imread("https://picsum.photos/1200")

def approximate(img = None, npoints = 6):
	
	today = str(datetime.date.today())

	dirpath = Path("days",today)
	if dirpath.exists() and dirpath.is_dir():
		shutil.rmtree(dirpath)
		
	os.mkdir("./days/" + today)

	if img is None:
		target = randomImage() 
		io.imsave("./days/" + today + "/target.png", target, plugin = "pil")
	else:
		target = io.imread(img, as_gray = False, plugin = "pil")

	counter = 0

	w, h = target.shape[0], target.shape[1]
	champion = (None, float("inf"))


	while counter < 10000:

		points = []
		for p in range(0, random.randint(4,npoints)):
			points.append((random.randint(0,w), random.randint(0,h)))

		rbg  = (random.randint(0,255),
					 	random.randint(0,255),
						random.randint(0,255))

		image = Image.new(mode = "RGB", size = (h,w), color = rbg)
		draw  = ImageDraw.Draw(image)

		for p in points:
			theta  = random.randint(0,360)
			radius = random.randint(75, round(0.4 * max(w,h)))
			sides  = random.randint(3,8)
			rc	= (random.randint(0,255),
						 random.randint(0,255),
						 random.randint(0,255))

			polygon = regularPolygon(p,radius,sides,theta)
			draw.polygon(polygon, fill = rc)

		ref = np.array(image)
		mse = metrics.mean_squared_error(target,ref)
		counter += 1
		if mse < champion[1]:
			if champion[1] != float("inf"):
				champion[0].save("./days/" + today + "/champion-" + str(counter) + ".png")
			champion = (image,mse)
			print("New Champion!", counter, champion[1])
	
	print("Final champion:", counter, champion[1])
	champion[0].save("./days/" + today + "/approximation.png")
