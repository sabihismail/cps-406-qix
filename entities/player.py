import pygame
from base.entity import Entity, Direction
from util.constants import BACKGROUND_ID
from .background import OUTLINE_COLOR as BACKGROUND_COLOUR

WIDTH = 20.0
HEIGHT = WIDTH
MOVE_OFFSET_X = 200.0
MOVE_OFFSET_Y = MOVE_OFFSET_X
COLOR = (255, 0, 0)

class Player(Entity):
    def __init__(self, unique_id):
        super().__init__(unique_id, width=WIDTH, height=HEIGHT, pos_x=0.0, pos_y=0.0)
        self.background = None
        self.display = None
        self.current_colour = None
        self.blocked = {
            Direction.LEFT: None,
            Direction.UP: None,
            Direction.RIGHT: None,
            Direction.DOWN: None
        }

    def late_init(self):
        self.background = self.display.get_entity(BACKGROUND_ID)

        self.pos_x = self.background.pos_x
        self.pos_y = self.background.pos_y

    def handle_event(self, event, key_pressed):
        if key_pressed[pygame.K_LEFT] or key_pressed[pygame.K_a]:
            self.move(Direction.LEFT)
        elif key_pressed[pygame.K_RIGHT] or key_pressed[pygame.K_d]:
            self.move(Direction.RIGHT)
        elif key_pressed[pygame.K_UP] or key_pressed[pygame.K_w]:
            self.move(Direction.UP)
        elif key_pressed[pygame.K_DOWN] or key_pressed[pygame.K_s]:
            self.move(Direction.DOWN)

    def pre_draw(self, delta_time):
        self.blocked[Direction.RIGHT] = self.valid_pos(self.pos_x + (MOVE_OFFSET_X * delta_time), self.pos_y, self.pos_x, self.pos_y)
        self.blocked[Direction.LEFT] = self.valid_pos(self.pos_x - (MOVE_OFFSET_X * delta_time), self.pos_y, self.pos_x, self.pos_y)
        self.blocked[Direction.UP] = self.valid_pos(self.pos_x, self.pos_y - (MOVE_OFFSET_Y * delta_time), self.pos_x, self.pos_y)
        self.blocked[Direction.DOWN] = self.valid_pos(self.pos_x, self.pos_y + (MOVE_OFFSET_Y * delta_time), self.pos_x, self.pos_y)

    def draw(self):
        pos = (self.pos_x - WIDTH / 2, self.pos_y - HEIGHT / 2, WIDTH, HEIGHT)
        self.surface.fill(COLOR, pos)

    def valid_pos(self, new_pos_x, new_pos_y, old_pos_x, old_pos_y):
        pos_to_save = self.background.leaves_play_area(new_pos_x, new_pos_y, old_pos_x, old_pos_y)

        return pos_to_save

    def move(self, direction):
        if self.blocked[direction]:
            val = self.blocked[direction]

            self.pos_x = val[0]
            self.pos_y = val[1]

            self.background.add_trail(self.pos_x, self.pos_y, direction)
