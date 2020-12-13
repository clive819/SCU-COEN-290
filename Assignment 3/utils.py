import numpy as np


def normalize(vector):
    return vector / np.linalg.norm(vector)


def reflected(vector, axis):
    return vector - 2 * np.dot(vector, axis) * axis


def sphereIntersect(center, radius, rayOrigin, rayDirection):
    b = 2 * np.dot(rayDirection, rayOrigin - center)
    c = np.linalg.norm(rayOrigin - center) ** 2 - radius ** 2
    delta = b ** 2 - 4 * c
    if delta >= 0:
        t1 = (-b + np.sqrt(delta)) / 2
        t2 = (-b - np.sqrt(delta)) / 2
        if t1 > 0 and t2 > 0:
            return min(t1, t2)
    return None


def nearestIntersectedObject(objects, rayOrigin, rayDirection):
    distances = [sphereIntersect(obj['center'], obj['radius'], rayOrigin, rayDirection) for obj in objects]
    nearestObject = None
    minDistance = np.inf
    for index, distance in enumerate(distances):
        if distance and distance < minDistance:
            minDistance = distance
            nearestObject = objects[index]
    return nearestObject, minDistance
