import pygame
from display import Display
from player import Player

FIELD_X = 500
FIELD_Y = FIELD_X

def main():
    pygame.init()

    surface = pygame.display.set_mode((FIELD_X, FIELD_Y))

    player = Player('Player', 1)

    display = Display(surface)
    display.add_entity(player)

    while True:
        event = pygame.event.poll()

        if event.type == pygame.QUIT:
            break

        display.clear() # clear everything before redraw
        display.draw() # redraw new scene

        pygame.display.flip()

    pygame.quit()

main()
