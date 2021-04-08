from shapely.geometry import Polygon, LineString, Point
from shapely.ops import split, nearest_points
from shapely.affinity import rotate
from random import uniform as randfloat

MAX_FAILS = 10

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
