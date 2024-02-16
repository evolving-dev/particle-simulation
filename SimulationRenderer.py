import math
import pygame

class Renderer:
    def __init__(self, dimensions, font, pixels_per_tile = 40):
        self.scaling = pixels_per_tile
        self.width = dimensions[0]
        self.height = dimensions[1]

        self.font = font
        self.clicked_creature = False

    def mix_color(self, color1, color2, factor = 0.5):
        r = color1[0] * factor +  color2[0] * (1 - factor)
        g = color1[1] * factor +  color2[1] * (1 - factor)
        b = color1[2] * factor +  color2[2] * (1 - factor)

        return [r, g, b]

    def is_on_screen(self, coords, margin=0):
        on_screen_x = coords[0] + margin > 0 and coords[0] - margin < self.width
        on_screen_y = coords[1] + margin > 0 and coords[1] - margin < self.height

        return on_screen_x and on_screen_y

    def render_world(self, screen, camera):
        screen.fill([220,220,220])

        for x in range(math.ceil(self.height / (self.scaling * camera.z))):
            pygame.draw.line(screen, [180,180,180], [0, (x - (camera.y % 1)) * self.scaling * camera.z], [self.width,(x - (camera.y % 1)) * self.scaling * camera.z])

        for y in range(math.ceil(self.width / (self.scaling * camera.z))):
            pygame.draw.line(screen, [180,180,180], [(y - (camera.x % 1)) * self.scaling * camera.z, 0], [(y - (camera.x % 1)) * self.scaling * camera.z, self.height])


    def render_simulation(self, screen, camera, simulation):
        font = pygame.font.Font(self.font, round(camera.z * 40))

        if simulation.has_border:
            #Screen coordinates of borders
            border_neg_x = (simulation.world_border[0] - camera.x) * camera.z * self.scaling
            border_pos_x = (simulation.world_border[2] - camera.x) * camera.z * self.scaling
            border_neg_y = (simulation.world_border[1] - camera.y) * camera.z * self.scaling
            border_pos_y = (simulation.world_border[3] - camera.y) * camera.z * self.scaling

            if border_neg_x > 0: #Border -x
                pygame.draw.rect(screen, [0,0,0], [0, 0, border_neg_x, self.height])
            if border_neg_y > 0: #-y
                pygame.draw.rect(screen, [0,0,0], [0, 0, self.width, border_neg_y])

            if border_pos_x < self.width: #Border +x
                pygame.draw.rect(screen, [0,0,0], [border_pos_x, 0, self.width, self.height])
            if border_pos_y < self.height: #+y
                pygame.draw.rect(screen, [0,0,0], [0, border_pos_y, self.width, self.height])

        for atom in simulation.atoms:
            screen_x = (atom.x - camera.x) * camera.z * self.scaling
            screen_y = (atom.y - camera.y) * camera.z * self.scaling
            radius = (atom.mass ** 0.5) * camera.z * self.scaling
            if self.is_on_screen([screen_x, screen_y], margin=radius):
                pygame.draw.circle(screen, [50, 50, 50], center=[screen_x, screen_y], radius=radius)

        for photon in simulation.photons:
            screen_x = (photon.x - camera.x) * camera.z * self.scaling
            screen_y = (photon.y - camera.y) * camera.z * self.scaling
            radius = 0.25 * camera.z * self.scaling
            if self.is_on_screen([screen_x, screen_y], margin=radius):
                pygame.draw.circle(screen, [255, 200, 0], center=[screen_x, screen_y], radius=radius)


    def render_fps_counter(self, screen, fps):
        font = pygame.font.Font(self.font, self.height // 40)
        fps_text = font.render("FPS: " + str(fps), True, [128,128,128])
        screen.blit(fps_text, [0,0])
