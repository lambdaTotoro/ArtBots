import math
import os
import random

from mastodon import Mastodon
from PIL      import Image, ImageDraw

# Some Geometric Functions we'll need later.
def distance(p1,p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

# Circle Intersection we'll need later.
def get_intersections(x0, y0, r0, x1, y1, r1):
    # circle 1: (x0, y0), radius r0
    # circle 2: (x1, y1), radius r1

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

def find_center(points, radius):
    ps = points[0:2]
    i1 = get_intersections(ps[0][0], ps[0][1], radius, ps[1][0], ps[1][1], radius)

    assert(i1 is not None)
    assert(len(i1) == 2)

    xs = list(map((lambda tp:tp[0]), ps))
    ys = list(map((lambda tp:tp[1]), ps))

    print(xs)

    x_avg = sum(xs) / len(xs)
    y_avg = sum(ys) / len(ys)

    d1 = distance(i1[0], (x_avg,y_avg))
    d2 = distance(i1[1], (x_avg,y_avg))

    if d1 < d2:
        center = i1[0]
    else:
        center = i1[1]

    return center

# Set up Mastodon
mastodon = Mastodon(
    access_token = 'token.secret',
    api_base_url = 'https://botsin.space'
)

# Calculate Polygon Coordinates

n = 3 + random.randint(0,7)
gons = []

for m in range(n,2,-1):

    gon = []

    if m == n:
        radius = 240
        theta  = math.radians(random.randint(0,360))
        
        for k in range(0,m):
            x = 250 + (radius * math.cos(2 * math.pi * k/m + theta))
            y = 250 + (radius * math.sin(2 * math.pi * k/m + theta)) 
            gon.append((round(x),round(y)))
    else:
        oldgon = gons[-1]
        index  = random.randint(0,len(oldgon)-1)
        p1 = oldgon[index-1] # Works even when index is 0. Thank you, python!
        p2 = oldgon[index]

        length = distance(p1,p2)
        radius = length / (2 * math.sin(math.pi / m))

        center = find_center(oldgon,radius)
        
        for k in range(0,m):
            x = center[0] + (radius * math.cos(2 * math.pi * k/m))
            y = center[1] + (radius * math.sin(2 * math.pi * k/m)) 
            gon.append((round(x),round(y)))

    gons.append(gon)
    print("Creating", str(m) + "-gon:", gon)

# Create Image

colours = ["orange", "pink", "red", "blue", "yellow", "green", "purple", "black"]

image = Image.new(mode = "RGB", size = (500,500), color = (255,255,255))
draw  = ImageDraw.Draw(image)

for gon in gons:
    if len(gon) >= 2:
        draw.polygon(gon, fill = random.choice(colours))

# Save Image

if not os.path.exists('imgs'):
    os.makedirs('imgs')

counter  = len(os.listdir('imgs'))
filename = str(counter) + ".png"

image.save('imgs/' + filename)

# Post to Mastodon
    
