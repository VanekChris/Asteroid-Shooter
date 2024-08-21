import pygame
import random
import os

class FallingAsteroids(pygame.sprite.Sprite):
    image_directory = "Assets/Asteroids/"

    def __init__(self, x, y, speed_slow=1, speed_fast=3):
        super().__init__()
        self.x = x
        self.y = y
        self.speed_slow = speed_slow
        self.speed_fast = speed_fast
        self.speed = random.randint(self.speed_slow, self.speed_fast)
        self.image = self.load_images()
        self.rect = self.image.get_rect(center=(x, y))

    def load_images(self):
        num = random.randint(1, 6)
        images = [pygame.image.load(f"{self.image_directory}/small{num}.png") for _ in range(7)]
        return random.choice(images)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > 800:
            self.rect.y = random.randint(-100, 10)
            self.rect.x = random.randint(0, 450)