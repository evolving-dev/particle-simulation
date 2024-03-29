import math

class Atom:
    def __init__(self, x, y, mass = 1, temperature = 0):
        self.x = x
        self.y = y

        self.vx = 0
        self.vy = 0

        self.mass = mass
        self.radius = math.sqrt(self.mass) / 2

        self.temperature = temperature

    def update_radius(self):
        self.radius = math.sqrt(self.mass) / 2
