# run this file in terminal is recommended

import matplotlib.pyplot as plt

from utils import *

# define image height and width
width = 512
height = 512

# define view point
camera = np.array([0, 0, 1])
ratio = float(width) / height
screen = (-1, 1 / ratio, 1, -1 / ratio)  # left, top, right, bottom

# define light source
light = {
    'position': np.array([3, 3, 3]),
    'diffuse': np.array([1, 1, 1]),
}

# define spheres
objects = [
    {
        'center': np.array([0, 0, -1]),
        'radius': 0.7,
        'diffuse': np.array([.8, 0, 0]),
    },
    {
        'center': np.array([-0.3, 0, 0]),
        'radius': 0.15,
        'diffuse': np.array([0, .8, 0]),
    },
    {
        'center': np.array([0.1, -0.3, 0]),
        'radius': 0.1,
        'diffuse': np.array([0, 0, .8]),
    },
]

image = np.full((height, width, 3), .1)
for i, y in enumerate(np.linspace(screen[1], screen[3], height)):
    print(f' Progress: {(i + 1) / height * 100: .2f}%', end='\r')

    for j, x in enumerate(np.linspace(screen[0], screen[2], width)):
        # screen is on origin
        pixel = np.array([x, y, 0])
        origin = camera
        direction = normalize(pixel - origin)

        # check for intersections
        nearestObject, minDistance = nearestIntersectedObject(objects, origin, direction)
        if nearestObject is None:
            continue

        # check for shadowing
        intersection = origin + minDistance * direction
        normalToSurface = normalize(intersection - nearestObject['center'])
        shiftedPoint = intersection + 1e-6 * normalToSurface
        intersectionToLight = normalize(light['position'] - shiftedPoint)

        _, minDistance = nearestIntersectedObject(objects, shiftedPoint, intersectionToLight)
        intersectionToLightDistance = np.linalg.norm(light['position'] - intersection)
        isShadowed = minDistance < intersectionToLightDistance

        if isShadowed:
            color = np.zeros(3)
        else:
            # calc diffused color
            color = nearestObject['diffuse'] * light['diffuse'] * np.dot(intersectionToLight, normalToSurface)

        image[i, j] = np.clip(color, 0, 1)

print()
plt.imsave('result.png', image)
plt.imshow(image)
plt.tight_layout()
plt.axis('off')
plt.show()
