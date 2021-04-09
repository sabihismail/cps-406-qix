import pygame
from engine.level_manager import LevelManager
from util.constants import FPS

WINDOW_X = 1000
WINDOW_Y = WINDOW_X

class Main():
    def __init__(self):
        self.fps = FPS
        self.clock = pygame.time.Clock()
        self.delta_time = 0

        self.surface = None
        self.level_manager = None

    def start(self):
        pygame.init()

        self.surface = pygame.display.set_mode((WINDOW_X, WINDOW_Y))
        self.level_manager = LevelManager(self.surface)

        self.clock.tick(self.fps)
        while True:
            event = pygame.event.poll()

            if event.type == pygame.QUIT:
                break

            key_pressed = pygame.key.get_pressed()

            self.level_manager.loop(event, key_pressed, self.delta_time)

            pygame.display.flip()

            self.delta_time = self.clock.tick(self.fps) / 1000.0

        pygame.quit()

if __name__ == '__main__':
    m = Main()
    m.start()
