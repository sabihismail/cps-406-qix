import pygame
from base.entity import Entity, Direction

WIDTH = 20.0
HEIGHT = WIDTH
MOVE_OFFSET_X = 200.0
MOVE_OFFSET_Y = MOVE_OFFSET_X
COLOR = (255, 0, 0)

class Qix(Entity):
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
