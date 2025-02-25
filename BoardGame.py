from board import boards
import pygame
import math

#khởi tạo Pygame
pygame.init()

#tạo kích thước màn hình
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pacman with Tom and Jerry")
font = pygame.font.Font(None, 20)

#tốc độ FPS
timer = pygame.time.Clock()
FPS = 60
PI = math.pi
#chọn level 1
color = 'pink'
level = boards
def draw_board():
    num1 = ((HEIGHT - 50) // len(boards))
    num2 = (WIDTH // len(boards[0]))
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level [i][j] == 1:
                pygame.draw.circle(screen, 'lightgreen', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 4)
            if level [i][j] == 2:
                pygame.draw.circle(screen, 'yellow', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 10)
            if level [i][j] == 3:
                pygame.draw.line(screen, color, (j * num2 + (0.5 * num2), i * num1),
                                (j * num2 + (0.5 * num2), i * num1 + num1), 3)
            if level[i][j] == 4:
                pygame.draw.line(screen, color, (j * num2, i * num1 + (0.5 * num1)),
                                 (j * num2 + num2, i * num1 + (0.5 * num1)), 3)
            if level[i][j] == 5:
                pygame.draw.arc(screen, color, [(j * num2 - (num2 * 0.4)) - 2, (i * num1 + (0.5 * num1)), num2, num1],
                                0, PI / 2, 3)
            if level[i][j] == 6:
                pygame.draw.arc(screen, color,
                                [(j * num2 + (num2 * 0.5)), (i * num1 + (0.5 * num1)), num2, num1], PI / 2, PI, 3)
            if level[i][j] == 7:
                pygame.draw.arc(screen, color, [(j * num2 + (num2 * 0.5)), (i * num1 - (0.4 * num1)), num2, num1], PI,
                                3 * PI / 2, 3)
            if level[i][j] == 8:
                pygame.draw.arc(screen, color,
                                [(j * num2 - (num2 * 0.4)) - 2, (i * num1 - (0.4 * num1)), num2, num1], 3 * PI / 2,
                                2 * PI, 3)
            if level[i][j] == 9:
                pygame.draw.line(screen, 'white', (j * num2, i * num1 + (0.5 * num1)),
                                 (j * num2 + num2, i * num1 + (0.5 * num1)), 3)

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