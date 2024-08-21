import pygame
from player_bullet import PlayerBullet
pygame.mixer.init()

class PlayerShip(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("Assets/ship.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5
        self.bullet_group = pygame.sprite.Group()
        self.last_shot = pygame.time.get_ticks()
        self.laser_sound = pygame.mixer.Sound("Assets/laser1.mp3")
        self.laser_sound.set_volume(0.5)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= 800:
            self.rect.bottom = 800
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= 450:
            self.rect.right = 450

    def shoot(self):
        bullet = PlayerBullet()
        bullet.rect.x = self.rect.centerx
        bullet.rect.y = self.rect.top
        self.bullet_group.add(bullet)
        self.laser_sound.play()

    def update(self):
        self.bullet_group.update()
        for bullet in self.bullet_group:
            bullet.rect.y -= 5
            if bullet.rect.bottom <= 0:
                bullet.kill()

    def stop(self):
        self.speed = 0