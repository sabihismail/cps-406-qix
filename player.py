import pygame
from entity import Entity, Direction

WIDTH = 10.0
HEIGHT = WIDTH
MOVE_OFFSET_X = 100.0
MOVE_OFFSET_Y = MOVE_OFFSET_X

class Player(Entity):
    def __init__(self, unique_id, heirarchy):
        super().__init__(unique_id, heirarchy)
        self.pos_x = 0.0
        self.pos_y = 0.0

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

        self.surface.fill((255,255,255), pos)

    def move(self, direction, delta_time):
        if direction == Direction.LEFT:
            self.pos_x -= (MOVE_OFFSET_X * delta_time)
        elif direction == Direction.RIGHT:
            self.pos_x += (MOVE_OFFSET_X * delta_time)
        elif direction == Direction.UP:
            self.pos_y -= (MOVE_OFFSET_Y * delta_time)
        elif direction == Direction.DOWN:
            self.pos_y += (MOVE_OFFSET_Y * delta_time)
        else:
            raise Exception("Cannot move in this direction.")
