from math import sqrt
from shapely.geometry import Polygon, LineString, Point
from shapely.ops import split, nearest_points
from shapely.affinity import rotate
from random import uniform as randfloat

MAX_FAILS = 10

# line distance from
# https://stackoverflow.com/questions/328107/how-can-you-determine-a-point-is-between-two-other-points-on-a-line-segment
def line_distance(a, b):
    return sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

def is_point_on_line(a, b, c, epsilon=0.000001):
    return -epsilon <= line_distance(a, c) + line_distance(c, b) - line_distance(a, b) <= epsilon

def is_line_on_line(larger, smaller):
    return is_point_on_line(larger[0], larger[1], smaller[0], epsilon=1.0) and is_point_on_line(larger[0], larger[1], smaller[1])

def points_are_equal(p1, p2, epsilon=0.000001):
    return -epsilon <= line_distance(p1, p2) <= epsilon 

def split_polygon(polygon, line_lst):
    line = LineString(line_lst)

    geometry_collection = split(polygon, line)

    result = []
    for element in geometry_collection:
        coords = [(a[0], a[1]) for a in list(element.exterior.coords)]

        result.append((coords, element))

    return result

def point_in_polygon(polygon, point):
    return polygon.contains(point)

def nearest_point_to_polygon(polygon, point):
    p1, p2 = nearest_points(polygon, point)

    return (p1.x, p1.y)

def compare_polygon_area(original, current):
    if not original or not current:
        return 0.0

    percentage = (original.area - current.area) / original.area

    return percentage

def random_points_from_polygon(polygon, number=1, boundary=None, min_distance=0, distance_from=None):
    points = []
    minx, miny, maxx, maxy = polygon.bounds

    if boundary:
        bounds_w = boundary[0]
        bounds_h = boundary[1]

        minx += bounds_w
        maxx -= bounds_w
        miny += bounds_h
        maxy -= bounds_h

    fails = 0
    while len(points) < number:
        point = Point(randfloat(minx, maxx), randfloat(miny, maxy))

        if polygon.contains(point):
            if fails != MAX_FAILS and distance_from and min_distance != 0:
                line = LineString([distance_from, point])

                if line.length < min_distance:
                    fails += 1
                    continue

            points.append(point)

    return points

def closest_vertex_polygon(polygon, point):
    coords = polygon.exterior.coords

    lowest = min(coords, key=lambda x: line_distance(x, point))

    return lowest
