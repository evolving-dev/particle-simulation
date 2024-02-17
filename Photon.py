import math
import random

class Photon:
    def __init__(self, x, y, speed_factor = 1):
        speed_factor = 4 * speed_factor #Default speed factor: 4

        self.x = x
        self.y = y

        self.vx = (random.random() - 0.5) * speed_factor * 2
        self.vy = random.choice([-1, 1]) * math.sqrt(speed_factor ** 2 - self.vx ** 2) #Ensures equal speeds for all photons
