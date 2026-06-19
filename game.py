import pygame, numpy as np, random
from puzzle import Puzzle2048
from tiles import Tile
import sqlite3
import time
from score_manager import ScoreManager

class Game():
    def __init__(self, main) -> None:
        self.main = main
        self.pressed = {}
        self.game_started = False
        self.game_lost = False
        self.moved_once = False

        #scores
        self.score = 0
        self.score_manager = ScoreManager()
        self.best_score = 0
        if self.best_score is None:
            self.best_score = 0

        #jeu
        self.puzzle = None
        self.tiles = Tile(surface=self.main.screen, game=self)
        self.font = pygame.font.Font("assets/Fonts/ClearSans-Medium.ttf", 16)
        self.final_font = pygame.font.Font("assets/Fonts/ClearSans-Bold.ttf", 50)


    def start(self):
        self.puzzle = Puzzle2048(self)
        self.score = 0
        self.best_score = self.score_manager.find_best_score()
        if self.best_score is None:
            self.best_score = 0
        self.game_started = True
        self.game_lost = False
        

    def update(self):
        #appui les touches
        if self.pressed.get(pygame.K_LEFT):
            self.puzzle.move('to_left')
        elif self.pressed.get(pygame.K_RIGHT):
            self.puzzle.move('to_right')
        elif self.pressed.get(pygame.K_UP):
            self.puzzle.move('to_up')
        elif self.pressed.get(pygame.K_DOWN):
            self.puzzle.move('to_down')

        self.apply_tiles()
        self.render_scores()


    def apply_tiles(self):
        for i in range(self.puzzle.grid.shape[0]):
            for j in range(self.puzzle.grid.shape[0]):
                value = int(self.puzzle.grid[i,j])
                if value > 0:
                    image = self.tiles.tile_sprites[value]
                    self.main.screen.blit(image, self.tiles.tile_coordinates[f"({i},{j})"])


    def render_scores(self):
        score_text = self.font.render(str(int(self.score)), 1, (236, 228, 221))
        score_text_rect = score_text.get_rect()
        score_text_rect.center = (403.5, 87)
        self.main.screen.blit(score_text, score_text_rect.topleft)

        best_score_text = self.font.render(str(int(self.best_score)), 1, (236, 228, 221))
        best_score_text_rect = best_score_text.get_rect()
        best_score_text_rect.center = (515, 87)
        self.main.screen.blit(best_score_text, best_score_text_rect.topleft)      


    def render_final_score(self):
        string_text = self.final_font.render("Score:", 1, (255,255,255))
        string_text_rect = string_text.get_rect()
        string_text_rect.center = (312, 500)
        self.main.screen.blit(string_text, string_text_rect.topleft)

        score_text = self.final_font.render(str(int(self.score)), 1, (255,255,255))
        score_text_rect = score_text.get_rect()
        score_text_rect.center = (312, 550)
        self.main.screen.blit(score_text, score_text_rect.topleft)


    def game_over(self):
        self.puzzle.grid = np.zeros((4,4))
        self.main.play_button_rect.center = (300,700)
        self.game_started = False
        self.game_lost = True
        self.score_manager.save_score(self.score)  




    
