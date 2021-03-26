import pygame
from entity import Entity

class Display():
    def __init__(self, surface):
        self.surface = surface
        self.entities: [Entity] = []
        self.entity_dict = {}

    def clear(self):
        self.surface.fill((0, 0, 0))

    def draw(self):
        self.sort_entities(self.entities)

        for entity in self.entities:
            entity.draw()

    def handle_event(self, event, key_pressed, delta_time):
        self.sort_entities(self.entities)

        for entity in self.entities:
            entity.handle_event(event, key_pressed, delta_time)

    def sort_entities(self, lst):
        lst.sort(key=lambda x: x.heirarchy)

    def add_entity(self, *entities):
        lst = list(entities)

        self.sort_entities(lst)

        for entity in lst:
            entity.surface = self.surface
            entity.display = self
            entity.late_init()

            self.entities.append(entity)
            self.entity_dict[entity.unique_id] = entity

    def get_entity(self, identifier):
        return self.entity_dict[identifier]
