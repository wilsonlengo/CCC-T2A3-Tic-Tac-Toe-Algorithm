import pygame
import os

letterX = pygame.image.load(os.path.join('img', 'x.png')) # Loading image of "X"
letterO = pygame.image.load(os.path.join('img', 'o.png')) # Loading imahe of "O"


class Grid:
    """Class to define the game-board functions and logic"""
    def __init__(self):
        """Constructor for the board"""
        self.grid_lines = [((0,200), (600,200)),  # first horizontal line
                           ((0,400), (600,400)),  # second horizontal line
                           ((200,0), (200,600)),  # first vertical line
                           ((400,0), (400,700))]  # second vertical line
        
        self.grid = [[0 for x in range(3)] for y in range(3)]
        self.switch_player = True
        # search directions:    |  N    |    NW   |    W   |   SW   |   S   |   SE   |   E   |   NE  |   
        self.search_direction = [(0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1)]
        self.game_over = False

        
    

    def draw(self, surface):
        """Function that draws the lines in grid"""
        for line in self.grid_lines:
            pygame.draw.line(surface, (200, 200, 200), line[0], line[1], 2)
        
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.get_cell_value(x, y) == "X":
                    surface.blit(letterX, (x*200, y*200))
                elif self.get_cell_value(x, y) == "O":
                    surface.blit(letterO, (x*200, y*200))
        

    def get_cell_value(self, x, y):
        """Getter for grid cells"""
        return self.grid[y][x]
    
    def set_cell_value(self, x, y, value):
        """Setter for the grid cells"""
        self.grid[y][x] = value

    def get_mouse(self, x, y, player):
        """Method to get mouse position of a player choice on grid"""
        if self.get_cell_value(x, y) == 0:
            self.set_cell_value(x, y, player)          
            self.grid_check(x, y, player)
        
        
    def is_within_bounds(self, x, y):
        """Checking if player choice is actually on the board"""
        return x >= 0 and x < 3 and y >= 0 and y < 3
    
    def grid_check(self, x, y, player):
        """Function that defines Tic-Tac-Toe game logic (3 in row = Win)"""
        count = 1
        for index, (dirx, diry) in enumerate(self.search_direction):
            if self.is_within_bounds(x+dirx, y+diry) and self.get_cell_value(x+dirx, y+diry) == player:
                count += 1
                xx = x + dirx
                yy = y + diry
                if self.is_within_bounds(xx+dirx, yy+diry) and self.get_cell_value(xx+dirx, yy+diry) == player:
                    count += 1
                    if count == 3:
                        break
                if count < 3:
                    new_direction = 0
                    # mapping indices to opposite directions: 0-4 1-5 2-6 3-7 4-0 5-1 6-2 7-3
                    if index == 0:
                        new_direction = self.search_direction[4] # N to S
                    elif index == 1:
                        new_direction = self.search_direction[5] # NW to SE
                    elif index == 2:
                        new_direction = self.search_direction[6] # W to E
                    elif index == 3:
                        new_direction = self.search_direction[7] # SW to NE
                    elif index == 4:
                        new_direction = self.search_direction[0] # S to N
                    elif index == 5:
                        new_direction = self.search_direction[1] # SE to NW
                    elif index == 6:
                        new_direction = self.search_direction[2] # E to W
                    elif index == 7:
                        new_direction = self.search_direction[3] # NE to SW
                    
                    if self.is_within_bounds(x + new_direction[0], y + new_direction[1]) \
                            and self.get_cell_value(x + new_direction[0], y + new_direction[1]) == player:
                        count += 1
                        if count == 3:
                            break
                    else:
                        count = 1
        # Determining the winner
        if count == 3:
            print(player, 'wins!')
            self.game_over = True
        else:
            self.game_over = self.full_grid()
    
    def full_grid(self):
        """Stops game if grid is full until either player resets"""
        for row in self.grid:
            for value in row:
                if value == 0:
                    return False
        return True
                    

    def reset_grid(self):
        """Resetting the game"""
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                self.set_cell_value(x, y, 0)  
            

    def print_grid(self):
        """Outputing the board"""
        for row in self.grid:
            print(row)