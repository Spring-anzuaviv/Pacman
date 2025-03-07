from src.specification import *
from src.BoardGame import draw_board1, draw_board2
from src.pacman import *

#khởi tạo Pygame
pygame.init()

#tạo kích thước màn hình
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(APP_CAPTION)
font = pygame.font.SysFont("timesnewroman", 32)

background_image1 = pygame.image.load(MENU_LOGO_1)
background_image2 = pygame.image.load(MENU_LOGO_2)
#phóng to thu nhỏ
background_image1 = pygame.transform.scale(background_image1, (WIDTH//2.2, HEIGHT//2.2))
background_image2 = pygame.transform.scale(background_image2, (WIDTH//1.8, HEIGHT//3))

player = Player(screen = screen, x_coord=10+26, y_coord=10+26,  target=[0, 0], speed=2, direct="", dead=False, powerup=False, board=boards2)

def draw_button(text, x, y, width, height, color, action=None, fontsize=int):
    pygame.draw.rect(screen, color, (x, y, width, height))
    font = pygame.font.SysFont("timesnewroman", fontsize)
    text_surface = font.render(text, True, COLORS["Black"])
    screen.blit(text_surface, (x + (width - text_surface.get_width()) // 2, y + (height - text_surface.get_height()) // 2))
    
    # Kiểm tra xem chuột có nhấn vào nút không
    mouse_x, mouse_y = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if x < mouse_x < x + width and y < mouse_y < y + height:
        if click[0] == 1 and action:
            action()

#xử lí phím cho player ở level 6
def handle_input():
    # Xử lý di chuyển của Pac-Man khi nhấn các phím mũi tên
    keys = pygame.key.get_pressed()  # Lấy trạng thái tất cả các phím
    if keys[pygame.K_RIGHT]:
        player.direction = "right"
        player.move()
    elif keys[pygame.K_LEFT]:
        player.direction = "left"
        player.move()
    elif keys[pygame.K_UP]:
        player.direction = "up"
        player.move()
    elif keys[pygame.K_DOWN]:
        player.direction = "down"
        player.move()

def screen_game(level):
    screen.fill(COLORS["Black"])
    global screen_running
    screen_running = True
    while screen_running:
        if(level == 1):
            draw_board1()
            player.draw()
            font = pygame.font.SysFont("timesnewroman", 50, bold = True)
            level_text = font.render(f"Level {level}", True, COLORS["Pink"])
            screen.blit(level_text, (900, 20))
            
            font1 = pygame.font.SysFont("timesnewroman", 32)
            time_text = font1.render(f"Search Time: 0.00 s", True, COLORS["White"]) 
            screen.blit(time_text, (830, 120))

            memory_text = font1.render(f"Memory Usage: 0 MB", True, COLORS["White"]) 
            screen.blit(memory_text, (830, 180))

            expanded_nodes_text = font1.render(f"Expanded Nodes: 0", True, COLORS["White"])  
            screen.blit(expanded_nodes_text, (830, 240))

        elif(level == 2):
            draw_board1()
            player.draw()
            font = pygame.font.SysFont("timesnewroman", 50, bold = True)
            level_text = font.render(f"Level {level}", True, COLORS["Green"])
            screen.blit(level_text, (900, 20))

            font1 = pygame.font.SysFont("timesnewroman", 32)
            time_text = font1.render(f"Search Time: 0.00 s", True, COLORS["White"]) 
            screen.blit(time_text, (830, 120))

            memory_text = font1.render(f"Memory Usage: 0 MB", True, COLORS["White"]) 
            screen.blit(memory_text, (830, 180))

            expanded_nodes_text = font1.render(f"Expanded Nodes: 0", True, COLORS["White"])  
            screen.blit(expanded_nodes_text, (830, 240))

        elif(level == 3):
            draw_board1()
            player.draw()
            font = pygame.font.SysFont("timesnewroman", 50, bold = True)
            level_text = font.render(f"Level {level}", True, COLORS["Blue"])
            screen.blit(level_text, (900, 20))

            font1 = pygame.font.SysFont("timesnewroman", 32)
            time_text = font1.render(f"Search Time: 0.00 s", True, COLORS["White"]) 
            screen.blit(time_text, (850, 120))

            memory_text = font1.render(f"Memory Usage: 0 MB", True, COLORS["White"]) 
            screen.blit(memory_text, (850, 180))

            expanded_nodes_text = font1.render(f"Expanded Nodes: 0", True, COLORS["White"])  
            screen.blit(expanded_nodes_text, (850, 240))

        elif(level == 4):
            draw_board1()
            player.draw()
            font = pygame.font.SysFont("timesnewroman", 50, bold = True)
            level_text = font.render(f"Level {level}", True, COLORS["Yellow"])
            screen.blit(level_text, (900, 20))

            font1 = pygame.font.SysFont("timesnewroman", 32)
            time_text = font1.render(f"Search Time: 0.00 s", True, COLORS["White"]) 
            screen.blit(time_text, (850, 120))

            memory_text = font1.render(f"Memory Usage: 0 MB", True, COLORS["White"]) 
            screen.blit(memory_text, (850, 180))

            expanded_nodes_text = font1.render(f"Expanded Nodes: 0", True, COLORS["White"])  
            screen.blit(expanded_nodes_text, (850, 240))

        elif(level == 5):
            draw_board1()
            player.draw()
            font = pygame.font.SysFont("timesnewroman", 50, bold = True)
            level_text = font.render(f"Level {level}", True, COLORS["BACKGROUND_BLUE"])
            screen.blit(level_text, (900, 20))

            font1 = pygame.font.SysFont("timesnewroman", 32)
            time_text = font1.render(f"Search Time: 0.00 s", True, COLORS["White"]) 
            screen.blit(time_text, (850, 120))

            memory_text = font1.render(f"Memory Usage: 0 MB", True, COLORS["White"]) 
            screen.blit(memory_text, (850, 180))

            expanded_nodes_text = font1.render(f"Expanded Nodes: 0", True, COLORS["White"])  
            screen.blit(expanded_nodes_text, (850, 240))
        elif(level == 6):
            screen.fill((0, 0, 0))
            draw_board2()
            keys = pygame.key.get_pressed()  # Kiểm tra phím đang được giữ
            if keys[pygame.K_LEFT]:
                player.direction = "left"
            elif keys[pygame.K_RIGHT]:
                player.direction = "right"
            elif keys[pygame.K_UP]:
                player.direction = "up"
            elif keys[pygame.K_DOWN]:
                player.direction = "down"
            player.move()
            player.draw()

            font = pygame.font.SysFont("timesnewroman", 50, bold = True)
            level_text = font.render(f"Level {level}", True, COLORS["BACKGROUND_BLUE"])
            screen.blit(level_text, (1000, 50))

            font1 = pygame.font.SysFont("timesnewroman", 32)
            time_text = font1.render(f"Score: {player.get_score()}", True, COLORS["White"]) 
            screen.blit(time_text, (970, 120))

            font1 = pygame.font.SysFont("timesnewroman", 32)
            time_text = font1.render(f"Lives: {player.get_lives()}", True, COLORS["White"]) 
            screen.blit(time_text, (970, 160))

            pygame.display.update()

        draw_button("Back", 1100, 750, 80, 40, COLORS["Red"], lambda: level_menu(), 32)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()

#hàm này tạm thời
def play_game(level):
    running = True
    while running:
        screen_game(level)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  
                running = False # end game khi đóng cửa sổ, nháp
            #xử lí di chuyển va chạm
        
        #update state game
        #vẽ lại các obj game khi chơi
        pygame.display.update()

    # pygame.quit()
    # sys.exit()

def level_menu():
    global screen_running
    screen_running = True
    while screen_running:
        screen.fill(COLORS["Black"])
        draw_button("Level 1", 480, 120, 270, 50, COLORS["Pink"], lambda: screen_game(1), 50)
        draw_button("Level 2", 480, 220, 270, 50, COLORS["Green"], lambda: screen_game(2), 50)
        draw_button("Level 3", 480, 320, 270, 50, COLORS["Blue"], lambda: screen_game(3), 50)
        draw_button("Level 4", 480, 420, 270, 50, COLORS["Yellow"], lambda: screen_game(4), 50)
        draw_button("Level 5", 480, 520, 270, 50, COLORS["BACKGROUND_BLUE"], lambda: screen_game(5), 50)
        draw_button("Level 6", 480, 620, 270, 50, COLORS["Purple"], lambda: screen_game(6), 50)
        draw_button("Back", 20, 20, 80, 40, COLORS["Red"], lambda: exit_level_menu(), 32) 

        level_text = font.render("Choose Your Level", True, COLORS["Yellow"])
        screen.blit(level_text, (WIDTH // 2 - level_text.get_width() // 2, 50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
    

def exit_level_menu():
    global screen_running
    screen_running = False
    menu()

def start_game():
    print("START GAME")
    global screen_running
    screen_running = True
    level_menu()
   
def exit_game():
    pygame.quit()
    sys.exit()

def menu():
    #di chuyển hình
    screen.fill(COLORS["Black"])  # Xóa màn hình cũ
    screen.blit(background_image1, (350, 30))
    screen.blit(background_image2, (320, 380))

    draw_button("Start Game", 200, 650, 270, 60, COLORS["Green"], start_game, 50)
    draw_button("Exit", 800, 650, 270, 60, COLORS["Red"], exit_game, 50)
    
    pygame.display.update()  # Cập nhật màn hình menu


def show_victory_screen(screen):
    screen.fill((0, 0, 0))  # Đặt nền màu đen
    font = pygame.font.SysFont("timesnewroman", 50, bold=True)
    win_text = font.render("YOU WIN!", True, (255, 255, 0))
    screen.blit(EMOJI_WIN_1, (425, 345))
    screen.blit(EMOJI_WIN_2, (725, 345))

    text_rect = win_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 50))
    
    sub_text = font.render("Press ENTER to Play Again", True, (255, 255, 255))
    sub_text_rect = sub_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 50))

    screen.blit(win_text, text_rect)
    screen.blit(sub_text, sub_text_rect)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Nhấn ENTER để chơi lại
                    waiting = False


def show_game_over_screen(screen):
    screen.fill((0, 0, 0))  # Đặt nền màu đen
    font = pygame.font.SysFont("timesnewroman", 50, bold=True)
    text = font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(EMOJI_LOSE, (390, 345))
    screen.blit(EMOJI_LOSE, (760, 345))

    text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 50))
    
    sub_text = font.render("Press ENTER to Try Again", True, (255, 255, 255))
    sub_text_rect = sub_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 50))

    screen.blit(text, text_rect)
    screen.blit(sub_text, sub_text_rect)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Nhấn ENTER để chơi lại
                    waiting = False
