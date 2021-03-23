from entity import Entity

class Player(Entity):
    def draw(self):
        self.surface.fill((255,0,0), (200,200,200,100))
