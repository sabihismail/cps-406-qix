from shapely.geometry import Polygon, LineString
from shapely.ops import split, nearest_points

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
