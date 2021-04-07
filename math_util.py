from shapely.geometry import Polygon, LineString
from shapely.ops import split

def split_polygon(polygon, line_lst):
    line = LineString(line_lst)

    geometry_collection = split(polygon, line)

    result = []
    for element in geometry_collection:
        coords = [(int(a[0]), int(a[1])) for a in list(element.exterior.coords)]

        result.append((coords, element))

    return result
