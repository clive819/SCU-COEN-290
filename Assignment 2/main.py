import csv

import numpy as np
from PIL import Image

IMAGE_SIZE = 600
PROJ_REF_POINT = 4

points = Image.new('RGB', (IMAGE_SIZE, IMAGE_SIZE))
wireframe = Image.new('RGB', (IMAGE_SIZE, IMAGE_SIZE))
vertices = []
triangles = []


def clamp(num, minVal=0, maxVal=IMAGE_SIZE - 1):
    return min(maxVal, max(minVal, int(num)))


def drawPixel(x, y, z):
    nx = clamp(x / (1 - z / PROJ_REF_POINT))
    ny = clamp(y / (1 - z / PROJ_REF_POINT))

    oriColor = pixels[nx, ny][0]
    newColor = int(255 * (z + 1))
    pixels[nx, ny] = (max(oriColor, newColor), 0, 0)


def drawLine(p1, p2):
    if p2[0] < p1[0]:
        drawLine(p2, p1)
        return

    p1x, p1y, p1z = p1
    p2x, p2y, p2z = p2

    dx = p2x - p1x
    dy = p2y - p1y
    dz = p2z - p1z

    for nx in np.arange(p1x, p2x, .2):
        ny = (nx - p1x) / dx * dy + p1y
        nz = (nx - p1x) / dx * dz + p1z
        drawPixel(nx, ny, nz)


# read in face vertices
with open('face-vertices.data') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        vertices.append(row)

# normalize
vertices = np.asarray(vertices, dtype=np.float32)
maxXY = max(abs(np.concatenate((vertices[..., 0], vertices[..., 1]))))
maxZ = max(abs(vertices[..., 2]))

vertices[..., 0] = vertices[..., 0] * ((IMAGE_SIZE / 2.5) / maxXY) + IMAGE_SIZE / 2
vertices[..., 1] = IMAGE_SIZE - (vertices[..., 1] * ((IMAGE_SIZE / 2.5) / maxXY) + IMAGE_SIZE / 2)
vertices[..., 2] = vertices[..., 2] * (.5 / maxZ) - .5

# read index
with open('face-index.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for index in csv_reader:
        triangles.append([vertices[int(i)] for i in index])

# project all points to xy-plane
pixels = points.load()

for vertex in vertices:
    drawPixel(*vertex)

# project wireframe
pixels = wireframe.load()

for v1, v2, v3 in triangles:
    drawLine(v1, v2)
    drawLine(v2, v3)
    drawLine(v1, v3)

# display
points.show()
wireframe.show()

points.save('Points.png')
wireframe.save('Wireframe.png')
