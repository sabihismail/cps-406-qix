import pygame
from random import randint
from shapely.geometry import LineString
from base.entity import Entity
from util.constants import BACKGROUND_ID, PLAYER_ID
from util.draw_util import rotate_surface
from util.math_util import random_points_from_polygon

WIDTH = 150.0
HEIGHT = WIDTH / 2
MOVE_OFFSET = 100.0
COLOUR = (0, 0, 255)
ANGLE_ROTATE_MULTIPLIER = 320.0
MOVE_RANDOMIZER = 100
MIN_ACCELERATION = 0.5

class Qix(Entity):
    def __init__(self, unique_id, speed=0.0, move_chance=0.0):
        super().__init__(unique_id, width=WIDTH, height=HEIGHT, pos_x=0.0, pos_y=0.0)
        self.speed = speed
        self.move_chance = move_chance

        self.background = None
        self.player = None
        self.display = None
        self.pos_x = 0.0
        self.pos_y = 0.0

        self.ellipse_surface = pygame.Surface((max(WIDTH, HEIGHT), max(WIDTH, HEIGHT)), pygame.SRCALPHA)
        self.angle = 0

        self.moving = False
        self.next_pos = None
        self.move_line = None
        self.current_line = None
        self.total_move = 0
        self.acceleration = 1

    def late_init(self):
        self.background = self.display.get_entity(BACKGROUND_ID)
        self.player = self.display.get_entity(PLAYER_ID)

        surface_pos = (0, 0, WIDTH, HEIGHT)
        pygame.draw.ellipse(self.ellipse_surface, COLOUR, surface_pos)

        self.pos_x = self.background.pos_x + self.background.bounds.width - max(WIDTH, HEIGHT) / 2
        self.pos_y = self.background.pos_y + self.background.bounds.height - max(WIDTH, HEIGHT) / 2

    def pre_draw(self, delta_time):
        self.angle += (ANGLE_ROTATE_MULTIPLIER * delta_time) % 360

        self.move(delta_time)
        self.check_player_collision()

    def check_player_collision(self):
        max_side = max(WIDTH, HEIGHT)

        ellipse_rect = pygame.Rect(self.pos_x - max_side / 2, self.pos_y - max_side / 2, max_side, max_side)
        player_bounds = pygame.Rect(self.player.bounds)

        if ellipse_rect.colliderect(player_bounds):
            self.player.handle_qix_damage()

    def draw(self):
        pos = (self.pos_x, self.pos_y)
        origin_pos = (WIDTH / 2, HEIGHT / 2)

        rotate_surface(self.surface, self.ellipse_surface, pos, origin_pos, self.angle)

    def move(self, delta_time):
        if not self.moving and randint(0, (MOVE_RANDOMIZER - self.move_chance)) == 0:
            random_points = random_points_from_polygon(self.background.active_trail_polygon,
                boundary=(max(WIDTH, HEIGHT), max(WIDTH, HEIGHT)),
                min_distance=(self.background.bounds.width / 2) * (1 - self.background.percentage),
                distance_from=(self.pos_x, self.pos_y))

            self.next_pos = random_points[0]
            self.move_line = LineString([(self.pos_x, self.pos_y), self.next_pos])
            self.current_line = LineString([(self.pos_x, self.pos_y), self.next_pos])
            self.moving = True
            self.total_move = 0

        if self.moving:
            distance_to_move = (MOVE_OFFSET + self.speed) * self.acceleration * delta_time
            move = distance_to_move / self.move_line.length
            self.total_move += move

            new_pos = self.move_line.interpolate(self.total_move, normalized=True)

            self.current_line = LineString([new_pos, self.next_pos])

            self.pos_x = new_pos.x
            self.pos_y = new_pos.y

            if self.current_line.length > (self.move_line.length / 2):
                self.acceleration += 0.2
            else:
                self.acceleration -= 0.2
                self.acceleration = max(1, self.acceleration)

            if self.current_line.length <= 1.0:
                self.acceleration = 1
                self.moving = False
                self.total_move = 0
