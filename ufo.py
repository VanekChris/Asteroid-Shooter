import pygame
from ufo_laser import UfoLaser
pygame.mixer.init()

class EnemyUfo(pygame.sprite.Sprite):

    def __init__(self, x, y, size):
        super().__init__()
        self.images = []
        for num in range(1, 5):
            img = pygame.image.load(f"Assets/UFO_{num}_Enlarged.png")
            if size == 1:
                img = pygame.transform.scale(img, (40, 20))
            if size == 2:
                img = pygame.transform.scale(img, (60, 40))
            if size == 3:
                img = pygame.transform.scale(img, (80, 60))
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0
        self.speed = 5
        self.move_sideways = False
        self.laser_group = pygame.sprite.Group()
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 1000
        self.destroyed = False
        self.health = 10
        # self.laser_sound = pygame.mixer.Sound("Assets/laser1.mp3")
        # self.laser_sound.set_volume(0.5)

    def update(self):
        self.move()
        if self.destroyed:
            return
        rotate_speed = 7
        self.counter += 1
        if self.counter >= rotate_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        if self.index >= len(self.images) - 1 and self.counter >= rotate_speed:
            self.index = 0
            self.counter = 0
            self.image = self.images[self.index]

        self.laser_group.update()
        for laser in self.laser_group:
            laser.rect.y += 5
            if laser.rect.bottom <= 0:
                laser.kill()

    def move(self):
        if self.destroyed:
            return

        if not self.move_sideways:
            self.rect.y += 1
            if self.rect.y >= 100:
                self.rect.y = 100
                self.move_sideways = True
        else:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_shot >= self.shoot_delay:
                self.shoot()
                self.last_shot = current_time

            self.rect.x += self.speed
            if self.rect.left <= 0 or self.rect.right >= 450:
                self.speed = -self.speed

    def shoot(self):
        laser = UfoLaser()
        laser.rect.x = self.rect.centerx
        laser.rect.y = self.rect.bottom
        self.laser_group.add(laser)

    def hit(self):
        self.destroyed = True
        self.laser_group.empty()