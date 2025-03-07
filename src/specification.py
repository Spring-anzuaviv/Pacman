import pygame
import sys
import os
import math
#import tạm thời
import psutil
import time

#Window
WIDTH, HEIGHT = 1200, 850
APP_CAPTION = r"Pacman with Tom and Jerry"
GRID_SIZE = CELL_SIZE = 26  
PI = math.pi

#Map
#0: empty,  1: wall,    2: path,    3:power pellets  
#Small test case
map = [
    [1, 0, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1]
] 
boards1 = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,2,2,2,1,2,3,2,2,2,2,2,2,2,2,2,2,2,1,2,2,2,1],
    [1,2,1,2,1,2,1,1,1,1,1,2,1,1,1,1,1,2,1,2,1,2,1],
    [1,2,2,2,2,2,2,2,1,2,2,2,2,2,1,2,2,2,2,2,2,2,1],
    [1,1,1,2,1,2,1,2,1,2,1,1,1,2,1,2,1,2,1,2,1,1,1],
    [1,2,2,2,1,2,1,2,1,2,1,0,1,2,1,2,1,2,1,2,2,2,2],
    [1,2,1,2,1,2,1,2,1,2,1,1,1,2,1,2,1,2,1,2,1,2,1],
    [1,2,2,2,1,2,1,2,2,2,2,2,2,2,2,2,1,2,1,2,2,2,1],
    [1,1,1,1,1,2,1,2,1,1,1,1,1,1,1,2,1,2,1,1,1,1,1],
    [1,2,2,2,2,2,1,2,2,2,2,2,2,2,2,2,1,2,2,2,2,2,1],
    [1,2,1,1,1,1,1,2,1,1,1,2,1,1,1,2,1,1,1,1,1,2,1],
    [2,2,2,2,2,2,2,2,1,2,2,2,2,2,1,2,2,2,2,2,2,2,1],
    [1,2,1,1,1,1,1,2,1,1,1,1,1,1,1,2,1,1,1,1,1,2,1],
    [1,2,2,2,2,2,1,2,2,2,2,2,2,2,2,3,1,2,2,2,2,2,1],
    [1,1,1,1,1,2,1,2,1,1,1,1,1,1,1,2,1,2,1,1,1,1,1],
    [1,2,2,2,1,2,1,2,2,2,2,2,2,2,2,2,1,2,1,2,2,2,1],
    [1,2,1,2,1,2,1,2,1,2,1,1,1,2,1,2,1,2,1,2,1,2,1],
    [1,2,2,2,1,2,1,2,1,2,1,0,1,2,1,2,1,2,1,2,2,2,1],
    [1,1,1,2,1,2,1,2,1,2,1,1,1,2,1,2,1,2,1,2,1,1,1],
    [1,2,2,2,2,2,2,2,1,2,2,2,2,2,1,2,2,2,2,2,2,2,1],
    [1,2,1,2,1,2,1,1,1,1,1,2,1,1,1,1,1,2,1,2,1,2,1],
    [1,2,2,2,1,2,2,2,3,2,2,2,2,2,2,2,2,2,1,2,2,2,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

#29x33
boards2 = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,2,2,2,2,2,2,1,2,2,2,1,2,1,2,2,2,3,2,2,2,2,2,1,2,2,2,2,2,2,2,2,1],
    [1,2,1,1,1,1,2,1,2,1,1,1,2,1,1,2,1,2,1,1,1,2,1,1,2,1,1,1,1,2,1,1,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,2,1,2,1,2,1,1,2,1,2,2,2,2,2,2,1],
    [1,2,4,4,4,2,4,4,4,2,4,4,4,4,4,2,1,2,1,2,2,2,2,2,2,1,2,1,1,1,1,2,1],
    [1,2,2,4,2,2,4,0,4,2,4,4,4,4,4,2,1,2,1,1,1,1,1,1,2,1,2,1,1,1,2,2,1],
    [1,2,1,4,2,1,4,0,4,2,4,2,4,2,4,2,1,2,2,2,2,2,2,2,2,2,2,2,2,1,2,1,1],
    [1,2,1,4,2,1,4,0,4,2,4,2,4,2,4,2,1,2,1,1,2,1,1,1,1,1,2,1,1,1,2,2,1],
    [1,2,1,4,2,1,4,0,4,2,4,2,4,2,4,2,1,2,1,1,2,1,1,1,1,1,2,2,2,1,1,2,1],
    [1,2,1,4,2,1,4,4,4,2,4,2,4,2,4,2,2,2,2,2,2,2,2,2,2,2,2,1,2,2,2,2,1],
    [1,2,1,1,2,1,2,1,1,2,2,2,2,2,1,2,1,1,1,1,2,1,1,1,1,2,1,1,2,1,1,2,1],
    [1,2,1,2,2,1,2,1,2,2,1,1,1,1,1,1,1,1,2,2,2,2,1,2,2,2,1,2,2,2,1,2,1],
    [1,2,1,2,1,1,2,1,1,2,2,2,2,2,2,2,2,2,2,1,1,2,1,2,1,2,2,2,1,2,1,2,1],
    [1,2,1,2,1,1,2,2,1,2,4,4,4,2,4,4,4,2,4,4,1,2,1,2,1,2,1,1,1,2,1,2,1],
    [1,2,2,2,2,1,2,1,1,2,4,0,4,2,4,4,4,2,4,0,4,2,1,2,1,2,2,2,2,2,1,2,1],
    [1,1,2,1,2,1,2,1,1,2,4,0,4,2,4,2,4,2,4,0,4,2,1,2,1,2,1,1,2,1,1,2,1],
    [1,2,2,1,2,2,2,2,2,2,4,4,4,2,4,2,4,2,4,0,4,2,1,2,1,2,1,3,2,1,2,2,1],
    [1,1,1,1,2,1,1,1,1,2,4,2,4,2,4,2,4,2,4,0,4,2,1,2,1,2,1,1,2,2,2,1,1],
    [1,2,2,2,2,2,2,2,2,2,4,2,4,2,4,2,4,2,4,4,2,2,1,2,1,2,2,2,2,1,1,1,1],
    [1,2,1,1,1,2,1,1,1,2,1,2,2,2,1,2,1,2,2,2,2,1,1,2,1,1,1,1,1,1,1,1,1],
    [1,2,1,0,1,2,1,2,1,2,1,3,1,1,1,2,1,1,1,2,1,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,2,1,0,1,2,1,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,1,2,1,1,1,2,1,1,1,2,1],
    [1,2,1,0,1,2,1,2,1,1,1,1,1,2,4,2,4,4,4,2,4,4,1,2,4,4,1,2,4,0,4,2,1],
    [1,2,1,0,1,2,1,2,2,2,2,2,2,2,4,2,4,2,2,2,4,0,4,2,4,0,4,2,4,0,4,2,1],
    [1,2,1,0,1,2,1,2,1,1,1,1,1,2,4,2,4,4,4,2,4,4,4,2,4,4,4,2,4,4,4,2,1],
    [1,2,1,0,1,2,1,2,1,2,2,2,4,2,4,2,4,2,2,2,4,4,2,2,4,4,2,2,2,4,2,2,1],
    [1,2,1,1,1,2,2,2,2,2,1,2,4,4,4,2,4,4,4,2,4,0,4,2,4,0,4,2,1,4,2,1,1],
    [1,2,3,2,2,2,1,2,2,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,3,2,2,2,2,2,2,2,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

#Color
COLORS = {
    "BACKGROUND_BLUE": (0, 90, 141),  # Màu nền vintage
    "Brown": (204, 153, 0),
    "White": (255, 255, 255),
    "Red": (244, 67, 54),
    "Pink": (255, 192, 203),
    "Yellow": (255, 255, 0),
    "Green": (0, 255, 0),
    "Black": (0,0,0), 
    "Blue": (0, 0, 255),
    "Purple": (128, 0, 128)
}
#emoji
EMOJI_LOSE = pygame.transform.scale(pygame.image.load(r"img/emoji_lose.png"), (50, 50))
EMOJI_WIN_1 = pygame.transform.scale(pygame.image.load(r"img/emoji_win_1.png"), (50, 50))
EMOJI_WIN_2 = pygame.transform.scale(pygame.image.load(r"img/emoji_win_2.png"), (50, 50))

#Menu logo
MENU_LOGO_1 = r"img/tomandjerry.png"
MENU_LOGO_2 = r"img/pacman.png"

#Pacman, ghost animations
PACMAN_UP_1 = pygame.transform.scale(pygame.image.load(r"img/PACMAN_UP_1.png"), (CELL_SIZE, CELL_SIZE))
PACMAN_UP_2 = pygame.transform.scale(pygame.image.load(r"img/PACMAN_UP_2.png"), (CELL_SIZE, CELL_SIZE))
PACMAN_DOWN_1 = pygame.transform.scale(pygame.image.load(r"img/PACMAN_DOWN_1.png"), (CELL_SIZE, CELL_SIZE))
PACMAN_DOWN_2 = pygame.transform.scale(pygame.image.load(r"img/PACMAN_DOWN_2.png"), (CELL_SIZE, CELL_SIZE))
PACMAN_LEFT_1 = pygame.transform.scale(pygame.image.load(r"img/PACMAN_LEFT_1.png"), (CELL_SIZE, CELL_SIZE))
PACMAN_LEFT_2 = pygame.transform.scale(pygame.image.load(r"img/PACMAN_LEFT_2.png"), (CELL_SIZE, CELL_SIZE))
PACMAN_RIGHT_1 = pygame.transform.scale(pygame.image.load(r"img/PACMAN_RIGHT_1.png"), (CELL_SIZE, CELL_SIZE))
PACMAN_RIGHT_2 = pygame.transform.scale(pygame.image.load(r"img/PACMAN_RIGHT_2.png"), (CELL_SIZE, CELL_SIZE))
POWERUP = pygame.transform.scale(pygame.image.load(r"img/powerup.png"), (CELL_SIZE, CELL_SIZE))
DEAD = pygame.transform.scale(pygame.image.load(r"img/dead.png"), (CELL_SIZE, CELL_SIZE))

GHOST_DEAD = pygame.transform.scale(pygame.image.load(r"img/dead.png"), (CELL_SIZE, CELL_SIZE))
GHOST_BLUE = pygame.transform.scale(pygame.image.load(r"img/blue.png"), (CELL_SIZE, CELL_SIZE))
GHOST_PINK = pygame.transform.scale(pygame.image.load(r"img/pink.png"), (CELL_SIZE, CELL_SIZE))
GHOST_RED = pygame.transform.scale(pygame.image.load(r"img/red.png"), (CELL_SIZE, CELL_SIZE))
GHOST_YELLOW = pygame.transform.scale(pygame.image.load(r"img/yellow.png"), (CELL_SIZE, CELL_SIZE))
GHOST_POWERUP = pygame.transform.scale(pygame.image.load(r"img/powerup.png"), (CELL_SIZE, CELL_SIZE))


