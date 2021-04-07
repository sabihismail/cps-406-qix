import pygame
from math import sqrt

# line distance from
# https://stackoverflow.com/questions/328107/how-can-you-determine-a-point-is-between-two-other-points-on-a-line-segment
def line_distance(a, b):
    return sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

def is_point_on_line(a, b, c, epsilon=0.000001):
    return -epsilon <= line_distance(a, c) + line_distance(c, b) - line_distance(a, b) <= epsilon

def is_line_on_line(a, b):
    larger = a if line_distance(a[0], a[1]) > line_distance(b[0], b[1]) else b
    smaller = b if larger == a else a

    return is_point_on_line(larger[0], larger[1], smaller[0], epsilon=1.0) and is_point_on_line(larger[0], larger[1], smaller[1])
