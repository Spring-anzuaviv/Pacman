from src.specification import *
from src.BoardGame import draw_board1, draw_board2

#khởi tạo Pygame
pygame.init()

#tạo kích thước màn hình
WIDTH, HEIGHT = 1300, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pacman with Tom and Jerry")
font = pygame.font.SysFont("timesnewroman", 50)

background_image1 = pygame.image.load("./img/tomandjerry.png")
background_image2 = pygame.image.load("./img/pacman.png")
#phóng to thu nhỏ
background_image1 = pygame.transform.scale(background_image1, (WIDTH//2.2, HEIGHT//2.2))
background_image2 = pygame.transform.scale(background_image2, (WIDTH//1.8, HEIGHT//3))


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


def screen_game(level):
    screen.fill(COLORS["Black"])

    if(level == 1):
        draw_board1()
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
        draw_board2()
        font = pygame.font.SysFont("timesnewroman", 50, bold = True)
        level_text = font.render(f"Level {level}", True, COLORS["BACKGROUND_BLUE"])
        screen.blit(level_text, (1000, 50))

        font1 = pygame.font.SysFont("timesnewroman", 32)
        time_text = font1.render(f"Score: 0.00", True, COLORS["White"]) 
        screen.blit(time_text, (970, 120))

    draw_button("Back", 1200, 750, 80, 40, COLORS["Red"], lambda: level_menu(), 32)

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

    pygame.quit()
    sys.exit()

def choose_level(level):
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
    #elif(level == 7):
    #    menu()

    pygame.display.update()
    play_game(level)

def level_menu():
    while True:
        screen.fill(COLORS["Black"])
        draw_button("Level 1", 520, 200, 270, 50, COLORS["Pink"], lambda: choose_level(1), 50)
        draw_button("Level 2", 520, 300, 270, 50, COLORS["Green"], lambda: choose_level(2), 50)
        draw_button("Level 3", 520, 400, 270, 50, COLORS["Blue"], lambda: choose_level(3), 50)
        draw_button("Level 4", 520, 500, 270, 50, COLORS["Yellow"], lambda: choose_level(4), 50)
        draw_button("Level 5", 520, 600, 270, 50, COLORS["BACKGROUND_BLUE"], lambda: choose_level(5), 50)
        draw_button("Level 6", 520, 700, 270, 50, COLORS["Purple"], lambda: choose_level(6), 50)
        #draw_button("Back", 1200, 750, 80, 40, COLORS["Red"], lambda: choose_level(7), 32) 

        level_text = font.render("Choose Your Level", True, COLORS["Yellow"])
        screen.blit(level_text, (WIDTH // 2 - level_text.get_width() // 2, 50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

def start_game():
    print("START GAME")
    level_menu()

def exit_game():
    pygame.quit()
    sys.exit()

def menu():
    #di chuyển hình
    screen.blit(background_image1, (350, 30))
    screen.blit(background_image2, (320, 380))

    draw_button("Start Game", 500, 650, 270, 60, COLORS["Green"], start_game, 50)
    draw_button("Exit", 500, 750, 270, 60, COLORS["Red"], exit_game, 50)


    