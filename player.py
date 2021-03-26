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

    def late_init(self):
        self.background = self.display.get_entity(BACKGROUND_ID)

        self.pos_x = self.background.pos_x - (WIDTH / 2)
        self.pos_y = self.background.pos_y - (HEIGHT / 2)

    def handle_event(self, event, key_pressed, delta_time):
        if key_pressed[pygame.K_LEFT]:
            self.move(Direction.LEFT, delta_time)
        elif key_pressed[pygame.K_RIGHT]:
            self.move(Direction.RIGHT, delta_time)
        elif key_pressed[pygame.K_UP]:
            self.move(Direction.UP, delta_time)
        elif key_pressed[pygame.K_DOWN]:
            self.move(Direction.DOWN, delta_time)

    def draw(self):
        pos = (self.pos_x, self.pos_y, WIDTH, HEIGHT)

        self.surface.fill(COLOR, pos)

    def valid_pos(self, new_pos_x, new_pos_y):
        pix_x = new_pos_x + (WIDTH / 2)
        pix_y = new_pos_y + (HEIGHT / 2)

        pix = self.surface.get_at((int(pix_x), int(pix_y)))[:3]

        return not pix == BACKGROUND_COLOUR

    def move(self, direction, delta_time):
        new_pos_x = self.pos_x
        new_pos_y = self.pos_y

        if direction == Direction.LEFT:
            new_pos_x -= (MOVE_OFFSET_X * delta_time)
        elif direction == Direction.RIGHT:
            new_pos_x += (MOVE_OFFSET_X * delta_time)
        elif direction == Direction.UP:
            new_pos_y -= (MOVE_OFFSET_Y * delta_time)
        elif direction == Direction.DOWN:
            new_pos_y += (MOVE_OFFSET_Y * delta_time)
        else:
            raise Exception("Cannot move in this direction.")

        if self.valid_pos(new_pos_x, new_pos_y):
            self.pos_x = new_pos_x
            self.pos_y = new_pos_y
