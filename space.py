
"""
Use numpy to represent each position and collisions between shapes
(considering just shapes for the moment). Here we might as well define
what we would be a screen.

Define the scatterer (initially) at the origin of the frame.
"""

import numpy as np

import draw

WIDTH, HEIGHT = 800, 800

centre = np.array([WIDTH / 2, HEIGHT / 2])
zero = np.array([0, 0])

def mag(vec):
    return np.linalg.norm(vec)

def unit(vec):
    return vec/mag(vec)

def angle(vec):
    if vec[1] == 0 and vec[0] > 0:
        return 0
    elif vec[1] == 0 and vec[0] < 0:
        return np.pi
    elif vec[0] == 0 and vec[1] > 0:
        return np.pi / 2
    elif vec[0] == 0 and vec[1] < 0:
        return 3 * np.pi / 2
    elif vec[0] > 0:
        return np.arctan(vec[1] / vec[0])
    else:
        return np.arctan(vec[1] / vec[0]) + np.pi

def checkLineIntersection(Line1, Line2): 
    if type(Line1) is not draw.Line or type(Line2) is not draw.Line:
        raise TypeError("Line1 and Line2 have to be lines")
    
    if Line1.getGradient() == Line2.getGradient():
        return False
    return True


def returnLineIntersection(part_pos, part_dir, Line2):
    pos1, pos2 = part_pos, Line2.getPos()
    grad1, grad2 = part_dir, Line2.getGradient()

    C = pos2 - pos1
    U = np.array([grad1, grad2]).T

    t = np.dot(np.linalg.inv(U), C)
    return t[0] * grad1 + pos1
