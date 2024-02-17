import copy
import math
import random
import utils

import Atom, Photon

class Simulation:
    def __init__(self, world_border = [-30, -30, 30, 30], fusion_threshold = 10):
        self.atoms = []
        self.photons = []

        self.fusion_threshold = fusion_threshold

        self.has_border = world_border != []
        self.world_border = world_border

    def clear_all(self):
        self.atoms = []
        self.photons = []
        self.structures = []

    def init_random_atoms(self, count=20):
        self.clear_all()

        min_x = self.world_border[0] + 1 if self.has_border else 0
        min_y = self.world_border[1] + 1 if self.has_border else 0
        max_x = self.world_border[2] - 1 if self.has_border else 3 * round(math.sqrt(count))
        max_y = self.world_border[3] - 1 if self.has_border else 3 * round(math.sqrt(count))

        for n_atom in range(count):
            x_coord = random.randint(min_x, max_x)
            y_coord = random.randint(min_y, max_y)
            temperature = random.choice([0,5,10,20])
            self.atoms += [Atom.Atom(x_coord, y_coord, temperature=temperature)]


    def iteration(self, speed=1):
        speed = speed / 8 #Default speed factor is 1/8

        atoms_out = copy.copy(self.atoms)

        for atom in atoms_out:
            #Atoms that have been fusioned and will be deleted at the end of this iteration
            if atom.mass == 0: continue

            #Temperature
            if atom.temperature >= 1:
                atom.vx += 0.25 * speed * atom.temperature * (random.random() - 0.5) / atom.mass
                atom.vy += 0.25 * speed * atom.temperature * (random.random() - 0.5) / atom.mass
                if random.randint(0,math.ceil(100 / speed)) <= atom.temperature:
                    atom.temperature -= 1 / atom.mass
                    self.photons += [Photon.Photon(atom.x, atom.y)]

            #Interactions between atoms
            for grav_atom in self.atoms:
                if atom == grav_atom or grav_atom.mass == 0: continue

                distance = utils.distance(atom.x, atom.y, grav_atom.x, grav_atom.y)

                #Interactions on collision
                if distance <= atom.radius + grav_atom.radius:
                    #Nuclear fusion
                    if atom.temperature >= self.fusion_threshold * atom.mass and grav_atom.temperature >= self.fusion_threshold * grav_atom.mass:
                        atom.mass += grav_atom.mass
                        atom.temperature = (atom.temperature + grav_atom.temperature) / 2

                        atom.vx = (atom.vx + grav_atom.vx) / 2
                        atom.vy = (atom.vy + grav_atom.vy) / 2

                        atom.update_radius()

                        grav_atom.mass = 0
                        grav_atom.temperature = 0

                    #Elastic collisions between atoms (conservation of momentum and energy)
                    else:
                        atom.x -= atom.vx * speed
                        atom.y -= atom.vy * speed
                        grav_atom.x -= grav_atom.vx * speed
                        grav_atom.y -= grav_atom.vy * speed

                        masses = atom.mass + grav_atom.mass

                        atom_vx_new = (atom.vx * atom.mass + grav_atom.mass * (2 * grav_atom.vx - atom.vx)) / masses
                        atom_vy_new = (atom.vy * atom.mass + grav_atom.mass * (2 * grav_atom.vy - atom.vy)) / masses

                        grav_atom.vx = (grav_atom.mass * grav_atom.vx + atom.mass * (2 * atom.vx - grav_atom.vx)) / masses
                        grav_atom.vy = (grav_atom.mass * grav_atom.vy + atom.mass * (2 * atom.vy - grav_atom.vy)) / masses

                        atom.vx = atom_vx_new
                        atom.vy = atom_vy_new

                        if atom.temperature > grav_atom.temperature + 1:
                            atom.temperature -= 1
                            grav_atom.temperature += 1
                        elif atom.temperature + 1 < grav_atom.temperature:
                            atom.temperature += 1
                            grav_atom.temperature -= 1

                #Gravitation
                else:
                    f_grav = (atom.mass * grav_atom.mass) / (distance * distance)

                    a_grav = f_grav / atom.mass

                    #Separate x and y components of acceleration
                    total_distance = abs(grav_atom.x - atom.x) + abs(grav_atom.y - atom.y)
                    x_component = (grav_atom.x - atom.x) / total_distance
                    y_component = (grav_atom.y - atom.y) / total_distance

                    atom.vx += x_component * a_grav * speed
                    atom.vy += y_component * a_grav * speed

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

        for n_atom in range(len(atoms_out)-1, -1, -1):
            if atoms_out[n_atom].mass == 0:
                del atoms_out[n_atom]
                continue
            atoms_out[n_atom].x += atoms_out[n_atom].vx * speed
            atoms_out[n_atom].y += atoms_out[n_atom].vy * speed

        for photon in self.photons:
            photon.x += photon.vx * speed
            photon.y += photon.vy * speed

        self.atoms = atoms_out
