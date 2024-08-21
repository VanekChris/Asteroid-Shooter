import pygame, sys
from text import DrawText
from icon import MenuIcon
from game import Game

class MenuScreen:
    def __init__(self, screen, game_start_sound):
        self.screen = screen
        self.game_start_sound = game_start_sound
        self.run = True
        self.current_pos = 0
        self.pos_options = [(100, 100), (100, 200), (100, 300)]
        self.icon = MenuIcon(self.pos_options[self.current_pos][0] - 50, self.pos_options[self.current_pos][1])
        self.icon_group = pygame.sprite.Group()
        self.icon_group.add(self.icon)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.current_pos == 0:
                        self.game_start_sound.play()
                        self.run = False

                    elif self.current_pos == 1:
                        self.game_start_sound.play()
                        self.run = False
                        
                    elif self.current_pos == 2:
                        pygame.quit()
                        sys.exit()

                elif event.key == pygame.K_DOWN:
                    self.current_pos = (self.current_pos + 1) % len(self.pos_options)
                    self.update_icon_pos()

                elif event.key == pygame.K_UP:
                    self.current_pos = (self.current_pos - 1) % len(self.pos_options)
                    self.update_icon_pos()

    def update_icon_pos(self):
        x, y = self.pos_options[self.current_pos]
        self.icon.rect.x = x - 50
        self.icon.rect.y = y

    def draw(self):
        self.screen.fill("black")
        DrawText("HOW TO PLAY", "white", 40, 100, 100, 200, 20, self.screen)
        DrawText("PLAY GAME", "white", 40, 100, 200, 300, 20, self.screen)
        DrawText("QUIT", "white", 40, 100, 300, 200, 20, self.screen)
        self.icon_group.draw(self.screen)
        self.icon_group.update()

    def run_menu(self):
        while self.run:
            self.handle_events()
            self.draw()
            pygame.display.update()
