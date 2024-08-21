import pygame
import sys
from menu import MenuScreen
from game import Game

pygame.init()
pygame.mixer.init()

WIDTH = 450
HEIGHT = 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroid Shooter")
clock = pygame.time.Clock()

bg_music = "Assets/music.mp3"
pygame.mixer.music.load(bg_music)
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)
game_start = pygame.mixer.Sound("Assets/game-start.mp3")
game_start.set_volume(0.5)

def main():
    
    while True:
        menu = MenuScreen(SCREEN, game_start)
        menu.run_menu()
        if not menu.run:
            game = Game(SCREEN)
            game.run_game()
        
        if menu.run == False and game.game_over:
            pygame.quit()
            sys.exit()

if __name__=="__main__":
    main()