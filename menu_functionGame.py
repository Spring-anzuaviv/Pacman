import pygame
import sys
import os
import time
from board_and_color import COLORS
from BoardGame import draw_board1, draw_board2

#khởi tạo Pygame
pygame.init()

#tạo kích thước màn hình
WIDTH, HEIGHT = 1200, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pacman with Tom and Jerry")
font = pygame.font.SysFont("Arial", 50)

background_image1 = pygame.image.load("D:/PACMAN/Pacman/tomandjerry.png")
background_image2 = pygame.image.load("D:/PACMAN/Pacman/pacman.png")
#phóng to thu nhỏ
background_image1 = pygame.transform.scale(background_image1, (WIDTH//2.2, HEIGHT//2.2))
background_image2 = pygame.transform.scale(background_image2, (WIDTH//1.8, HEIGHT//3))


def draw_button(text, x, y, width, height, color, action=None):
    pygame.draw.rect(screen, color, (x, y, width, height))
    text_surface = font.render(text, True, COLORS["Black"])
    screen.blit(text_surface, (x + (width - text_surface.get_width()) // 2, y + (height - text_surface.get_height()) // 2))
    
    # Kiểm tra xem chuột có nhấn vào nút không
    mouse_x, mouse_y = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if x < mouse_x < x + width and y < mouse_y < y + height:
        if click[0] == 1 and action:
            action()


def choose_level(level):
    print(f"Level {level} chosen!")
    screen.fill(COLORS["Black"])

    if(level == 1):
        draw_board1()

    elif(level == 2):
        draw_board1()
    elif(level == 3):
        draw_board1()
    elif(level == 4):
        draw_board1()
    elif(level == 5):
        draw_board1()
    elif(level == 6):
        draw_board2()

    

#đang lỗi
def level_menu():
    while True:
        screen.fill(COLORS["Black"])
        draw_button("Level 1", 450, 200, 270, 50, COLORS["Pink"], lambda: choose_level(1))
        draw_button("Level 2", 450, 300, 270, 50, COLORS["Green"], lambda: choose_level(2))
        draw_button("Level 3", 450, 400, 270, 50, COLORS["Blue"], lambda: choose_level(3))
        draw_button("Level 4", 450, 500, 270, 50, COLORS["Yellow"], lambda: choose_level(4))
        draw_button("Level 5", 450, 600, 270, 50, COLORS["BACKGROUND_BLUE"], lambda: choose_level(5))
        draw_button("Level 6", 450, 700, 270, 50, COLORS["Purple"], lambda: choose_level(6))

        level_text = font.render("Choose Your Level", True, (255, 255, 0))
        screen.blit(level_text, (WIDTH // 2 - level_text.get_width() // 2, 50))

        # Kiểm tra sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Kiểm tra nếu chuột click vào các nút
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                
                # Kiểm tra nếu chuột nhấn vào "Level 1"
                if 450 <= mouse_x <= 450 + 270 and 200 <= mouse_y <= 200 + 50:
                    choose_level(1)
                    return  # Chuyển sang level 1 và thoát khỏi vòng lặp này

                # Kiểm tra các nút khác (Level 2 đến Level 6)
                elif 450 <= mouse_x <= 450 + 270:
                    if 300 <= mouse_y <= 300 + 50:
                        choose_level(2)
                        return
                    elif 400 <= mouse_y <= 400 + 50:
                        choose_level(3)
                        return
                    elif 500 <= mouse_y <= 500 + 50:
                        choose_level(4)
                        return
                    elif 600 <= mouse_y <= 600 + 50:
                        choose_level(5)
                        return
                    elif 700 <= mouse_y <= 700 + 50:
                        choose_level(6)
                        return

        pygame.display.update()

def start_game():
    print("START GAME")
    level_menu()

def exit_game():
    pygame.quit()
    sys.exit()

def menu():
    #di chuyển hình
    screen.blit(background_image1, (300, 30))
    screen.blit(background_image2, (280, 380))

    draw_button("Start Game", 450, 650, 270, 60, COLORS["Green"], start_game)
    draw_button("Exit", 450, 750, 270, 60, COLORS["Red"], exit_game)


    