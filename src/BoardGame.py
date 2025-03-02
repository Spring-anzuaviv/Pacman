from src.specification import *
#khởi tạo Pygame
pygame.init()

#tạo kích thước màn hình
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(APP_CAPTION)
font = pygame.font.Font(None, 20)

#chọn level 1 - 5
def draw_board1():
    maze_width = len(boards1[0]) * GRID_SIZE
    maze_height = len(boards1) * GRID_SIZE
    offset_x = 100
    offset_y = 100 
    

    for row in range(len(boards1)):
        for col in range(len(boards1[row])):
            x, y = offset_x + col * GRID_SIZE, offset_y + row * GRID_SIZE
            if boards1[row][col] == 1:
                pygame.draw.rect(screen, COLORS["Pink"], (x, y, GRID_SIZE, GRID_SIZE))
            elif boards1[row][col] == 2:
                pygame.draw.circle(screen, COLORS["White"], (x + GRID_SIZE // 2, y + GRID_SIZE // 2), 5)
            elif boards1[row][col] == 3:
                pygame.draw.circle(screen, COLORS["Yellow"], (x + GRID_SIZE // 2, y + GRID_SIZE // 2), 10)


                #####################################################
    #test ghost and pacman
    screen.blit(GHOST_BLUE, (offset_x + 26, offset_y + 26))
    #pacman được thêm vô menu_ScreenGame hàm screen_game()

#level 6
def draw_board2():
    maze_width = (len(boards2[0]) * GRID_SIZE)//5
    maze_height = (len(boards2) * GRID_SIZE)//15
    offset_x = 10
    offset_y = 10

    for row in range(len(boards2)):
        for col in range(len(boards2[row])):
            x, y = offset_x + col * GRID_SIZE, offset_y + row * GRID_SIZE
            if boards2[row][col] == 1:
                pygame.draw.rect(screen, COLORS["BACKGROUND_BLUE"], (x, y, GRID_SIZE, GRID_SIZE))  # Tường màu hồng
            elif boards2[row][col] == 2:
                pygame.draw.circle(screen, COLORS["White"], (x + GRID_SIZE // 2, y + GRID_SIZE // 2), 5)  # Đường đi Pacman
            elif boards2[row][col] == 3:
                pygame.draw.circle(screen, COLORS["Red"], (x + GRID_SIZE // 2, y + GRID_SIZE // 2), 10)  # Power Pellets
            elif boards2[row][col] == 4:
                pygame.draw.rect(screen, COLORS["Brown"], (x, y, GRID_SIZE, GRID_SIZE))  # Tường đặc biệt màu nâu