class camera2d:
    def __init__(self, x=0, y=0, zoom=1, rotation=0):
        self.x = x
        self.y = y
        self.zoom = zoom
        self.rotation = rotation
    def get_position(self):
        return (self.x, self.y)
    def set_position(self, pos):
        self.x, self.y = pos