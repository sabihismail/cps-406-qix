import pygame
import time
from base.entity import Entity, Direction
from util.constants import BACKGROUND_ID
from entities.background import Background

WIDTH = 20.0
HEIGHT = WIDTH
MOVE_OFFSET_X = 200.0
MOVE_OFFSET_Y = MOVE_OFFSET_X
COLOUR = (255, 0, 0)

class Player(Entity):
    def __init__(self, unique_id):
        super().__init__(unique_id, width=WIDTH, height=HEIGHT, pos_x=0.0, pos_y=0.0)
        self.pos_x = 0.0
        self.pos_y = 0.0
        self.bounds = None
        self.background = None
        self.display = None
        self.lives = 3
        self.font = pygame.font.SysFont('Arial',30)
        self.livesd = self.font.render('Lives: ' + str(self.lives), False, (255, 255, 255))
        self.invuln = 0
        self.blocked = {
            Direction.LEFT: None,
            Direction.UP: None,
            Direction.RIGHT: None,
            Direction.DOWN: None
        }

    def late_init(self):
        self.background = self.display.get_entity(BACKGROUND_ID)

        self.pos_x = self.background.pos_x
        self.pos_y = self.background.pos_y

        self.bounds = (self.pos_x - WIDTH / 2, self.pos_y - HEIGHT / 2, WIDTH, HEIGHT)

    def handle_event(self, _, key_pressed):
        print(self.lives, self.invuln)
        if self.invuln > 0:
            self.invuln -= 1
        if key_pressed[pygame.K_LEFT] or key_pressed[pygame.K_a]:
            self.move(Direction.LEFT)
        elif key_pressed[pygame.K_RIGHT] or key_pressed[pygame.K_d]:
            self.move(Direction.RIGHT)
        elif key_pressed[pygame.K_UP] or key_pressed[pygame.K_w]:
            self.move(Direction.UP)
        elif key_pressed[pygame.K_DOWN] or key_pressed[pygame.K_s]:
            self.move(Direction.DOWN)

    def pre_draw(self, delta_time):
        self.blocked[Direction.RIGHT] = self.valid_pos(self.pos_x + (MOVE_OFFSET_X * delta_time), self.pos_y, self.pos_x, self.pos_y)
        self.blocked[Direction.LEFT] = self.valid_pos(self.pos_x - (MOVE_OFFSET_X * delta_time), self.pos_y, self.pos_x, self.pos_y)
        self.blocked[Direction.UP] = self.valid_pos(self.pos_x, self.pos_y - (MOVE_OFFSET_Y * delta_time), self.pos_x, self.pos_y)
        self.blocked[Direction.DOWN] = self.valid_pos(self.pos_x, self.pos_y + (MOVE_OFFSET_Y * delta_time), self.pos_x, self.pos_y)

    def draw(self):
        self.surface.fill(COLOUR, self.bounds)

    def valid_pos(self, new_pos_x, new_pos_y, old_pos_x, old_pos_y):
        pos_to_save = self.background.leaves_play_area(new_pos_x, new_pos_y)#, old_pos_x, old_pos_y)

        return pos_to_save

    def move(self, direction):
        if self.blocked[direction]:
            val = self.blocked[direction]

            self.pos_x = val[0]
            self.pos_y = val[1]
        
            self.bounds = (self.pos_x - WIDTH / 2, self.pos_y - HEIGHT / 2, WIDTH, HEIGHT)

            self.background.add_trail(self.pos_x, self.pos_y, direction)

    def handle_qix_damage(self):
        if not self.invuln > 0:
            self.lives -= 1
            self.invuln = 200
            self.livesd = self.font.render('Lives: ' + str(self.lives), False, (255, 255, 255))

    def handle_sparc_damage(self):
        if not self.invuln > 0:
            self.lives -= 1
            self.invuln = 200
            self.livesd = self.font.render('Lives: ' + str(self.lives), False, (255, 255, 255))
            
