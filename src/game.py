import random

import pygame
from tile import *


class MineSweeper():

    def __init__(self, width, height, num_bombs, display_info):

        self.width = width
        self.height = height
        self.num_bombs = num_bombs
        self.display_info = display_info
        self.over = False
        self.reveal = True

        # Init graphic grid
        self.graphic_grid = [[HIDDEN for _ in range(width)] for _ in range(height)]

        # Init logic grid
        self.logic_grid = [[EMPTY for _ in range(width)] for _ in range(height)]

        # Place bombs on logic grid
        self.bomb_positions = set(random.sample(
            [(i, j) for i in range(height) for j in range(width)], num_bombs))
        for i, j in self.bomb_positions:
            self.logic_grid[i][j] = BOMB

        # Calculate numbers
        for i in range(height):
            for j in range(width):
                if self.logic_grid[i][j] == BOMB:
                    continue
                counter = 0
                # Top
                if i > 0 and self.logic_grid[i-1][j] == BOMB:
                    counter += 1
                # Top Right
                if i > 0 and j < width - 1 and self.logic_grid[i-1][j+1] == BOMB:
                    counter += 1
                # Right
                if j < width - 1 and self.logic_grid[i][j+1] == BOMB:
                    counter += 1
                # Bottom Right
                if i < height - 1 and j < width - 1 and self.logic_grid[i+1][j+1] == BOMB:
                    counter += 1
                # Bottom
                if i < height - 1 and self.logic_grid[i+1][j] == BOMB:
                    counter += 1
                # Bottom Left
                if i < height - 1 and j > 0 and self.logic_grid[i+1][j-1] == BOMB:
                    counter += 1
                # Left
                if j > 0 and self.logic_grid[i][j-1] == BOMB:
                    counter += 1
                # Top Left
                if i > 0 and j > 0 and self.logic_grid[i-1][j-1] == BOMB:
                    counter += 1
                self.logic_grid[i][j] = counter

        self.flag_positions = []

        self.hidden_positions = [(i, j)
                                 for i in range(height) for j in range(width)]

        self.single_press = None
        
        self.pressed_positions = []

    def __is_valid(self, i, j):
        return 0 <= i < self.height and 0 <= j < self.width

    def __get_valid_neighbours(self, i, j):
        neighbouring_pos = [
            (i-1, j),   # Top
            (i-1, j+1),  # Top Right
            (i, j+1),   # Right
            (i+1, j+1),  # Bottom Right
            (i+1, j),   # Bottom
            (i+1, j-1),  # Bottom Left
            (i, j-1),   # Left
            (i-1, j-1),  # Top Left
        ]
        neighbours = []
        for k, l in neighbouring_pos:
            if self.__is_valid(k, l):
                neighbours.append((k, l))
        return neighbours

    def restart(self):
        self.__init__(self.width, self.height, self.num_bombs, self.display_info)

    def get(self, i, j):
        return self.graphic_grid[i][j]

    def set(self, i, j, val):
        if val == FLAG:
            self.flag_positions.append((i, j))
        elif val == HIDDEN:
            self.hidden_positions.append((i, j))
        if self.get(i, j) == FLAG:
            self.flag_positions.remove((i, j))
        elif self.get(i, j) == HIDDEN:
            self.hidden_positions.remove((i, j))
        
        self.graphic_grid[i][j] = val

    # Change graphic grid
    def reveal_tile(self, i, j):
        self.set(i, j, self.logic_grid[i][j])
        if self.get(i, j) == BOMB:
            self.lost_grid(i, j)

    def check_single_press(self):
        if self.single_press:
            i, j = self.single_press
            self.reveal_tile(i, j)
            if self.get(i, j) == EMPTY:
                self.empty_patch(i, j)
            self.single_press = None

    def empty_patch(self, i, j):

        # Get empty tiles patch with BFS
        queue = [(i, j)]
        visited = [(i, j)]
        other = []

        while queue:
            (i, j) = queue.pop(0)
            for neighbour in self.__get_valid_neighbours(i, j):
                if neighbour not in visited:
                    k, l = neighbour
                    if self.logic_grid[k][l] == EMPTY:
                        queue.append(neighbour)
                        visited.append(neighbour)
                    else:
                        if neighbour not in other:
                            other.append(neighbour)

        for (i, j) in visited + other:
            self.set(i, j, self.logic_grid[i][j])

    # True -> Over, False -> Ok
    def pressed_neighbours(self, i, j):
        # Get neighbours
        neighbours = self.__get_valid_neighbours(i, j)
        to_delete = []
        for k, l in neighbours:
            if self.get(k, l) not in [HIDDEN, FLAG]:
                to_delete.append((k, l))
        for k, l in to_delete:
            neighbours.remove((k, l))

        # Get hidden neighbours
        for k, l in neighbours:
            if self.get(k, l) == HIDDEN:
                self.pressed_positions.append((k, l))

        # Count number of flags around
        flag_count = 0
        for k, l in neighbours:
            if self.get(k, l) == FLAG:
                flag_count += 1

        # If no flags, do nothing
        if flag_count == 0:
            self.reveal = False
            return

        # If wrong number of flags, do nothing
        if flag_count != self.logic_grid[i][j]:
            self.reveal = False
            return

        # Else, reveal tiles
        for k, l in neighbours:
            if self.get(k, l) == FLAG:
                continue
            # If bomb hit, lose
            if self.logic_grid[k][l] == BOMB:
                self.lost_grid(k, l)
                return
            self.set(k, l, self.logic_grid[k][l])
            if self.get(k, l) == EMPTY:
                self.empty_patch(k, l)

    def reveal_pressed_neighours(self):
        if self.pressed_positions:
            for i, j in self.pressed_positions:
                if self.reveal:
                    self.over = self.reveal_tile(i, j)
                    if self.over:
                        self.lost_grid(i, j)
                else:
                    self.set(i, j, HIDDEN)
        self.pressed_positions = []
        self.reveal = True
    
    # Display lose grid
    def lost_grid(self, i, j):

        self.over = True
        
        # Bombs
        for row, col in self.bomb_positions:
            if self.get(row, col) == FLAG:
                continue
            self.set(row, col, BOMB)

        # Clicked Bomb
        self.set(i, j, BOMB_EXPLODED)

        # Wrong flags
        for row, col in self.flag_positions:
            if self.logic_grid[row][col] != BOMB:
                self.set(row, col, BOMB_CROSSED)
        
        self.update_display() 
        
    def update_display(self):
        for i in range(self.height):
            for j in range(self.width):
                self.display_info["screen"].blit(self.display_info["images"][self.get(i, j)], (j*self.display_info["tile_size"], i*self.display_info["tile_size"]))
        pygame.display.flip()
    
    def auto_finish(self):
        if set(self.hidden_positions).issubset(set(self.bomb_positions)):
            for i, j in self.hidden_positions:
                self.set(i, j, FLAG)

    def check_win(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.get(i, j) == HIDDEN:
                    return False
        return True
