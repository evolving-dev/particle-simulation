import random

class Photon:
    def __init__(self, x, y, speed_factor = 0.25):
        self.x = x
        self.y = y

        self.vx = (random.random() - 0.5) * speed_factor
        self.vy = (random.random() - 0.5) * speed_factor
