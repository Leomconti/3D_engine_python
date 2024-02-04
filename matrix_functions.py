import math
import numpy as np

def translate(pos):
    tx, ty, tz = pos
    return np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [tx, ty, tz, 1]
    ])

def rotate_x(theta):
    return np.array([
        [1, 0, 0, 0],
        [0, math.cos(theta), math.sin(theta), 0],
        [0, -math.sin(theta), math.cos(theta), 0],
        [0, 0, 0, 1]
    ])

def rotate_y(theta):
    return np.array([
        [math.cos(theta), 0, -math.sin(theta), 0],
        [0, 1, 0, 0],
        [math.sin(theta), 0, math.cos(theta), 0],
        [0, 0, 0, 1]
    ])

def rotate_z(theta):
    return np.array([
        [math.cos(theta), math.sin(theta), 0, 0],
        [-math.sin(theta), math.cos(theta), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])

def scale(s):
    return np.array([
        [s, 0, 0, 0],
        [0, s, 0, 0],
        [0, 0, s, 0],
        [0, 0, 0, 1]
    ])