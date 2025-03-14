import pygame
import sys
import os
import math
import psutil
import copy
import time
import heapq
from collections import deque
#Window
WIDTH, HEIGHT = 1200, 850
APP_CAPTION = r"Pacman with Tom and Jerry"
GRID_SIZE = CELL_SIZE = 26  
PI = math.pi

#Screen state
STATE_HOME = "home"
STATE_PLAYING = "playing"
STATE_ABOUT = "about"
STATE_LEVEL = "level"
STATE_GAMEOVER = "gameover"
STATE_WIN = "win"
STATE_RESULT = "result" # Vẽ xong path"
STATE_RESULT_4 = "result for 4"
STATE_HOW_TO_PLAY = "how to play"

#Map
#0: empty,  1: wall,    2: path,    3:power pellets  

#23 x 23
boards1 = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,2,2,2,1,2,3,2,2,2,2,2,2,2,2,2,2,2,1,2,2,2,1],
    [1,2,1,2,1,2,1,1,1,1,1,2,1,1,1,1,1,2,1,2,1,2,1],
    [1,2,2,2,2,2,2,2,1,2,2,2,2,2,1,2,2,2,2,2,2,2,1],
    [1,1,1,2,1,2,1,2,1,2,1,1,1,2,1,2,1,2,1,2,1,1,1],
    [1,2,2,2,1,2,1,2,1,2,1,0,1,2,1,2,1,2,1,2,2,2,1],
    [1,2,1,2,1,2,1,2,1,2,1,1,1,2,1,2,1,2,1,2,1,2,1],
    [1,2,2,2,1,2,1,2,2,2,2,2,2,2,2,2,1,2,1,2,2,2,1],
    [1,1,1,1,1,2,1,2,1,1,1,1,1,1,1,2,1,2,1,1,1,1,1],
    [1,2,2,2,2,2,1,2,2,2,2,2,2,2,2,2,1,2,2,2,2,2,1],
    [1,2,1,1,1,1,1,2,1,1,1,2,1,1,1,2,1,1,1,1,1,2,1],
    [1,2,2,2,2,2,2,2,1,2,2,2,2,2,1,2,2,2,2,2,2,2,1],
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
boards1_offset = ((WIDTH - len(boards1[0]) * GRID_SIZE) // 2, (HEIGHT - len(boards1) * GRID_SIZE) // 2)

#29x33
boards2 = [
     [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
     [1,2,2,2,2,2,2,1,2,2,2,1,2,1,2,2,2,3,2,2,2,2,2,1,2,2,2,2,2,2,2,2,1],
     [1,2,1,1,1,1,2,1,2,1,1,1,2,1,1,2,1,2,1,1,1,2,1,1,2,1,1,1,1,2,1,1,1],
     [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,2,1,2,1,2,1,1,2,1,2,2,2,2,2,2,1],
     [1,2,4,4,4,2,4,4,4,2,4,4,4,4,4,2,1,2,1,2,2,2,2,2,2,1,2,1,1,1,1,2,1],
     [1,2,2,4,2,2,4,0,4,2,4,4,4,4,4,2,1,2,1,1,1,1,1,1,2,1,2,1,1,1,2,2,1],
     [1,2,1,4,2,1,4,0,4,2,4,0,4,0,4,2,1,2,2,2,2,2,2,2,2,2,2,2,2,1,2,1,1],
     [1,2,1,4,2,1,4,0,4,2,4,0,4,0,4,2,1,2,1,1,2,1,1,1,1,1,2,1,1,1,2,2,1],
     [1,2,1,4,2,1,4,0,4,2,4,0,4,0,4,2,1,2,1,1,2,1,1,1,1,1,2,2,2,1,1,2,1],
     [1,2,1,4,2,1,4,4,4,2,4,0,4,0,4,2,2,2,2,2,2,2,2,2,2,2,2,1,2,2,2,2,1],
     [1,2,1,1,2,2,2,1,1,2,2,2,2,2,2,2,1,1,1,1,2,1,1,1,1,2,1,1,2,1,1,2,1],
     [1,2,1,2,2,1,2,1,2,2,1,1,1,1,1,1,1,1,2,2,2,2,1,2,2,2,1,2,2,2,1,2,1],
     [1,2,1,2,1,1,2,1,1,2,2,2,2,2,2,2,2,2,2,1,1,2,1,2,1,2,2,2,1,2,1,2,1],
     [1,2,1,2,1,1,2,2,1,2,4,4,4,2,4,4,4,2,4,4,1,2,1,2,1,2,1,1,1,2,1,2,1],
     [1,2,2,2,2,1,2,1,1,2,4,0,4,2,4,4,4,2,4,0,4,2,1,2,1,2,2,2,2,2,1,2,1],
     [1,1,2,1,2,1,2,1,1,2,4,0,4,2,4,0,4,2,4,0,4,2,1,2,1,2,1,1,2,1,1,2,1],
     [1,2,2,1,2,2,2,2,2,2,4,4,4,2,4,0,4,2,4,0,4,2,1,2,1,2,1,3,2,1,2,2,1],
     [1,1,1,1,2,1,1,1,1,2,4,0,4,2,4,0,4,2,4,0,4,2,1,2,1,2,1,1,2,2,2,1,1],
     [1,2,2,2,2,2,2,2,2,2,4,0,4,2,4,0,4,2,4,4,2,2,1,2,1,2,2,2,2,1,1,1,1],
     [1,2,1,1,1,2,1,1,1,2,1,2,2,2,1,2,1,2,2,2,2,1,1,2,1,1,1,1,1,1,1,1,1],
     [1,2,1,0,1,2,1,2,1,2,1,3,1,1,1,2,1,1,1,2,1,2,2,2,2,2,2,2,2,2,2,2,1],
     [1,2,1,0,1,2,1,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,1,2,1,1,1,2,1,1,1,2,1],
     [1,2,1,0,1,2,1,2,1,1,1,1,1,2,4,2,4,4,4,2,4,4,1,2,4,4,1,2,4,0,4,2,1],
     [1,2,1,0,1,2,1,2,2,2,2,2,2,2,4,2,4,0,0,2,4,0,4,2,4,0,4,2,4,0,4,2,1],
     [1,2,1,0,1,2,1,2,1,1,1,1,1,2,4,2,4,4,4,2,4,4,4,2,4,4,4,2,4,4,4,2,1],
     [1,2,1,0,1,2,1,2,1,2,2,2,4,2,4,2,4,0,0,2,4,4,0,2,4,4,0,2,3,4,2,2,1],
     [1,2,1,1,1,2,2,2,2,2,1,2,4,4,4,2,4,4,4,2,4,0,4,2,4,0,4,2,1,4,2,1,1],
     [1,2,3,2,2,2,1,2,2,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
     [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

#Color
COLORS = {
    "BACKGROUND_BLUE": (0, 90, 141),  
    "Brown": (204, 153, 0),
    "White": (255, 255, 255),
    "Red": (244, 67, 54),
    "Pink": (255, 192, 203),
    "Yellow": (255, 255, 0),
    "Green": (0, 255, 0),
    "Black": (0,0,0), 
    "Blue": (0,191,255),
    "Purple": (128, 0, 128),
    "Orange": (255,127, 0)
}
#emoji
EMOJI_LOSE = pygame.transform.scale(pygame.image.load(r"img/emoji_lose.png"), (50, 50))
EMOJI_WIN_1 = pygame.transform.scale(pygame.image.load(r"img/emoji_win_1.png"), (50, 50))
EMOJI_WIN_2 = pygame.transform.scale(pygame.image.load(r"img/emoji_win_2.png"), (50, 50))

#Menu logo
MENU_LOGO_1 = r"img/tomandjerry.png"
MENU_LOGO_2 = r"img/pacman.png"

#Pacman, ghost animations
PACMAN_UP_1 = pygame.transform.scale(pygame.image.load(r"img/pacman_up_1.png"), (CELL_SIZE, CELL_SIZE))
PACMAN_UP_2 = pygame.transform.scale(pygame.image.load(r"img/pacman_up_2.png"), (CELL_SIZE, CELL_SIZE))
PACMAN_DOWN_1 = pygame.transform.scale(pygame.image.load(r"img/pacman_down_1.png"), (CELL_SIZE, CELL_SIZE))
PACMAN_DOWN_2 = pygame.transform.scale(pygame.image.load(r"img/pacman_down_2.png"), (CELL_SIZE, CELL_SIZE))
PACMAN_LEFT_1 = pygame.transform.scale(pygame.image.load(r"img/pacman_left_1.png"), (CELL_SIZE, CELL_SIZE))
PACMAN_LEFT_2 = pygame.transform.scale(pygame.image.load(r"img/pacman_left_2.png"), (CELL_SIZE, CELL_SIZE))
PACMAN_RIGHT_1 = pygame.transform.scale(pygame.image.load(r"img/pacman_right_1.png"), (CELL_SIZE, CELL_SIZE))
PACMAN_RIGHT_2 = pygame.transform.scale(pygame.image.load(r"img/pacman_right_2.png"), (CELL_SIZE, CELL_SIZE))
PACMAN_POWERUP_UP_1 = pygame.transform.scale(pygame.image.load(r"img/pacman_powerup_up_1.png"), (CELL_SIZE, CELL_SIZE))
PACMAN_POWERUP_UP_2 = pygame.transform.scale(pygame.image.load(r"img/pacman_powerup_up_2.png"), (CELL_SIZE, CELL_SIZE))
PACMAN_POWERUP_DOWN_1 = pygame.transform.scale(pygame.image.load(r"img/pacman_powerup_down_1.png"), (CELL_SIZE, CELL_SIZE))
PACMAN_POWERUP_DOWN_2 = pygame.transform.scale(pygame.image.load(r"img/pacman_powerup_down_2.png"), (CELL_SIZE, CELL_SIZE))
PACMAN_POWERUP_LEFT_1 = pygame.transform.scale(pygame.image.load(r"img/pacman_powerup_left_1.png"), (CELL_SIZE, CELL_SIZE))
PACMAN_POWERUP_LEFT_2 = pygame.transform.scale(pygame.image.load(r"img/pacman_powerup_left_2.png"), (CELL_SIZE, CELL_SIZE))
PACMAN_POWERUP_RIGHT_1 = pygame.transform.scale(pygame.image.load(r"img/pacman_powerup_right_1.png"), (CELL_SIZE, CELL_SIZE))
PACMAN_POWERUP_RIGHT_2 = pygame.transform.scale(pygame.image.load(r"img/pacman_powerup_right_2.png"), (CELL_SIZE, CELL_SIZE))
PACMAN_LIVE = pygame.transform.scale(pygame.image.load(r"img/pacman_live.png"), (CELL_SIZE, CELL_SIZE))

GHOST_DEAD = pygame.transform.scale(pygame.image.load(r"img/dead.png"), (CELL_SIZE, CELL_SIZE))
GHOST_BLUE = pygame.transform.scale(pygame.image.load(r"img/blue.png"), (CELL_SIZE, CELL_SIZE))
GHOST_PINK = pygame.transform.scale(pygame.image.load(r"img/pink.png"), (CELL_SIZE, CELL_SIZE))
GHOST_RED = pygame.transform.scale(pygame.image.load(r"img/red.png"), (CELL_SIZE, CELL_SIZE))
GHOST_ORANGE = pygame.transform.scale(pygame.image.load(r"img/orange.png"), (CELL_SIZE, CELL_SIZE))
GHOST_POWERUP = pygame.transform.scale(pygame.image.load(r"img/powerup.png"), (CELL_SIZE, CELL_SIZE))

BG_IMG = pygame.transform.scale(pygame.image.load(r"img/bg.png"), (CELL_SIZE, CELL_SIZE))

