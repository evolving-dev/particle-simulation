import pygame
import time, os

from ast import literal_eval

import Camera, Simulation, SimulationRenderer

def readfile(name):
    with open(name,"rb") as f:
        return f.read().decode("utf-8")

dimensions = [1280,720]
target_fps = 60
current_screen = "simulation"
open = True

pygame.init()
screen = pygame.display.set_mode(dimensions)

clock = pygame.time.Clock()
pygame.display.set_caption("Teilchensimulation")


cam = Camera.Camera()
renderer = SimulationRenderer.Renderer(dimensions, "font/PTSans-Regular.ttf")
simulation = Simulation.Simulation()
simulation.init_random_atoms()

dt = 0
global_speed = 1
t = time.time()

simulation_running = False

while open:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            open = False

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 4:
                cam.z += 0.1 if cam.z < 10 else 0
            elif event.button == 5:
                cam.z -= 0.1 if cam.z >= 0.2 else 0

        elif event.type == pygame.KEYDOWN:
            if current_screen == "simulation":
                if event.key == pygame.K_SPACE:
                    simulation_running = not simulation_running


    if current_screen == "simulation":
        cam.update(pygame.key.get_pressed(), dt)

        if simulation_running:
            simulation.iteration()
        renderer.render_world(screen, cam)
        renderer.render_simulation(screen, cam, simulation)
        renderer.render_fps_counter(screen, round(clock.get_fps(), 1))


    pygame.display.flip()

    clock.tick(target_fps)

    dt = time.time() - t
    t = time.time()

pygame.quit()