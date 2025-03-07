import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
# from src.BoardGame import draw_board2, screen, draw_board1
# from src.specification import *
# from src.ghost import *
# from src.menu_ScreenGame import menu, level_menu
# from src.pacman import *
from src.game import *

os.environ['SDL_VIDEO_CENTERED'] = '1'

#tốc độ FPS
timer = pygame.time.Clock()
FPS = 60

def main():
    # ghost = Ghost(x_coord = 26 , y_coord = 26, target = [26 * 20, 26 * 19], speed = 2, img=GHOST_PINK, direct=0, dead=False, powerup=False, board=boards1)
    # path = ghost.move_ucs()
    # ghost.draw_path()
    #print(path)
    # map = copy.deepcopy(boards2)
    # player = Player(screen = screen, x_coord=10 + 26, y_coord=10 + 26, speed=2, direct="", dead=False, powerup=False, board=map, board_offset=0)
    
    # running = True
    # while running:
    #     timer.tick(FPS)
    #     screen.fill('black')
    #    # menu()
        #     player.move()
            
        #     for event in pygame.event.get():
        #         if event.type == pygame.QUIT:
        #             running = False
            
        #     pygame.display.flip()
        # pygame.quit()
    #     screen.fill("black")  # Xóa màn hình cũ
    #     draw_board2(map)
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             running = False
    #         player.move(event)  # Gọi hàm move() để cập nhật vị trí Pac-Man liên tục
    #     player.draw()  # Vẽ Pac-Man ở vị trí mới

    #     pygame.display.flip()  # Cập nhật màn hình
    # pygame.quit()
    game = Game()
    game.run()
    
main()