import pygame
import os
from src.BoardGame import draw_board2, screen, draw_board1
from src.specification import COLORS
from src.menu_ScreenGame import menu, level_menu


os.environ['SDL_VIDEO_CENTERED'] = '1'

#tốc độ FPS
timer = pygame.time.Clock()
FPS = 60

def main():
    while True:
        timer.tick(FPS)
        screen.fill('black')
        menu()
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        pygame.display.flip()
    pygame.quit()

main()