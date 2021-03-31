from enum import Enum
from constants import ENTITY_HEIRARCHY

class Entity():
    def __init__(self, unique_id, width=0, height=0, pos_x=0.0, pos_y=0.0):
        self.unique_id = unique_id
        self.heirarchy = self.identify_hierarchical_order(unique_id)
        self.surface = None
        self.width = width
        self.height = height
        self.pos_x = pos_x
        self.pos_y = pos_y

    def identify_hierarchical_order(self, identifier):
        for i, value in enumerate(ENTITY_HEIRARCHY):
            if value == identifier:
                return i

        return 1000

    def late_init(self):
        pass

    def handle_event(self, event, key_pressed):
        pass

    def pre_draw(self, delta_time):
        pass

    def draw(self):
        raise NotImplementedError()

    def __str__(self):
        return "ID: " + self.unique_id + ", Heirarchy: " + str(self.heirarchy)

class Direction(Enum):
    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3
