import sys
sys.path.append("D:/PACMAN/Pacman/src") #path này tùy theo đg dẫn folder src trong máy của mỗi ng
from src.BoardGame import draw_board2, screen, draw_board1
from src.specification import *
from src.ghost import *
from src.menu_ScreenGame import menu, level_menu

os.environ['SDL_VIDEO_CENTERED'] = '1'

#tốc độ FPS
timer = pygame.time.Clock()
FPS = 60

def main():
    ghost = Ghost(x_coord = 26 , y_coord = 26, target = [26 * 4, 26 * 5], speed=2, img=GHOST_BLUE, direct=0, dead=False, powerup=False, board=map)
    path = ghost.move_bfs()
    print(path)
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