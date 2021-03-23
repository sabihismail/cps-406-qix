from entity import Entity

class Display():
    def __init__(self, surface):
        self.surface = surface
        self.entities: [Entity] = []

    def clear(self):
        self.surface.fill((0, 0, 0))

    def draw(self):
        self.entities.sort(key=lambda x: x.heirarchy)

        for entity in self.entities:
            entity.draw()

    def handle_event(self, event, key_pressed, delta_time):
        self.entities.sort(key=lambda x: x.heirarchy)

        for entity in self.entities:
            entity.handle_event(event, key_pressed, delta_time)

    def add_entity(self, entity):
        entity.surface = self.surface

        self.entities.append(entity)
