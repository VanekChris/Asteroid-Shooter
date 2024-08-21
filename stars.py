import pygame
import random

star_colors = ["white", "red", "orange", "yellow", "blue", "lightblue", "lightyellow"]

class FallingStars:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.x = random.randint(0, 450)
        self.y = random.randint(-100, 0)
        self.speed = random.randint(1, 25)
        self.color = (random.choice(star_colors))

    def update(self):
        self.y += self.speed
        if self.y >= 800:
            self.y = 0
            self.x = random.randint(0, 450)

    def draw(self, screen):
        pygame.draw.ellipse(screen, self.color, (self.x, self.y, self.width, self.height))