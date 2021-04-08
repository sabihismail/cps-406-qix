import pygame
from engine.display import Display
from entities.player import Player
from entities.background import Background
from entities.qix import Qix
from util.constants import *

WINDOW_X = 1000
WINDOW_Y = WINDOW_X

class Main():
    def __init__(self):
        self.fps = FPS
        self.clock = pygame.time.Clock()
        self.delta_time = 0

        self.player = Player(PLAYER_ID)
        self.background = Background(BACKGROUND_ID)

    def start(self):
        pygame.init()

        self.surface = pygame.display.set_mode((WINDOW_X, WINDOW_Y))

        self.display = Display(self.surface)
        self.display.add_entity(self.player, self.background)

        self.clock.tick(self.fps)
        while True:
            event = pygame.event.poll()

            if event.type == pygame.QUIT:
                break

            key_pressed = pygame.key.get_pressed()

            self.display.handle_event(event, key_pressed)
            self.display.clear() # clear everything before redraw
            self.display.draw(self.delta_time) # redraw new scene

            pygame.display.flip()

            self.delta_time = self.clock.tick(self.fps) / 1000.0

        pygame.quit()

if __name__ == '__main__':
    m = Main()
    m.start()
