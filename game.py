import pygame
import random
import sys
from ship import PlayerShip
from asteroid import FallingAsteroids
from ufo import EnemyUfo
from particle_spawn import ParticleSpawn
from text import DrawText
from stars import FallingStars
from high_score import read_high_score, write_high_score
from game_over import GameOverScreen

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.width, self.height = screen.get_size()
        self.running = True
        self.score = 0
        self.highScore = read_high_score()
        self.lives = 3
        self.next_life = 1000
        self.asteroid_score = 1000
        self.asteroid_speed_slow = 1
        self.asteroid_speed_fast = 3
        self.max_asteroids = 5
        self.game_over = False
        self.stars = [FallingStars(self.screen, random.randint(1, 4), random.randint(1, 4)) for _ in range(10)]

        self.player = PlayerShip(self.width // 2, self.height - 50)
        self.sprite_group = pygame.sprite.Group(self.player)
        self.asteroid_group = pygame.sprite.Group()
        self.ufo_group = pygame.sprite.Group()
        self.particle_spawner = ParticleSpawn()

        self.spawn_asteroids(self.max_asteroids)
        self.ufo_spawn_interval = 60000  # 60 seconds
        self.last_ufo_spawn_time = pygame.time.get_ticks()

    def spawn_asteroids(self, count):
        for _ in range(count):
            x = random.randint(0, self.width)
            y = random.randint(-100, -10)
            asteroid = FallingAsteroids(x, y, self.asteroid_speed_slow, self.asteroid_speed_fast)
            self.asteroid_group.add(asteroid)

    def spawn_ufo(self):
        x = random.randint(50, self.width - 50)
        y = -100
        size = 3
        new_ufo = EnemyUfo(x, y, size)
        self.ufo_group.add(new_ufo)

    def handle_events(self):
        self.player.move()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.shoot()

    def update(self):
        current_time = pygame.time.get_ticks()

        if self.score >= self.next_life:
            self.lives += 1
            self.next_life += 1000

        if self.score >= self.asteroid_score:
            self.asteroid_speed_slow += 1
            self.asteroid_speed_fast += 1
            self.asteroid_score += 1000
            for asteroid in self.asteroid_group:
                asteroid.speed = random.randint(self.asteroid_speed_slow, self.asteroid_speed_fast)

        if self.lives <= 0:
            write_high_score(self.highScore)
            self.game_over = True

        if current_time - self.last_ufo_spawn_time >= self.ufo_spawn_interval:
            self.spawn_ufo()
            self.last_ufo_spawn_time = current_time

        self.sprite_group.update()
        self.asteroid_group.update()
        self.ufo_group.update()
        self.particle_spawner.update()

        for star in self.stars:
            star.update()

        self.check_collisions()

        if self.score > self.highScore:
            self.highScore = self.score

    def check_collisions(self):
        for bullet in self.player.bullet_group:
            collided_asteroids = pygame.sprite.spritecollide(bullet, self.asteroid_group, True)
            for asteroid in collided_asteroids:
                self.particle_spawner.spawn_particles((bullet.rect.x, bullet.rect.y))
                bullet.kill()
                self.score += 10
                if len(self.asteroid_group) < self.max_asteroids:
                    self.spawn_asteroids(1)

            collided_ufos = pygame.sprite.spritecollide(bullet, self.ufo_group, False)
            for ufo in collided_ufos:
                ufo.health -= 1
                bullet.kill()
                if ufo.health <= 0:
                    ufo.kill()
                    self.score += 50

        for ufo in self.ufo_group:
            for laser in ufo.laser_group:
                if pygame.sprite.spritecollide(laser, self.sprite_group, False):
                    laser.kill()
                    self.lives -= 1

        if pygame.sprite.spritecollide(self.player, self.asteroid_group, True):
            self.lives -= 1
            if len(self.asteroid_group) < self.max_asteroids:
                self.spawn_asteroids(1)

    def render(self):
        self.screen.fill("black")
        for star in self.stars:
            star.draw(self.screen)

        DrawText(f"HIGH SCORE: {self.highScore}", "white", 30, 20, 20, 200, 20, self.screen)
        DrawText(f"SCORE: {self.score}", "white", 30, 20, 50, 200, 20, self.screen)
        DrawText(f"LIVES: {self.lives}", "white", 30, 350, 20, 200, 20, self.screen)
        self.sprite_group.draw(self.screen)
        self.player.bullet_group.draw(self.screen)
        self.asteroid_group.draw(self.screen)
        self.ufo_group.draw(self.screen)
        for ufo in self.ufo_group:
            ufo.laser_group.draw(self.screen)
        self.particle_spawner.particle_group.draw(self.screen)

    def game_over_screen(self):
        game_over_screen_f = GameOverScreen(self.screen, self.clock, self.width, self.height, self.restart_game)
        game_over_screen_f.show()

    def restart_game(self):
        self.lives = 3
        self.score = 0
        self.asteroid_speed_slow = 1
        self.asteroid_speed_fast = 3
        self.asteroid_score = 1000
        self.game_over = False
        self.run_game()

    def run_game(self):
        while self.running:
            self.handle_events()
            if not self.game_over:
                self.update()
                self.render()
            else:
                # Handle game over logic or transition to game over screen
                write_high_score(self.highScore)
                self.game_over_screen()  # This should be replaced with a transition
            pygame.display.update()
            self.clock.tick(60)

# Usage Example
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((450, 800))
    game = Game(screen)
    game.run_game()