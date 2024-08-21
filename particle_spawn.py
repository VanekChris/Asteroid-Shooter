import pygame
from particle import Particle
import random

class ParticleSpawn:
    def __init__(self):
        self.particle_group = pygame.sprite.Group()

    def update(self):
        self.particle_group.update()

    def spawn_particles(self, pos):
        random_num = random.randrange(3, 30)
        for num in range(random_num):
            num = Particle()
            num.rect.x = pos[0]
            num.rect.y = pos[1]
            self.particle_group.add(num)