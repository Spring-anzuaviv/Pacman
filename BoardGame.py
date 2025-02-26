from board import boards
import pygame
import math
import os

#khởi tạo Pygame
pygame.init()

#tạo kích thước màn hình
WIDTH, HEIGHT = 890, 850
os.environ['SDL_VIDEO_CENTERED'] = '1'
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pacman with Tom and Jerry")
font = pygame.font.Font(None, 20)

GRID_SIZE = 30  # Kích thước mỗi ô vuông
#tốc độ FPS
timer = pygame.time.Clock()
FPS = 60
PI = math.pi

#chọn level 1
color = 'pink'
def draw_board():
    maze_width = len(boards[0]) * GRID_SIZE
    maze_height = len(boards) * GRID_SIZE
    offset_x = (WIDTH - maze_width) // 2
    offset_y = (HEIGHT - maze_height) // 2

    for row in range(len(boards)):
        for col in range(len(boards[row])):
            x, y = offset_x + col * GRID_SIZE, offset_y + row * GRID_SIZE
            if boards[row][col] == 1:
                pygame.draw.rect(screen, 'pink', (x, y, GRID_SIZE, GRID_SIZE))
            elif boards[row][col] == 2:
                pygame.draw.circle(screen, 'white', (x + GRID_SIZE // 2, y + GRID_SIZE // 2), 5)
            elif boards[row][col] == 3:
                pygame.draw.circle(screen, 'yellow', (x + GRID_SIZE // 2, y + GRID_SIZE // 2), 10)

running = True
while running:
    timer.tick(FPS)
    screen.fill('black')
    draw_board()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    pygame.display.flip()
pygame.quit()