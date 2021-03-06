"""Conway's Game of Life

Written by Sam Hubbard - samlhub@gmail.com
"""

import os
from math import sin, cos, floor, ceil, pi
from time import sleep
from copy import deepcopy


HEADER = """
     /  /
    /  /
   /~~/   Conway's Game of Life
  /  /
    /~~~~\\
   /  /  /  Sam Hubbard
  /  /  /     - samlhub@gmail.com
"""

EMPTY  = u"\u2591" * 2
FILLED = u"\u2593" * 2
WALL   = u"\u2588"

PATTERN_GLIDER = [(2, 2), (2, 1), (2, 0), (1, 0), (0, 1)]
PATTERN_LWSS = [(1, 0), (4, 0), (0, 1), (0, 2), (4, 2), (0, 3), (1, 3),
    (2, 3), (3, 3)]
PATTERN_ACORN = [(1, 0), (3, 1), (0, 2), (1, 2), (4, 2), (5, 2), (6, 2)]
PATTERN_BLOCK = [(0, 0), (1, 0), (0, 1), (1, 1)]
PATTERN_QUEEN = [(4, 0), (2, 1), (4, 1), (1, 2), (3, 2), (0, 3), (3, 3),
    (1, 4), (3, 4), (2, 5), (4, 5), (4, 6)]


class Grid:
    """Stores and displays the playing grid."""
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.data = [[EMPTY]*width for x in range(height)]
        self.generation = 0

    def __getitem__(self, t):
        t = (t[0] % self.width, t[1] % self.height)
        return self.data[t[1]][t[0]]

    def __setitem__(self, t, value):
        t = (t[0] % self.width, t[1] % self.height)
        self.data[t[1]][t[0]] = value

    def __str__(self):
        out = WALL * (self.width * len(EMPTY) + 4) + "\n"
        for row in self.data:
            out += WALL * 2
            for item in row:
                out += str(item)
            out += WALL * 2 + "\n"
        out += WALL * (self.width * len(EMPTY) + 4)
        return out + "\n\n  GENERATION: " + str(self.generation)


def step(grid):
    """Steps the grid forward one iteration, using classic
       Conway Game of Life rules."""
    next = deepcopy(grid)
    next.generation += 1
    for i in range(grid.width):
        for j in range(grid.height):
            neighbours = 0
            for n in range(8):
                x = i + round_out(cos(n * pi / 4))
                y = j + round_out(sin(n * pi / 4))
                if grid[x, y] == FILLED:
                    neighbours += 1
            if grid[i, j] == FILLED:
                if not 1 < neighbours < 4:
                    next[i, j] = EMPTY
            elif neighbours == 3:
                next[i, j] = FILLED
    return next


def add_pattern(grid, pattern, x, y):
    """Adds a starting pattern to the grid at specified position.
       Patterns are lists containing offsets of filled cells."""
    for t in pattern:
        grid[x + t[0], y + t[1]] = FILLED


def int_input(prompt, error="Please input an integer:"):
    print(prompt, end=" ")
    while True:
        try:
            x = int(input())
            return x
        except:
            print(error, end=" ")


def round_out(n):
    """Rounds to the nearest integer away from zero."""
    # Forgive me oh Lord, for I have sinned.
    if abs(n) < 10**-10: n = 0
    
    if n != 0:
        return ceil(abs(n)) * int(n / abs(n))
    else:
        return 0


def get_settings():
    """Prompts the user to input settings."""
    class Settings:
        def __init__(self):
            self.width = int_input("Width of grid:")
            self.height = int_input("Height of grid:")
            self.timestep = int_input("Time-step (ms):")
    return Settings()


if __name__ == "__main__":
    print(HEADER)
    settings = get_settings()
    
    grid = Grid(settings.width, settings.height)
    add_pattern(grid, PATTERN_BLOCK, 5, 7)
    add_pattern(grid, PATTERN_BLOCK, 25, 7)
    add_pattern(grid, PATTERN_QUEEN, 10, 4)
    
    while True:
        os.system("cls")
        print(grid)
        sleep(settings.timestep / 1000)
        grid = step(grid)
