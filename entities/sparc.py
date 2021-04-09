import pygame
from random import randint
from base.entity import Entity, Direction
from util.constants import BACKGROUND_ID, PLAYER_ID
from util.draw_util import rotate_surface
from util.math_util import points_are_equal

WIDTH = 20
HEIGHT = WIDTH
MOVE_OFFSET = 100.0
COLOUR = (159, 50, 255)
ANGLE_ROTATE_MULTIPLIER = 320.0

class Sparc(Entity):
    def __init__(self, unique_id, speed=0.0):
        super().__init__(unique_id, width=WIDTH, height=HEIGHT, pos_x=0.0, pos_y=0.0)
        self.speed = speed

        self.background = None
        self.player = None
        self.display = None
        self.pos_x = 0.0
        self.pos_y = 0.0
        self.bounds = None

        self.entity_surface = pygame.Surface((max(WIDTH, HEIGHT), max(WIDTH, HEIGHT)), pygame.SRCALPHA)
        self.angle = 0
        self.current_direction = Direction.UP
        self.blocked = {
            Direction.LEFT: None,
            Direction.UP: None,
            Direction.RIGHT: None,
            Direction.DOWN: None
        }

    def late_init(self):
        self.background = self.display.get_entity(BACKGROUND_ID)
        self.player = self.display.get_entity(PLAYER_ID)

        surface_pos = (0, 0, WIDTH, HEIGHT)
        pygame.draw.rect(self.entity_surface, COLOUR, surface_pos)

        self.pos_x = self.background.pos_x + self.background.bounds.width
        self.pos_y = self.background.pos_y + self.background.bounds.height

        self.bounds = (self.pos_x - WIDTH / 2, self.pos_y - HEIGHT / 2, WIDTH, HEIGHT)

    def pre_draw(self, delta_time):
        if delta_time == 0:
            return

        self.angle += (ANGLE_ROTATE_MULTIPLIER * delta_time) % 360

        self.blocked = self.bounds_check(self.pos_x, self.pos_y, delta_time)

        self.move(delta_time)
        self.check_player_collision()
        
    def bounds_check(self, x, y, delta_time):
        d = {
            Direction.RIGHT: self.bounds_check_individual(x, y, Direction.RIGHT, delta_time),
            Direction.UP: self.bounds_check_individual(x, y, Direction.UP, delta_time),
            Direction.LEFT: self.bounds_check_individual(x, y, Direction.LEFT, delta_time),
            Direction.DOWN: self.bounds_check_individual(x, y, Direction.DOWN, delta_time),
        }
        
        return d

    def bounds_check_individual(self, x, y, direction, delta_time):
        total_speed = (MOVE_OFFSET + self.speed) * delta_time

        x_diff = 0
        y_diff = 0
        if direction == Direction.RIGHT:
            x_diff = total_speed
        elif direction == Direction.LEFT:
            x_diff = -total_speed
        elif direction == Direction.DOWN:
            y_diff = total_speed
        elif direction == Direction.UP:
            y_diff = -total_speed

        return self.valid_pos(x + x_diff, y + y_diff)

    def move(self, delta_time):
        pos = self.blocked[self.current_direction]

        if not pos:
            new_pos = self.background.get_closest_vertex((self.pos_x, self.pos_y))
            bounds_check = self.bounds_check(new_pos[0], new_pos[1], delta_time)

            all_directions = []
            for key in Direction.all_keys():
                if key == self.current_direction or key == Direction.opposite(self.current_direction):
                    continue
                
                if not bounds_check[key]:
                    continue

                all_directions.append(key)
            
            direction = all_directions[randint(0, len(all_directions) - 1)]

            self.current_direction = direction
            self.pos_x = new_pos[0]
            self.pos_y = new_pos[1]
        else:
            self.pos_x = pos[0]
            self.pos_y = pos[1]

    def valid_pos(self, new_pos_x, new_pos_y):
        current_pos = (self.pos_x, self.pos_y)
        pos_to_save = self.background.get_sparc_location(new_pos_x, new_pos_y)

        if not pos_to_save:
            return None

        if points_are_equal(current_pos, pos_to_save):
            return None

        return pos_to_save

    def check_player_collision(self):
        max_side = max(WIDTH, HEIGHT)

        rect = pygame.Rect(self.pos_x - max_side / 2, self.pos_y - max_side / 2, max_side, max_side)
        player_bounds = pygame.Rect(self.player.bounds)

        if rect.colliderect(player_bounds):
            self.player.handle_sparc_damage()

    def draw(self):
        pos = (self.pos_x, self.pos_y)
        origin_pos = (WIDTH / 2, HEIGHT / 2)

        rotate_surface(self.surface, self.entity_surface, pos, origin_pos, self.angle)
