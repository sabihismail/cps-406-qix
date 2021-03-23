from enum import Enum

class Entity():
    def __init__(self, unique_id, heirarchy):
        self.unique_id = unique_id
        self.heirarchy = heirarchy
        self.surface = None

    def handle_event(self, event, key_pressed, delta_time):
        pass

    def draw(self):
        raise NotImplementedError()

class Direction(Enum):
    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3
