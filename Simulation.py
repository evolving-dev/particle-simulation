import copy
import math
import random
import utils

import Atom, Photon

class Simulation:
    def __init__(self, world_border = [-30, -30, 30, 30]):
        self.atoms = []
        self.photons = []

        self.has_border = world_border != []
        self.world_border = world_border

    def clear_all(self):
        self.atoms = []
        self.photons = []
        self.structures = []

    def init_random_atoms(self, count=20):
        self.clear_all()

        min_x = self.world_border[0] + 1 if self.has_border else -100
        min_y = self.world_border[1] + 1 if self.has_border else -100
        max_x = self.world_border[2] - 1 if self.has_border else 100
        max_y = self.world_border[3] - 1 if self.has_border else 100

        for n_atom in range(count):
            x_coord = random.randint(min_x, max_x)
            y_coord = random.randint(min_y, max_y)
            temperature = random.randint(0, 5)
            self.atoms += [Atom.Atom(x_coord, y_coord, temperature=temperature)]


    def iteration(self, speed=1, collision_prevention=True):
        if self.has_border: #Delete photons exiting the world border
            for p in range(len(self.photons) - 1, -1, -1):
                if self.photons[p].x < self.world_border[0] or self.photons[p].x > self.world_border[2]:
                    del self.photons[p]
                elif self.photons[p].y < self.world_border[1] or self.photons[p].y > self.world_border[3]:
                    del self.photons[p]

        atoms_out = copy.deepcopy(self.atoms)
        photons_out = copy.deepcopy(self.photons)

        for atom in atoms_out:
            #Temperature
            if atom.temperature > 0:
                atom.x += math.sin(atom.temp_movement_state) * speed * 0.125
                atom.y += math.cos(atom.temp_movement_state + 0.5) * speed * 0.125
                atom.temp_movement_state += random.randint(60,90)/100
                if atom.temp_movement_state > 6.29: #2*Pi
                    atom.temp_movement_state = 0
                if random.randint(0,100) <= atom.temperature:
                    atom.temperature -= 1 / atom.mass
                    photons_out += [Photon.Photon(atom.x, atom.y)]

            #Gravitation
            grav_vx = 0
            grav_vy = 0
            for grav_atom in self.atoms:
                distance = utils.distance(atom.x, atom.y, grav_atom.x, grav_atom.y)

                #Prevent atoms from overlapping
                if distance <= atom.radius + grav_atom.radius:
                    continue

                f_grav = (atom.mass * grav_atom.mass) / (distance ** 2)

                a_grav = f_grav / atom.mass

                #Separate x and y components of acceleration
                x_component = (grav_atom.x - atom.x) / (abs(grav_atom.x - atom.x) + abs(grav_atom.y - atom.y))
                y_component = (grav_atom.y - atom.y) / (abs(grav_atom.x - atom.x) + abs(grav_atom.y - atom.y))

                a_x = x_component * a_grav
                a_y = y_component * a_grav

                atom.x += a_x * speed
                atom.y += a_y * speed

                if collision_prevention:
                    for test_atom in atoms_out:
                        if atom == test_atom:
                            continue

                        distance = utils.distance(atom.x, atom.y, test_atom.x, test_atom.y)
                        iters = 0
                        while distance <= (atom.radius + test_atom.radius) and iters < 4:
                            iters += 1
                            if (a_x == 0 or a_y == 0):
                                break
                            atom.x -= a_x / 4
                            atom.y -= a_y / 4
                            distance = utils.distance(atom.x, atom.y, test_atom.x, test_atom.y)

            #Momentum (Impuls)
            atom.x += atom.vx * speed
            atom.y += atom.vy * speed

            #World borders
            if self.has_border:
                if atom.x - (atom.mass ** 0.5) < self.world_border[0]:
                    atom.x = self.world_border[0] + (atom.mass ** 0.5)
                if atom.x + (atom.mass ** 0.5) > self.world_border[2]:
                    atom.x = self.world_border[2] - (atom.mass ** 0.5)
                if atom.y - (atom.mass ** 0.5) < self.world_border[1]:
                    atom.y = self.world_border[1] + (atom.mass ** 0.5)
                if atom.y + (atom.mass ** 0.5) > self.world_border[3]:
                    atom.y = self.world_border[3] - (atom.mass ** 0.5)


        for photon in photons_out:
            photon.x += photon.vx * speed
            photon.y += photon.vy * speed

        self.atoms = atoms_out
        self.photons = photons_out
