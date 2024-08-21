import pygame
import random

class Particle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.w = random.randrange(1, 6)
        self.h = self.w
        self.size = (self.w, self.h)
        self.image = pygame.Surface(self.size)
        self.color = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.kill_timer = 60
        self.vel_x = random.randrange(-16, 16)
        self.vel_y = random.randrange(-16, 16)

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        if self.kill_timer == 0:
            self.kill()
        else:
            self.kill_timer -= 1