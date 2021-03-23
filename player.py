from entity import Entity

class Player(Entity):
    def draw(self):
        self.surface.fill((255,255,255), (10,10,10,10))
