class Entity():
    def __init__(self, unique_id, heirarchy):
        self.unique_id = unique_id
        self.heirarchy = heirarchy
        self.surface = None

    def draw(self):
        raise NotImplementedError()
