import pygame
import sys
from text import DrawText

class GameOverScreen:

    def __init__(self, screen, clock, width, height, restart_callback):
        self.screen = screen
        self.clock = clock
        self.width = width
        self.height = height
        self.restart_callback = restart_callback
        self.run = True

        self.icon_image = pygame.image.load("Assets/ship.png").convert_alpha()
        self.icon = pygame.sprite.Sprite()
        self.icon.image = self.icon_image
        self.icon.rect = self.icon.image.get_rect(x=83, y=256)
        self.icon_group = pygame.sprite.Group(self.icon)

    def show(self):
        while self.run:
            self.screen.fill("black")
            DrawText("GAME OVER", "white", 40, self.width // 3, self.height // 4, 300, 20, self.screen)
            DrawText("PLAY AGAIN", "white", 40, self.width // 3, self.height // 3, 200, 20, self.screen)
            DrawText("QUIT", "white", 40, self.width // 2.3, self.height // 2.5, 200, 20, self.screen)
        
            self.icon_group.draw(self.screen)
            self.icon_group.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN and self.icon.rect.y == 256 and self.icon.rect.x == 83:
                        self.icon.rect.x = 128
                        self.icon.rect.y = 311  

                    if event.key == pygame.K_UP and self.icon.rect.x == 128 and self.icon.rect.y == 311:
                        self.icon.rect.x = 83
                        self.icon.rect.y = 256   

                    if self.icon.rect.x == 128 and event.key == pygame.K_RETURN:
                        run = False
                        pygame.quit()
                        sys.exit()
                
                    if self.icon.rect.x == 83 and event.key == pygame.K_RETURN:
                        self.run = False
                        self.restart_callback()

            pygame.display.update()
            self.clock.tick(60)      