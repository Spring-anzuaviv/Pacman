import pygame
import os
from BoardGame import draw_board2, screen, draw_board1, COLORS

os.environ['SDL_VIDEO_CENTERED'] = '1'

#tốc độ FPS
timer = pygame.time.Clock()
FPS = 60

running = True
while running:
    timer.tick(FPS)
    screen.fill('black')
    draw_board1()
    #draw_board2()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    pygame.display.flip()
pygame.quit()