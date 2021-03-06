import pygame
from base.entity import Entity

class Display():
    def __init__(self, surface):
        self.surface = surface
        self.entities: [Entity] = []
        self.entity_dict = {}
        self.dynamic_entity_dict = {}

    def clear(self):
        self.surface.fill((0, 0, 0))

    def draw(self, delta_time):
        self.sort_entities(self.entities)
        for entity in self.entities:
            entity.pre_draw(delta_time)
            entity.draw()
        self.entities[1].pre_draw(delta_time)
        self.entities[1].draw()

    def handle_event(self, event, key_pressed):
        self.sort_entities(self.entities)

        for entity in self.entities:
            entity.handle_event(event, key_pressed)

    def sort_entities(self, lst):
        lst.sort(key=lambda x: x.heirarchy)

    def add_entity(self, *entities, dynamic=True):
        lst = list(entities)

        self.sort_entities(lst)

        for entity in lst:
            entity.surface = self.surface
            entity.display = self
            entity.late_init()

            self.entities.append(entity)
            self.entity_dict[entity.unique_id] = entity

            if dynamic:
                dynamic_entities = self.dynamic_entity_dict.get(entity.unique_id, [])
                dynamic_entities.append(entity)

                self.dynamic_entity_dict[entity.unique_id] = dynamic_entities

    def get_entity(self, identifier):
        return self.entity_dict[identifier]

    def get_dynamic_entities(self, identifier):
        return self.dynamic_entity_dict[identifier]
