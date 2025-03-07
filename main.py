import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
from src.game import *


os.environ['SDL_VIDEO_CENTERED'] = '1'

#tốc độ FPS
timer = pygame.time.Clock()
FPS = 60

def main():
    #     screen.fill("black")  # Xóa màn hình cũ
    #     draw_board2(map)
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             running = False
    #         player.move(event)  # Gọi hàm move() để cập nhật vị trí Pac-Man liên tục
    #     player.draw()  # Vẽ Pac-Man ở vị trí mới
        # screen.fill("black")  # Xóa màn hình cũ
        # draw_board2(map)
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         running = False
        #     player.move(event)  # Gọi hàm move() để cập nhật vị trí Pac-Man liên tục

        # if check_win_condition(map):
        #     show_victory_screen(screen)
        #     pygame.quit()
        #     sys.exit()

        # if player.powerup and pygame.time.get_ticks() > player.powerup_timer:
        #     player.powerup = False
        # player.draw()  # Vẽ Pac-Man ở vị trí mới

    game = Game()
    game.run()

main()