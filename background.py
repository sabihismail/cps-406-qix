import pygame
from entity import Entity, Direction
from draw_util import get_lines_by_rect, to_line_list, to_vertices_list, lines_to_dict, vertices_to_dict
from collision_util import is_point_on_line, is_line_on_line

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
        self.temp_trail = []

    def late_init(self):
        display_width, display_height = self.surface.get_size()

        self.pos_x = (display_width - WIDTH) / 2
        self.pos_y = (display_height - HEIGHT) / 2
        
        self.bounds = pygame.Rect(self.pos_x, self.pos_y, WIDTH, HEIGHT)

        self.active_trail = to_vertices_list(get_lines_by_rect(self.bounds))

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

    def leaves_play_area(self, x, y):
        ret_x = x
        ret_y = y

        if x < self.bounds.x:
            ret_x = self.bounds.x

        if y < self.bounds.y:
            ret_y = self.bounds.y

        if x > self.bounds.x + self.bounds.width:
            ret_x = self.bounds.x + self.bounds.width

        if y > self.bounds.x + self.bounds.height:
            ret_y = self.bounds.y + self.bounds.height

        return (ret_x, ret_y)

    def on_perimeter(self):
        if not self.current_trail_start or not self.current_trail_end:
            return True

        for line in to_line_list(self.active_trail):
            if is_line_on_line(line, (self.current_trail_start, self.current_trail_end)):
                return True

        return False

    def add_trail(self, x, y, direction):
        x = int(x)
        y = int(y)

        if direction != self.last_trail_direction:
            if self.current_trail_end and not self.on_perimeter():
                self.temp_trail.append((self.current_trail_start, self.current_trail_end))

            self.current_trail_start = self.current_trail_end or (x, y)
            self.current_trail_end = (x, y)
            self.last_trail_direction = direction
        else:
            self.current_trail_end = (x, y)

        self.check_connection()

    def check_connection(self):
        if self.current_trail_end == self.current_trail_start:
            return

        for line in to_line_list(self.active_trail):
            if is_point_on_line(line[0], line[1], self.current_trail_start):
                continue

            if is_point_on_line(line[0], line[1], self.current_trail_end):
                self.add_to_active_trails(line)
                return

    def add_to_active_trails(self, start_line):
        self.temp_trail.append((self.current_trail_start, self.current_trail_end))

        end_line = None
        for line in to_line_list(self.active_trail):
            if is_point_on_line(line[0], line[1], self.current_trail_end):
                end_line = line
                break

        vertices = to_vertices_list(self.temp_trail)
        vertices = vertices[:-1]
        vertices.insert(0, start_line[0])
        vertices.append(end_line[1])

        d = vertices_to_dict(self.active_trail)
        print(self.temp_trail)
        print(vertices)
        print(d)
        while vertices[0] != vertices[len(vertices) - 1]:
            last_vertex = vertices[len(vertices) - 1]

            possible_next_vertices = d[last_vertex][::-1]

            best_vertex = self.find_best_vertex(vertices, possible_next_vertices)

            vertices.append(best_vertex)

        self.active_trail = vertices
        self.temp_trail = []

        self.current_trail_start = None
        self.current_trail_end = None
        self.last_trail_direction = None

    def find_best_vertex(self, lst, next_vertices):
        for vertex in next_vertices:
            tmp = list(lst)
            
            if tmp.count(vertex) <= 1:
                return vertex
