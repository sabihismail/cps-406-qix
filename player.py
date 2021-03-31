import pygame
from entity import Entity, Direction
from constants import BACKGROUND_ID
from background import COLOR as BACKGROUND_COLOUR

WIDTH = 10.0
HEIGHT = WIDTH
MOVE_OFFSET_X = 100.0
MOVE_OFFSET_Y = MOVE_OFFSET_X
COLOR = (255, 255, 255)

class Player(Entity):
    def __init__(self, unique_id):
        super().__init__(unique_id, width=WIDTH, height=HEIGHT, pos_x=0.0, pos_y=0.0)
        self.display = None
        self.blocked = {
            Direction.LEFT: None,
            Direction.UP: None,
            Direction.RIGHT: None,
            Direction.DOWN: None
        }

    def late_init(self):
        self.background = self.display.get_entity(BACKGROUND_ID)

        self.pos_x = self.background.pos_x - (WIDTH / 2)
        self.pos_y = self.background.pos_y - (HEIGHT / 2)

    def handle_event(self, event, key_pressed):
        if key_pressed[pygame.K_LEFT]:
            self.move(Direction.LEFT)
        elif key_pressed[pygame.K_RIGHT]:
            self.move(Direction.RIGHT)
        elif key_pressed[pygame.K_UP]:
            self.move(Direction.UP)
        elif key_pressed[pygame.K_DOWN]:
            self.move(Direction.DOWN)

    def pre_draw(self, delta_time):
        self.blocked[Direction.RIGHT] = self.valid_pos(self.pos_x + (MOVE_OFFSET_X * delta_time), self.pos_y)
        self.blocked[Direction.LEFT] = self.valid_pos(self.pos_x - (MOVE_OFFSET_X * delta_time), self.pos_y)
        self.blocked[Direction.UP] = self.valid_pos(self.pos_x, self.pos_y - (MOVE_OFFSET_Y * delta_time))
        self.blocked[Direction.DOWN] = self.valid_pos(self.pos_x, self.pos_y + (MOVE_OFFSET_Y * delta_time))

    def draw(self):
        pos = (self.pos_x, self.pos_y, WIDTH, HEIGHT)

        self.surface.fill(COLOR, pos)

    def valid_pos(self, new_pos_x, new_pos_y):
        pix_x = new_pos_x + (WIDTH / 2)
        pix_y = new_pos_y + (HEIGHT / 2)

        pix = self.surface.get_at((int(pix_x), int(pix_y)))

        if pix != BACKGROUND_COLOUR:
            return None

        return (new_pos_x, new_pos_y)

    def move(self, direction):
        if self.blocked[direction]:
            val = self.blocked[direction]

            self.pos_x = val[0]
            self.pos_y = val[1]
