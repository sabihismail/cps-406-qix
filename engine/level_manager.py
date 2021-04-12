import pygame
from entities.player import Player
from entities.background import Background
from entities.qix import Qix
from entities.sparc import Sparc
from util.constants import PLAYER_ID, BACKGROUND_ID, QIX_ID, SPARC_ID
from .display import Display

PERCENTAGE_THRESHOLD = 60.0
QIX_SPEED_INTERVAL = 5.0
QIX_MOVE_CHANCE = 2
SPARC_SPEED_INTERVAL = 5.0

class LevelManager():
    def __init__(self, surface, levels):
        self.level = levels
        self.surface = surface
        self.complete = False

        self.background = None
        self.player = None
        self.qix = None
        self.sparcs = []

        self.configure_level()

    def configure_level(self):
        self.player = Player(PLAYER_ID)
        self.background = Background(BACKGROUND_ID)

        self.spawn_qix()
        self.spawn_sparc()

        self.display = Display(self.surface)
        
        self.display.add_entity(self.player, self.background, self.qix)
        for sparc in self.sparcs:
            self.display.add_entity(sparc, dynamic=True)

    def loop(self, event, key_pressed, delta_time):
        self.display.handle_event(event, key_pressed)
        self.display.clear()
        self.display.draw(delta_time)

        self.check_lives()

        self.check_level_complete()

    def spawn_qix(self):
        speed = QIX_SPEED_INTERVAL * self.level
        move_chance = QIX_MOVE_CHANCE * self.level

        self.qix = Qix(QIX_ID, speed=speed, move_chance=move_chance)

    def spawn_sparc(self):
        sparc_count = 1 if self.level < 3 else 2

        for _ in range(sparc_count):
            speed = SPARC_SPEED_INTERVAL * self.level

            sparc = Sparc(SPARC_ID, speed=speed)

            self.sparcs.append(sparc)

    def check_level_complete(self):
        if self.background.percentage*100 >= PERCENTAGE_THRESHOLD:
            self.complete = True
            self.player.lives = 0

    def check_lives(self):
        self.surface.blit(self.player.livesd, (200,100))
        a = pygame.font.SysFont('Arial',30)
        b = a.render('Level: ' + str(self.level), False, (255, 255, 255))
        self.surface.blit(b, (500,100))
