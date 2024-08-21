import pygame

class PlayerBullet(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Assets/bullet.jpg").convert_alpha()
        self.rect = self.image.get_rect()
        self.vel_y = -5
        self.vel_x = 0
