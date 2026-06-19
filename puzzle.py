import pygame, numpy as np, random

class Puzzle2048():
    def __init__(self, game) -> None:
        self.grid = np.zeros((4, 4))

        self.game = game
        self.game_is_over = False

        self.add_new_tile()
        self.add_new_tile()


    def add_new_tile(self):
        grid_mask = self.grid != 0     
        while 1:
            cell = (random.randint(0,3), random.randint(0,3))
            if not grid_mask[cell]:            
                self.grid[cell] = 2
                break


    def move(self, direction):        
        if self.game.moved_once == False:
            if self.check_if_can_move(direction):         
                self.move_if_zero(direction)                      
                self.add_tiles(direction)
                self.move_if_zero(direction)
                self.add_new_tile() 
                if self.check_if_over():
                    self.game.game_over()
                else:
                    self.game.moved_once = True



    def add_tiles(self, direction):
        #détection de l'impossibilité du mouvement
        if direction == 'to_left':
            for row in range(self.grid.shape[0]):
                value_set = self.grid[row]

                for i in range(value_set.shape[0]):
                    for j in range(i+1, value_set.shape[0]):
                        if value_set[i] == value_set[j]:
                            value_set[i] += value_set[j]
                            self.game.score += value_set[j]*2
                            value_set[j] = 0

                self.grid[row] = value_set

        elif direction == 'to_right':
            for row in range(self.grid.shape[0]):
                value_set = self.grid[row]

                for i in range(value_set.shape[0]-1, -1, -1):
                    for j in range(i-1, -1, -1):
                        if value_set[i] == value_set[j]:
                            value_set[i] += value_set[j]
                            self.game.score += value_set[j]*2
                            value_set[j] = 0

                self.grid[row] = value_set
            
        elif  direction == 'to_down':
            for col in range(self.grid.shape[0]):
                value_set = self.grid[:,col]

                for i in range(value_set.shape[0]-1, -1, -1):
                    for j in range(i-1, -1, -1):
                        if value_set[i] == value_set[j]:
                            value_set[i] += value_set[j]
                            self.game.score += value_set[j]*2
                            value_set[j] = 0

                self.grid[:,col] = value_set

        elif direction == 'to_up':
            for col in range(self.grid.shape[0]):
                value_set = self.grid[:,col]

                for i in range(value_set.shape[0]):
                    for j in range(i+1, value_set.shape[0]):
                        if value_set[i] == value_set[j]:
                            value_set[i] += value_set[j]
                            self.game.score += value_set[j]*2
                            value_set[j] = 0

                self.grid[:,col] = value_set


    def move_if_zero(self, direction):
        for i in range(self.grid.shape[0]):          
            if direction == 'to_up':
                non_zero_values = self.grid[:, i][self.grid[:, i] != 0]
                zeros_to_add = self.grid.shape[0] - len(non_zero_values)
                self.grid[:, i] = np.concatenate((non_zero_values, np.zeros(zeros_to_add)))

            elif direction == 'to_left':
                non_zero_values = self.grid[i, :][self.grid[i, :] != 0]
                zeros_to_add = self.grid.shape[0] - len(non_zero_values)
                self.grid[i, :] = np.concatenate((non_zero_values, np.zeros(zeros_to_add)))

            if direction == 'to_down':
                non_zero_values = self.grid[:, i][self.grid[:, i] != 0]
                zeros_to_add = self.grid.shape[0] - len(non_zero_values)
                self.grid[:, i] = np.concatenate((np.zeros(zeros_to_add), non_zero_values))

            elif direction == 'to_right':
                non_zero_values = self.grid[i, :][self.grid[i, :] != 0]
                zeros_to_add = self.grid.shape[0] - len(non_zero_values)
                self.grid[i, :] = np.concatenate((np.zeros(zeros_to_add), non_zero_values))


    def check_if_can_move(self, direction):
        if direction == "to_left":
            for row in range(self.grid.shape[0]):
                sub_grid = self.grid[row]

                # Vérifier si deux cellules adjacentes peuvent fusionner
                for i in range(sub_grid.shape[0] - 1):
                    if sub_grid[i] == sub_grid[i+1] and sub_grid[i] != 0:
                        return True

                # Vérifier s'il existe un zéro avant une valeur non nulle (déplacement possible)
                for i in range(sub_grid.shape[0] - 1):
                    if sub_grid[i] == 0 and sub_grid[i+1] != 0:
                        return True

        elif direction == "to_right":
            for row in range(self.grid.shape[0]):
                sub_grid = self.grid[row]

                # Vérifier si deux cellules adjacentes peuvent fusionner (dans l'autre sens)
                for i in range(sub_grid.shape[0] - 1, 0, -1):
                    if sub_grid[i] == sub_grid[i-1] and sub_grid[i] != 0:
                        return True

                # Vérifier s'il existe un zéro après une valeur non nulle (déplacement possible)
                for i in range(sub_grid.shape[0] - 1, 0, -1):
                    if sub_grid[i] == 0 and sub_grid[i-1] != 0:
                        return True

        elif direction == "to_up":
            for col in range(self.grid.shape[1]):
                sub_grid = self.grid[:, col]  # Prendre les colonnes (utiliser la syntaxe numpy pour slice une colonne)

                # Vérifier si deux cellules adjacentes peuvent fusionner verticalement
                for i in range(sub_grid.shape[0] - 1):
                    if sub_grid[i] == sub_grid[i+1] and sub_grid[i] != 0:
                        return True

                # Vérifier s'il existe un zéro avant une valeur non nulle (déplacement possible vers le haut)
                for i in range(sub_grid.shape[0] - 1):
                    if sub_grid[i] == 0 and sub_grid[i+1] != 0:
                        return True

        elif direction == "to_down":
            for col in range(self.grid.shape[1]):
                sub_grid = self.grid[:, col]  # Prendre les colonnes (utiliser la syntaxe numpy pour slice une colonne)

                # Vérifier si deux cellules adjacentes peuvent fusionner verticalement (dans l'autre sens)
                for i in range(sub_grid.shape[0] - 1, 0, -1):
                    if sub_grid[i] == sub_grid[i-1] and sub_grid[i] != 0:
                        return True

                # Vérifier s'il existe un zéro après une valeur non nulle (déplacement possible vers le bas)
                for i in range(sub_grid.shape[0] - 1, 0, -1):
                    if sub_grid[i] == 0 and sub_grid[i-1] != 0:
                        return True
    

        return False
    

    def check_if_over(self):
        if np.all(self.grid != 0):
            for row in range(self.grid.shape[0]):
                for col in range(self.grid.shape[0]-1):                
                    if self.grid[row,col] == self.grid[row,col+1]:
                        return False
            for col in range(self.grid.shape[0]):
                for row in range(self.grid.shape[0]-1):                
                    if self.grid[row,col] == self.grid[row+1,col]:
                        return False                
            return True   
        return False     



    



        
