import random

class Photon:
    def __init__(self, x, y, speed_factor = 1):
        speed_factor = 8 * speed_factor #Default speed factor: 8

        self.x = x
        self.y = y

        self.vx = (random.random() - 0.5) * speed_factor
        self.vy = (random.random() - 0.5) * speed_factor
