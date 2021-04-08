import pygame
from shapely.geometry import Point, Polygon, LineString
from entity import Entity, Direction
from draw_util import get_lines_by_rect, to_line_list, to_vertices_list, lines_to_dict, unique_vertices_to_dict
from collision_util import is_point_on_line, is_line_on_line
from math_util import split_polygon, point_in_polygon, nearest_point_to_polygon
from math import trunc

WIDTH = 600.0
HEIGHT = WIDTH
FULL_BACKGROUND_COLOUR = (20, 20, 20)
INSIDE_COLOR = (150, 150, 150)
OUTLINE_COLOR = (100, 100, 100)
OUTLINE_WIDTH = 1
TRAIL_COLOR = (0, 255, 0)

class ListNode():
    def __init__(self, x):
        self.val = x
        self.next = None

class Background(Entity):
    def __init__(self, unique_id):
        super().__init__(unique_id, width=WIDTH, height=HEIGHT, pos_x=0.0, pos_y=0.0)
        self.bounds = None
        self.last_trail_direction = None
        self.current_trail_start = None
        self.current_trail_end = None
        self.active_trail = []
        self.active_trail_polygon = None
        self.temp_trail = []
        self.off_perimeter = False

    def late_init(self):
        display_width, display_height = self.surface.get_size()

        self.pos_x = (display_width - WIDTH) / 2
        self.pos_y = (display_height - HEIGHT) / 2
        
        self.bounds = pygame.Rect(self.pos_x, self.pos_y, WIDTH, HEIGHT)

        trail = to_vertices_list(get_lines_by_rect(self.bounds))
        self.set_active_trail(trail)

    def set_active_trail(self, trail, polygon=None):
        self.active_trail = trail
        if not polygon:
            self.active_trail_polygon = Polygon(trail)
        else:
            self.active_trail_polygon = polygon

    def draw_polygon(self, vertices):
        pygame.draw.polygon(self.surface, INSIDE_COLOR, vertices, width=0)

        for line in to_line_list(vertices):
            pygame.draw.line(self.surface, TRAIL_COLOR, line[0], line[1], width=1)

    def draw(self):
        self.surface.fill(FULL_BACKGROUND_COLOUR)

        self.draw_polygon(self.active_trail)

        for trail in self.temp_trail:
            pygame.draw.line(self.surface, TRAIL_COLOR, trail[0], trail[1], width=1)
        
        if self.current_trail_start and self.current_trail_end:
            pygame.draw.line(self.surface, TRAIL_COLOR, self.current_trail_start, self.current_trail_end, width=1)

    def leaves_play_area(self, x, y, x2, y2):
        ret_x = x
        ret_y = y
        '''pointer = Point(x,y)

        for line in to_line_list(self.active_trail):
            if is_point_on_line(line[0], line[1], (trunc(x2), trunc(y2))):
                if line[0][0] == line[1][0]:
                    bruh = max(line[0][1],line[1][1])
                    brah = min(line[0][1],line[1][1])
                    if x < line[0][0] and not pointer.intersects(self.active_trail_polygon):
                        ret_x = line[0][0]
                    if x > line[0][0] and not pointer.intersects(self.active_trail_polygon):
                        ret_x = line[0][0]
                    if y < brah and not pointer.intersects(self.active_trail_polygon):
                        ret_y = brah
                    if y > bruh and not pointer.intersects(self.active_trail_polygon):
                        ret_y = bruh
                if line[0][1] == line[1][1]:
                    bruh = max(line[0][0],line[1][0])
                    brah = min(line[0][0],line[1][0])
                    if y < line[0][1] and not pointer.intersects(self.active_trail_polygon):
                        ret_y = line[0][1]
                    if y > line[0][1] and not pointer.intersects(self.active_trail_polygon):
                        ret_y = line[0][1]
                    if x < brah and not pointer.intersects(self.active_trail_polygon):
                        ret_x = brah
                    if x > bruh and not pointer.intersects(self.active_trail_polygon):
                        ret_x = bruh'''

        pointer = Point(x, y)
        if not point_in_polygon(self.active_trail_polygon, pointer):
            point = nearest_point_to_polygon(self.active_trail_polygon, pointer)

            ret_x, ret_y = point[0], point[1]

        return (ret_x, ret_y)

    def line_on_perimeter(self, start, end):
        if not start or not end:
            return False

        for line in to_line_list(self.active_trail):
            if is_line_on_line(line, (self.current_trail_start, self.current_trail_end)):
                return True

        return False

    def point_on_perimeter(self, point):
        if not point:
            return False

        for line in to_line_list(self.active_trail):
            if is_point_on_line(line[0], line[1], point):
                return True

        return False

    def add_trail(self, x, y, direction):
        point = (x, y)
        if not self.point_on_perimeter(point):
            self.off_perimeter = True

            if direction != self.last_trail_direction and not Direction.opposite(self.last_trail_direction, direction):
                if self.current_trail_end:
                    self.temp_trail.append((self.current_trail_start, self.current_trail_end))
                    self.current_trail_start = self.current_trail_end or point

                self.current_trail_end = point
                self.last_trail_direction = direction
            else:
                self.current_trail_end = (x, y)
        else:
            if self.current_trail_start and self.off_perimeter:
                self.current_trail_end = point
                self.temp_trail.append((self.current_trail_start, self.current_trail_end))

                self.check_connection()

                self.off_perimeter = False
            else:
                self.current_trail_start = point

    def check_connection(self):
        if not self.current_trail_start or not self.current_trail_end:
            return

        if self.current_trail_end == self.current_trail_start:
            return

        self.add_to_active_trails()

    def add_to_active_trails(self):
        self.temp_trail.append((self.current_trail_start, self.current_trail_end))

        temp_trail_vertices = to_vertices_list(self.temp_trail)
        polygons = split_polygon(self.active_trail_polygon, temp_trail_vertices)
        polygons.sort(key=lambda x: x[1].area)

        small_polygon = polygons[0]
        large_polygon = polygons[1]

        self.set_active_trail(large_polygon[0], large_polygon[1])
        self.temp_trail = []

        self.current_trail_start = None
        self.current_trail_end = None
        self.last_trail_direction = None

    def find_best_vertex(self, lst, next_vertices):
        for vertex in next_vertices:
            tmp = list(lst)
            
            if tmp.count(vertex) <= 1:
                return vertex
