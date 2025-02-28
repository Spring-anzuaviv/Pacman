import pygame
import os
from src.BoardGame import draw_board2, screen, draw_board1
from src.board_and_color import COLORS
from src.menu_functionGame import menu, level_menu


os.environ['SDL_VIDEO_CENTERED'] = '1'

#tốc độ FPS
timer = pygame.time.Clock()
FPS = 60

def main():
    while True:
        timer.tick(FPS)
        screen.fill('black')
        #draw_board1()
        #draw_board2()
        menu()
        #level_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        pygame.display.flip()
    pygame.quit()

main()