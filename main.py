import sys
import os
import pygame

# Thêm đường dẫn src để import module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
from src.BoardGame import draw_board1, screen
from src.specification import *
from src.pacman import Player  # Đúng class của Pac-Man

os.environ['SDL_VIDEO_CENTERED'] = '1'

# Tốc độ FPS
timer = pygame.time.Clock()
FPS = 60

# Sự kiện kết thúc Powerup
POWERUP_END_EVENT = pygame.USEREVENT + 1

def main():
    # Khởi tạo hình ảnh Pac-Man
    player_images = [PACMAN_RIGHT_1, PACMAN_RIGHT_2, PACMAN_RIGHT_1, PACMAN_RIGHT_2]

    # Tạo Pac-Man
    pacman = Player(
        x_coord=100, 
        y_coord=100, 
        target=[0, 0], 
        speed=2, 
        images=player_images, 
        direct="right", 
        dead=False, 
        powerup=False, 
        board=boards1
    )

    running = True
    while running:
        timer.tick(FPS)
        screen.fill(COLORS["Black"])  # Xóa màn hình cũ

        draw_board1()  # Vẽ lại bàn cờ
        pacman.draw()  # Vẽ Pac-Man theo trạng thái

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Nhấn P để bật Powerup
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    print("Powerup activated!")
                    pacman.powerup = True
                    pygame.time.set_timer(POWERUP_END_EVENT, 5000)  # Powerup kéo dài 5 giây

                # Nhấn D để bật Dead
                elif event.key == pygame.K_d:
                    print("Pac-Man died!")
                    pacman.dead = True

            # Khi hết thời gian Powerup
            elif event.type == POWERUP_END_EVENT:
                print("Powerup ended!")
                pacman.powerup = False

        pygame.display.flip()  # Cập nhật màn hình sau mỗi frame

    pygame.quit()
    sys.exit()

main()