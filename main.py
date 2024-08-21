import pygame
import random
import sys

from menu import MenuScreen
from game import Game
from stars import FallingStars
from ship import PlayerShip
from player_bullet import PlayerBullet
from text import DrawText
from icon import MenuIcon
from asteroid import FallingAsteroids
from particle_spawn import ParticleSpawn
from ufo import EnemyUfo

pygame.init()
pygame.mixer.init()

WIDTH = 450
HEIGHT = 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
STAR_COUNT = 25
MAX_ASTEROIDS = 5
EXTRA_LIFE = 1000
ASTEROID_SCORE = 500
UFO_SPAWN = 60000 
small_asteroids_images = FallingAsteroids.load_images("Assets/Asteroids/small")

pygame.display.set_caption("Astroid Shooter")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)

bg_music = "Assets/music.mp3"
pygame.mixer.music.load(bg_music)
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)  
game_start = pygame.mixer.Sound("Assets/game-start.mp3")
game_start.set_volume(0.5)

score = 0
lives = 3
next_life = EXTRA_LIFE
asteroid_speed = 1
game_over = False
run = True

stars = [FallingStars(SCREEN, random.randint(1, 4), random.randint(1, 4)) for _ in range(STAR_COUNT)]
player = PlayerShip(WIDTH // 2, HEIGHT - 50)
icon = MenuIcon(WIDTH // 3 - player.rect.width, HEIGHT // 3 + 5)
icon2 = MenuIcon(115, 210)
icon_group = pygame.sprite.Group()
icon_group.add(icon)
icon2_group = pygame.sprite.Group()
icon2_group.add(icon2)
sprite_group = pygame.sprite.Group()
sprite_group.add(player)
particle_spawner = ParticleSpawn()
ufo_group = pygame.sprite.Group()
asteroid_group = pygame.sprite.Group()

def initialize_asteroids():
    for _ in range(MAX_ASTEROIDS):
        spawn_asteroids()

def spawn_asteroids():
    x = random.randint(20, WIDTH - 20)
    y = random.randint(-100, -10)
    asteroid = FallingAsteroids(x, y)
    asteroid.speed_slow += asteroid_speed
    asteroid.speed_fast += asteroid_speed
    asteroid.speed = random.randint(asteroid.speed_slow, asteroid.speed_fast)
    asteroid_group.add(asteroid)

def spawn_ufo():
    x = random.randint(50, WIDTH - 50)
    y = -100
    size = 3
    new_ufo = EnemyUfo(x, y, size)
    ufo_group.add(new_ufo)

def menu_screen():
    global run

    initial_x, initial_y = 93, 195

    icon2.rect.x = initial_x
    icon2.rect.y = initial_y

    while run:
        SCREEN.fill("black")

        DrawText("HOW TO PLAY", "white", 40, WIDTH // 3, HEIGHT // 3, 200, 20, SCREEN)
        DrawText("ASTEROID", "white", 40, WIDTH // 3, 50, 50, 50, SCREEN)
        DrawText("SHOOTER", "white", 40, WIDTH // 3, 100, 50, 50, SCREEN)
        DrawText("QUIT", "white", 40, WIDTH // 2.3, HEIGHT // 2.5, 200, 20, SCREEN)
        DrawText("PLAY GAME", "white", 40, WIDTH // 3, HEIGHT // 4, 300, 20, SCREEN)
        
        icon2_group.draw(SCREEN)
        icon2_group.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if icon2.rect.x == 93 and icon2.rect.y == 195:
                    if event.key == pygame.K_RETURN:
                        game_start.play()
                        return
                    elif event.key == pygame.K_DOWN:
                        icon2.rect.x = 94
                        icon2.rect.y = 260
                    elif event.key == pygame.K_UP:
                        icon2.rect.x = 125
                        icon2.rect.y = 310

                elif icon2.rect.x == 94 and icon2.rect.y == 260:
                    if event.key == pygame.K_RETURN:
                        game_start.play()
                        pass
                    elif event.key == pygame.K_UP:
                        icon2.rect.x = 93
                        icon2.rect.y = 195
                    elif event.key == pygame.K_DOWN:
                        icon2.rect.x = 125
                        icon2.rect.y = 310

                elif icon2.rect.x == 125 and icon2.rect.y == 310:
                    if event.key == pygame.K_RETURN:
                        run = False
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_UP:
                        icon2.rect.x = 94
                        icon2.rect.y = 260
                    elif event.key == pygame.K_DOWN:
                        icon2.rect.x = 93
                        icon2.rect.y = 195

        pygame.display.update()
        clock.tick(60)

def game_over_screen():
    global score, lives, run, game_over

    while run:
        SCREEN.fill("black")
        DrawText("GAME OVER", "white", 40, WIDTH // 3, HEIGHT // 4, 300, 20, SCREEN)
        DrawText("PLAY AGAIN", "white", 40, WIDTH // 3, HEIGHT // 3, 200, 20, SCREEN)
        DrawText("QUIT", "white", 40, WIDTH // 2.3, HEIGHT // 2.5, 200, 20, SCREEN)
        
        icon_group.draw(SCREEN)
        icon_group.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN and icon.rect.y == 256 and icon.rect.x == 83:
                    icon.rect.x = 128
                    icon.rect.y = 311  

                if event.key == pygame.K_UP and icon.rect.x == 128 and icon.rect.y == 311:
                    icon.rect.x = 83
                    icon.rect.y = 256   

                if icon.rect.x == 128 and event.key == pygame.K_RETURN:
                    run = False
                    pygame.quit()
                    sys.exit()
            
                if icon.rect.x == 83 and event.key == pygame.K_RETURN:
                    lives = 3
                    score = 0
                    game_over = False
                    main()     

        pygame.display.update()
        clock.tick(60)      

def main():
    global run, score, lives, game_over, next_life, asteroid_speed, ASTEROID_SCORE

    initialize_asteroids()
    
    current_time = pygame.time.get_ticks()
    ufo_time = pygame.time.get_ticks()
    
    while run:
        menu_screen()

        while run and not game_over:
            SCREEN.fill("black")
            DrawText(f"SCORE: {score}", "white", 40, 20, 20, 200, 20, SCREEN)
            DrawText(f"LIVES: {lives}", "white", 40, 300, 20, 300, 20, SCREEN)

            if score >= next_life:
                lives += 1
                next_life += EXTRA_LIFE

            if score >= ASTEROID_SCORE:
                asteroid_speed += 1
                ASTEROID_SCORE += 500
                    
            for star in stars:
                star.draw(SCREEN)
                star.update()

            if lives <= 0:
                game_over = True
                game_over_screen()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        player.shoot()

            sprite_group.draw(SCREEN)
            player.bullet_group.draw(SCREEN)
            ufo_group.draw(SCREEN)
            asteroid_group.draw(SCREEN) 
            particle_spawner.particle_group.draw(SCREEN)

            player.move()
            
            sprite_group.update()
            player.update()
            ufo_group.update()
            asteroid_group.update()
            particle_spawner.update()
            
            current_time = pygame.time.get_ticks()
            if current_time - ufo_time >= UFO_SPAWN:
                spawn_ufo()
                ufo_time = current_time

            for ufo in ufo_group:
                ufo.laser_group.draw(SCREEN)
                ufo.laser_group.update()
                ufo.move()

            for bullet in player.bullet_group:
                collided_asteroids = pygame.sprite.spritecollide(bullet, asteroid_group, True)
                for asteroid in collided_asteroids:
                    particle_spawner.spawn_particles((bullet.rect.x, bullet.rect.y))
                    bullet.kill()
                    score += 10
                    
                    if len(asteroid_group) < MAX_ASTEROIDS:
                        for _ in range(5):
                            spawn_asteroids()
           
                ufo_collide = pygame.sprite.spritecollide(bullet, ufo_group, False)
                for ufo in ufo_collide:
                    ufo.health -= 1
                    bullet.kill()
                    if ufo.health <= 0:
                        ufo.kill()
                        lives += 1
            
            for ufo in ufo_group:
                for ufo_laser in ufo.laser_group:
                    laser_collide = pygame.sprite.spritecollide(ufo_laser, sprite_group, False)
                    if laser_collide:
                        lives -= 1
                        ufo_laser.kill()

            if pygame.sprite.spritecollide(player, asteroid_group, True):
                lives -= 1
            
            pygame.display.update()
            clock.tick(60)

        game_over = False

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()