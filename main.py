import pygame
import numpy as np
import random
from game import Game
from tiles import Tile

class Main():

    allowed_keys = [1073741903,
                    1073741904, 
                    1073741905, 
                    1073741906, 
                    1073741912, 
                    13, 
                    27, 
                    32]


    def __init__(self, fps=30) -> None:

        #fonctionnement de l'interface
        pygame.init()           
        self.clock = pygame.time.Clock()
        self.FPS = fps

        pygame.display.set_caption("2048")
        self.screen = pygame.display.set_mode((620,800))
        self.background = pygame.image.load('assets/grid.jpg')
        self.background = pygame.transform.scale(self.background, (620, 800))

        #fonctionnement du jeu
        self.game = Game(main=self)  
        self.running = True

        #2048
        self.font2048 = pygame.font.Font('assets/Fonts/ClearSans-Bold.ttf', 100)
        self.text2048 = self.font2048.render('2048', 1, (232, 218, 203))
        self.text2048_rect = self.text2048.get_rect()
        self.text2048_rect.center = (160,160)


        #bouton play
        self.play_button = pygame.image.load('assets/start-button.png')
        self.play_button = pygame.transform.scale(self.play_button, (300,300))
        self.play_button_rect = self.play_button.get_rect()
        self.play_button_rect.center = (300,500)       

        #game over
        self.game_over = pygame.image.load('assets/game-over.png')
        self.game_over = pygame.transform.scale(self.game_over, (500,500))
        self.game_over_rect = self.play_button.get_rect()
        self.game_over_rect.center = (210,150)        
        
        #boucle principale
        self.run_program()


    def run_program(self):
        
        while self.running:

            if not self.game.game_started and not self.game.game_lost:      
                self.screen.blit(self.background, (0, 0))          
                self.screen.blit(self.play_button, self.play_button_rect.topleft)
                self.screen.blit(self.text2048, self.text2048_rect)
            elif self.game.game_lost:
                self.screen.blit(self.game_over, self.game_over_rect.topleft)
                self.screen.blit(self.play_button, self.play_button_rect.topleft)
                self.game.render_final_score()
            else:
                self.screen.blit(self.background, (0, 0))
                self.screen.blit(self.text2048, self.text2048_rect)
                self.game.update()            
      
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.game.score_manager.save_score(self.game.score)
                elif event.type == pygame.KEYDOWN:
                    if event.key in self.allowed_keys:
                        self.game.pressed[event.key] = True
                elif event.type == pygame.KEYUP:
                    if event.key in self.allowed_keys:
                        self.game.moved_once = False
                        self.game.pressed[event.key] = False
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.game.game_started:
                    if self.play_button_rect.collidepoint(event.pos):
                        self.game.start()

            pygame.display.flip()

            self.clock.tick(self.FPS)

        pygame.quit()


if __name__ == '__main__':
    Main(fps = 120)
