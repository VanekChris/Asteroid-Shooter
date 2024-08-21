import pygame

class MenuIcon(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("Assets/ship.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)