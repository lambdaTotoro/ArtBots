import itertools
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

def randomImage(size = 1000):
	return io.imread("https://picsum.photos/" + str(size))

def vadd(v1, v2):
	return (v1[0] + v2[0], v1[1] + v2[1])

def approximate(image = None, nsteps = 20000, px = 1200):
	
	target = np.array(Image.open(image).convert("RGB")) if image is not None else randomImage(px)
	
	no_imgs = len(os.listdir("imgs")) // 2
	(dx,dy) = (target.shape[0], target.shape[1])
	
	gray  = random.randint(0,255)
	image = Image.new(mode = "RGB", size = (dx,dy), color = (gray,gray,gray))
	draw  = ImageDraw.Draw(image)

	mse = float("inf")
	steps = nsteps
	
	vectors = []
	for _ in range(0,3):
		x = random.randint(-50,50)
		y = random.randint(-50,50)
		for s in range(-2,2,1):
			vectors.append((s * x, s * y))
	
	champion = (None,float("inf"))
		
	while steps > 0:
				
		p1 = (random.randint(0,dx-1), random.randint(0,dy-1))
		cp = (p1[1],p1[0])
		colour = (target[cp][0], target[cp][1], target[cp][2])
		
		choices = []
		for v in vectors:
			p2 = vadd(p1, v)
			choices.append((p1,p2,colour))
		
		best_candidate = champion
		
		for config in choices:
			copy  = image.copy()
			cdraw = ImageDraw.Draw(copy)
			cdraw.line([config[0],config[1]],width=random.randint(5,10),fill=config[2])
			ref = np.array(copy)
			
			mse = metrics.mean_squared_error(target,ref)
			steps -= 1
			if mse < best_candidate[1]:
				best_candidate = (copy, mse)
				break
		
		if best_candidate[1] < champion[1]:
			champion = best_candidate
			image = champion[0]
			
	# Save image
	fn = str(len(os.listdir('imgs'))) + ".png"
	champion[0].save("./imgs/" + fn)
	return fn
