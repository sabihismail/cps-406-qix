import pygame
from display import Display
from player import Player

FIELD_X = 500
FIELD_Y = FIELD_X

class Main():
    def __init__(self):
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.player = Player('Player', 1)
        self.delta_time = 0

    def start(self):
        pygame.init()

        self.surface = pygame.display.set_mode((FIELD_X, FIELD_Y))

        self.display = Display(self.surface)
        self.display.add_entity(self.player)

        self.clock.tick(self.fps)
        while True:
            event = pygame.event.poll()

            if event.type == pygame.QUIT:
                break

            key_pressed = pygame.key.get_pressed()

            self.display.handle_event(event, key_pressed, self.delta_time)
            self.display.clear() # clear everything before redraw
            self.display.draw() # redraw new scene

            pygame.display.flip()

            self.delta_time = self.clock.tick(self.fps) / 1000.0

        pygame.quit()

m = Main()
m.start()
