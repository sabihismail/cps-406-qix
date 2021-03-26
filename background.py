import pygame
from entity import Entity

WIDTH = 300.0
HEIGHT = WIDTH
COLOR = (100, 100, 100)

class Background(Entity):
    def __init__(self, unique_id):
        super().__init__(unique_id, width=WIDTH, height=HEIGHT, pos_x=0.0, pos_y=0.0)

    def late_init(self):
        display_width, display_height = self.surface.get_size()

        self.pos_x = (display_width - WIDTH) / 2
        self.pos_y = (display_height - HEIGHT) / 2

    def draw(self):
        pos = (self.pos_x, self.pos_y, WIDTH, HEIGHT)

        self.surface.fill(COLOR, pos)
