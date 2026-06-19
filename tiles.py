import pygame
import numpy as np

class Tile(pygame.sprite.Sprite):
    
    def __init__(self, surface, game) -> None:
        super().__init__()

        #interface
        self.screen = surface
        self.game = game

        #paramètres des tuiles
        self.tile_size = 110
        self.grid_width_x = 18.5
        self.grid_width_y = 14.5

        self.tile_coordinates = {}
        self.get_tile_coordinates()
        
        self.tile_sprites = {}
        self.load_sprites()

    
    def get_tile_coordinates(self):
        origin = np.array([62.5, 255])   #point d'origine haut gauche de la grille
        offset_h = np.array([self.tile_size + self.grid_width_x, 0])
        offset_v = np.array([0, self.tile_size + self.grid_width_y])

        for i in range(4):
            for j in range(4):
                tile_position = origin + i * offset_v + j * offset_h
                self.tile_coordinates[f"({i},{j})"] = tile_position

    def load_sprites(self):
        for i in range(1, 21, 1):
            image = pygame.image.load(f"assets/Tiles/{2**i}.png")
            self.tile_sprites[2**i] = pygame.transform.scale(image, (self.tile_size, self.tile_size))

