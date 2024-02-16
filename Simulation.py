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


    def iteration(self, speed=1):
        speed = speed / 8 #Default speed factor is 1/8

        atoms_out = copy.copy(self.atoms)

        for atom in atoms_out:
            #Temperature
            if atom.temperature > 0:
                if random.randint(0,math.ceil(100 / speed)) <= atom.temperature:
                    atom.temperature -= 1 / atom.mass
                    self.photons += [Photon.Photon(atom.x, atom.y)]

            #Gravitation
            for grav_atom in self.atoms:
                distance = utils.distance(atom.x, atom.y, grav_atom.x, grav_atom.y)

                #Prevent atoms from overlapping
                if distance <= atom.radius + grav_atom.radius:
                    continue

                f_grav = (atom.mass * grav_atom.mass) / (distance * distance)

                a_grav = f_grav / atom.mass

                #Separate x and y components of acceleration
                total_distance = abs(grav_atom.x - atom.x) + abs(grav_atom.y - atom.y)
                x_component = (grav_atom.x - atom.x) / total_distance
                y_component = (grav_atom.y - atom.y) / total_distance

                atom.vx += x_component * a_grav * speed
                atom.vy += y_component * a_grav * speed

            #Momentum (Impuls)
            atom.x += atom.vx * speed
            atom.y += atom.vy * speed

            #Elastic collisions between atoms (conservation of momentum and energy)
            for test_atom in atoms_out:
                if atom == test_atom:
                    continue

                distance = utils.distance(atom.x, atom.y, test_atom.x, test_atom.y)

                if distance <= (atom.radius + test_atom.radius):
                    atom.x -= atom.vx * speed
                    atom.y -= atom.vy * speed
                    test_atom.x -= test_atom.vx * speed
                    test_atom.y -= test_atom.vy * speed

                    masses = atom.mass + test_atom.mass

                    atom_vx_new = (atom.vx * atom.mass + test_atom.mass * (2 * test_atom.vx - atom.vx)) / masses
                    atom_vy_new = (atom.vy * atom.mass + test_atom.mass * (2 * test_atom.vy - atom.vy)) / masses

                    test_atom.vx = (test_atom.mass * test_atom.vx + atom.mass * (2 * atom.vx - test_atom.vx)) / masses
                    test_atom.vy = (test_atom.mass * test_atom.vy + atom.mass * (2 * atom.vy - test_atom.vy)) / masses

                    atom.vx = atom_vx_new
                    atom.vy = atom_vy_new

            #World borders
            if self.has_border:
                if atom.x - atom.radius < self.world_border[0]:
                    atom.x = self.world_border[0] + atom.radius
                    atom.vx = -atom.vx
                if atom.x + atom.radius > self.world_border[2]:
                    atom.x = self.world_border[2] - atom.radius
                    atom.vx = -atom.vx
                if atom.y - atom.radius < self.world_border[1]:
                    atom.y = self.world_border[1] + atom.radius
                    atom.vy = -atom.vy
                if atom.y + atom.radius > self.world_border[3]:
                    atom.y = self.world_border[3] - atom.radius
                    atom.vy = -atom.vy

                for p in range(len(self.photons) - 1, -1, -1): #Delete photons exiting the world border
                    if self.photons[p].x < self.world_border[0] or self.photons[p].x > self.world_border[2]:
                        del self.photons[p]
                    elif self.photons[p].y < self.world_border[1] or self.photons[p].y > self.world_border[3]:
                        del self.photons[p]


        for photon in self.photons:
            photon.x += photon.vx * speed
            photon.y += photon.vy * speed

        self.atoms = atoms_out
