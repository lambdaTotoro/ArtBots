
from PIL import Image, ImageDraw

from skimage import io
from skimage import metrics

def approximate(img, npoints = 5, ngons = 5, nradii = 5, ncolours = 5):

	mars = io.imread(img,"pil")
	w, h = len(mars), len(mars[0])

	white = (0,0,0)
	image = Image.new(mode = "RGB", size = (w,h), color = white)
	draw  = ImageDraw.Draw(image)

	image.save("days/compare.jpg")
	ref = io.imread("days/compare.jpg", "pil")

	mse = metrics.mean_squared_error(mars,ref)
	print(mse)

approximate("days/mars.jpg")
