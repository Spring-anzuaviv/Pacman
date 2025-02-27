from board import boards2, boards1
import pygame
import math
import os

#khởi tạo Pygame
pygame.init()

#tạo kích thước màn hình
WIDTH, HEIGHT = 1200, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pacman with Tom and Jerry")
font = pygame.font.Font(None, 20)

GRID_SIZE = 26  # Kích thước mỗi ô vuông
PI = math.pi

COLORS = {
    "TOM_GRAY": (166, 166, 166),
    "JERRY_BROWN": (156, 107, 48),  # Tai và bụng Jerry
    "BELLY_WHITE": (242, 230, 206), 
    "BACKGROUND_BLUE": (0, 90, 141),  # Màu nền vintage
    "LOGO_RED": (224, 60, 49),  # Màu chữ logo
    "VINTAGE_GREEN": (124, 158, 143),  # Màu nội thất
    "Brown": (204, 153, 0)
}

#chọn level 1 - 5
def draw_board1():
    maze_width = len(boards1[0]) * GRID_SIZE
    maze_height = len(boards1) * GRID_SIZE
    offset_x = (WIDTH - maze_width) // 2
    offset_y = (HEIGHT - maze_height) // 2

    for row in range(len(boards1)):
        for col in range(len(boards1[row])):
            x, y = offset_x + col * GRID_SIZE, offset_y + row * GRID_SIZE
            if boards1[row][col] == 1:
                pygame.draw.rect(screen, 'pink', (x, y, GRID_SIZE, GRID_SIZE))
            elif boards1[row][col] == 2:
                pygame.draw.circle(screen, 'white', (x + GRID_SIZE // 2, y + GRID_SIZE // 2), 5)
            elif boards1[row][col] == 3:
                pygame.draw.circle(screen, 'yellow', (x + GRID_SIZE // 2, y + GRID_SIZE // 2), 10)
                

#level 6
def draw_board2():
    maze_width = len(boards2[0]) * GRID_SIZE
    maze_height = len(boards2) * GRID_SIZE
    offset_x = (WIDTH - maze_width) // 2
    offset_y = (HEIGHT - maze_height) // 2

    for row in range(len(boards2)):
        for col in range(len(boards2[row])):
            x, y = offset_x + col * GRID_SIZE, offset_y + row * GRID_SIZE
            if boards2[row][col] == 1:
                pygame.draw.rect(screen, COLORS["BACKGROUND_BLUE"], (x, y, GRID_SIZE, GRID_SIZE))  # Tường màu hồng
            elif boards2[row][col] == 2:
                pygame.draw.circle(screen, 'white', (x + GRID_SIZE // 2, y + GRID_SIZE // 2), 5)  # Đường đi Pacman
            elif boards2[row][col] == 3:
                pygame.draw.circle(screen, 'red', (x + GRID_SIZE // 2, y + GRID_SIZE // 2), 10)  # Power Pellets
            elif boards2[row][col] == 4:
                pygame.draw.rect(screen, COLORS["Brown"], (x, y, GRID_SIZE, GRID_SIZE))  # Tường đặc biệt màu nâu