from specification import *
from pacman import *
from ghost import *
class Game:
    def __init__(self): 
    # Menu screen
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(APP_CAPTION)
        self.font = pygame.font.SysFont("timesnewroman", 32)
        self.background_image1 = pygame.image.load(MENU_LOGO_1)
        self.background_image2 = pygame.image.load(MENU_LOGO_2)
        self.background_image1 = pygame.transform.scale(self.background_image1, (WIDTH//2.2, HEIGHT//2.2))
        self.background_image2 = pygame.transform.scale(self.background_image2, (WIDTH//1.8, HEIGHT//3))
        self.state = "home"
        self.level = 0
        self.board = []
        self.path = []
        self.img = None
        self.offset = 0
        # Nếu win, thua reset lại
        # Nếu tạm dừng có thể 
        self.player = Player(screen = self.screen, x_coord = 10 + 26, y_coord = 10 + 26, speed = 2, direct="", dead=False, powerup=False, board=self.board, board_offset = 0)
        self.pink_ghost = Ghost(x_coord = 26 , y_coord = 26, target = [26 * 20, 26 * 19], speed = 2, img=GHOST_PINK, direct=0, dead=False, powerup=False, board=self.board, board_offset = 0)
        self.blue_ghost = Ghost(x_coord = 26 , y_coord = 26, target = [26 * 20, 26 * 19], speed = 2, img=GHOST_BLUE, direct=0, dead=False, powerup=False, board=self.board, board_offset = 0)
        self.orange_ghost = Ghost(x_coord = 26 , y_coord = 26, target = [26 * 20, 26 * 19], speed = 2, img=GHOST_YELLOW, direct=0, dead=False, powerup=False, board=self.board, board_offset = 0)
        self.red_ghost = Ghost(x_coord = 26 , y_coord = 26, target = [26 * 20, 26 * 19], speed = 2, img=GHOST_RED, direct=0, dead=False, powerup=False, board=self.board, board_offset = 0)


    def draw_board1(self):
        maze_width = len(boards1[0]) * GRID_SIZE
        maze_height = len(boards1) * GRID_SIZE
        offset_x = 100
        offset_y = 100 

        for row in range(len(boards1)):
            for col in range(len(boards1[row])):
                x, y = offset_x + col * GRID_SIZE, offset_y + row * GRID_SIZE
                if boards1[row][col] == 1:
                    pygame.draw.rect(self.screen, COLORS["Pink"], (x, y, GRID_SIZE, GRID_SIZE))
                elif boards1[row][col] == 2:
                    pygame.draw.circle(self.screen, COLORS["White"], (x + GRID_SIZE // 2, y + GRID_SIZE // 2), 5)
                elif boards1[row][col] == 3:
                    pygame.draw.circle(self.screen, COLORS["Yellow"], (x + GRID_SIZE // 2, y + GRID_SIZE // 2), 10)
                elif boards1[row][col] == 5:
                    pygame.draw.rect(self.screen, COLORS["Black"], (x, y, GRID_SIZE, GRID_SIZE))

    def draw_board2(self, boards2):
        maze_width = (len(boards2[0]) * GRID_SIZE)//5
        maze_height = (len(boards2) * GRID_SIZE)//15
        offset_x = 10
        offset_y = 10

        for row in range(len(boards2)):
            for col in range(len(boards2[row])):
                x, y = offset_x + col * GRID_SIZE, offset_y + row * GRID_SIZE
                if boards2[row][col] == 1:
                    pygame.draw.rect(self.screen, COLORS["BACKGROUND_BLUE"], (x, y, GRID_SIZE, GRID_SIZE))  # Tường màu hồng
                elif boards2[row][col] == 2:
                    pygame.draw.circle(self.screen, COLORS["White"], (x + GRID_SIZE // 2, y + GRID_SIZE // 2), 5)  # Đường đi Pacman
                elif boards2[row][col] == 3:
                    pygame.draw.circle(self.screen, COLORS["Red"], (x + GRID_SIZE // 2, y + GRID_SIZE // 2), 10)  # Power Pellets
                elif boards2[row][col] == 4:
                    pygame.draw.rect(self.screen, COLORS["Brown"], (x, y, GRID_SIZE, GRID_SIZE))  # Tường đặc biệt màu nâu
                elif boards2[row][col] == 5:
                    pygame.draw.rect(self.screen, COLORS["Black"], (x, y, GRID_SIZE, GRID_SIZE ))

    def draw_button(self, text, x, y, width, height, color, action=None, fontsize=int):
        pygame.draw.rect(self.screen, color, (x, y, width, height))
        self.font = pygame.font.SysFont("timesnewroman", fontsize)
        text_surface = self.font.render(text, True, COLORS["Black"])
        self.screen.blit(text_surface, (x + (width - text_surface.get_width()) // 2, y + (height - text_surface.get_height()) // 2))
        
        # Kiểm tra xem chuột có nhấn vào nút không
        mouse_x, mouse_y = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        
        if x < mouse_x < x + width and y < mouse_y < y + height:
            if click[0] == 1 and action:
                action()

    def set_state(self, new_state, new_level):
        self.state = new_state
        if new_level:
            self.level = new_level  

    def level_menu(self):
        self.state = "level"
        # global screen_running
        # screen_running = True
        # while screen_running:
        #self.screen.fill(COLORS["Black"])
        self.draw_button("Level 1", 480, 120, 270, 50, COLORS["Pink"], lambda: self.set_state(STATE_PLAYING, 1), 50)
        self.draw_button("Level 2", 480, 220, 270, 50, COLORS["Green"], lambda: self.set_state(STATE_PLAYING, 2), 50)
        self.draw_button("Level 3", 480, 320, 270, 50, COLORS["Blue"], lambda: self.set_state(STATE_PLAYING, 3), 50)
        self.draw_button("Level 4", 480, 420, 270, 50, COLORS["Yellow"], lambda: self.set_state(STATE_PLAYING, 4), 50)
        self.draw_button("Level 5", 480, 520, 270, 50, COLORS["BACKGROUND_BLUE"], lambda: self.set_state(STATE_PLAYING, 5), 50)
        self.draw_button("Level 6", 480, 620, 270, 50, COLORS["Purple"], lambda: self.set_state(STATE_PLAYING, 6), 50)
        self.draw_button("Back", 20, 20, 80, 40, COLORS["Red"], lambda: self.exit_level_menu(), 32) 

        level_text = self.font.render("Choose Your Level", True, COLORS["Yellow"])
        self.screen.blit(level_text, (WIDTH // 2 - level_text.get_width() // 2, 50))

            # for event in pygame.event.get():
            #     if event.type == pygame.QUIT:
            #         pygame.quit()
            #         sys.exit()
           # pygame.display.update()    

    def launch_game(self, level):
        if self.level == 1:
            self.level_1()
        elif self.level == 2:
            self.level_2()
        elif self.level == 3:
            self.level_3()
        elif self.level == 4:
            self.level_4()
        elif self.level == 5:
            self.level_5()

    def exit_level_menu(self):
        self.state = "home"
        global screen_running
        screen_running = False
        self.home_screen()
    
    def exit_game(self):
        pygame.quit()
        sys.exit()

    def home_screen(self):
        self.state = "home"
        self.screen.blit(self.background_image1, (350, 30))
        self.screen.blit(self.background_image2, (320, 380))

        self.draw_button("Start Game", 200, 650, 270, 60, COLORS["Green"], self.level_menu, 50)
        self.draw_button("Exit", 800, 650, 270, 60, COLORS["Red"], self.exit_game, 50)

    def reset_ghost(self, ghost): ...
    def reset_player(self): ...


    # Level 1:  Implement the Blue Ghost using Breadth-First Search (BFS) algorithm to chase Pac-Man
    def level_1(self):
        self.offset = 100
        self.draw_board1()
        self.board = copy.deepcopy(boards1) #check ghost và player board trỏ cùng vị trí vs board game chưa
        self.player.map = copy.deepcopy(boards1)

        self.player.offset = 100
        self.player.update_position(self.offset + 26 * 21, self.offset + 26 * 21)
        self.player.appear()

        self.blue_ghost.map = copy.deepcopy(boards1)
        self.blue_ghost.offset = 100
        self.blue_ghost.update_position(self.offset + CELL_SIZE, self.offset + CELL_SIZE)
        self.blue_ghost.target = [self.player.x_pos, self.player.y_pos]
        print((self.blue_ghost.target[1], self.blue_ghost.target[0]))

        path = self.blue_ghost.move_bfs()
        self.blue_ghost.draw_path()

        font = pygame.font.SysFont("timesnewroman", 50, bold = True)
        level_text = font.render(f"Level {self.level}", True, COLORS["Pink"])
        self.screen.blit(level_text, (900, 20))
        

        font1 = pygame.font.SysFont("timesnewroman", 32)
        time_text = font1.render(f"Search Time: 0.00 s", True, COLORS["White"]) 
        self.screen.blit(time_text, (830, 120))

        memory_text = font1.render(f"Memory Usage: 0 MB", True, COLORS["White"]) 
        self.screen.blit(memory_text, (830, 180))

        expanded_nodes_text = font1.render(f"Expanded Nodes: 0", True, COLORS["White"])  
        self.screen.blit(expanded_nodes_text, (830, 240))
        self.draw_button("Back", 1100, 750, 80, 40, COLORS["Red"], lambda: self.level_menu(), 32)
        self.state = STATE_HOME

    # Level 2: Implement the Pink Ghost using the Depth-First Search (DFS) algorithm to chase Pac-Man.
    def level_2(self): 
        self.offset = 100
        self.draw_board1()
        self.board = copy.deepcopy(boards1) #check ghost và player board trỏ cùng vị trí vs board game chưa
        self.player.map = copy.deepcopy(boards1)

        self.player.offset = 100
        self.player.update_position(self.offset + 26 * 21, self.offset + 26 * 21)
        self.player.appear()

        self.pink_ghost.map = copy.deepcopy(boards1)
        self.pink_ghost.offset = 100
        self.pink_ghost.update_position(self.offset + CELL_SIZE, self.offset + CELL_SIZE)
        self.pink_ghost.target = [self.player.x_pos, self.player.y_pos]
        # print((self.pink_ghost.target[1], self.pink_ghost.target[0]))

        path = self.pink_ghost.move_dfs()
        self.pink_ghost.draw_path()

        font = pygame.font.SysFont("timesnewroman", 50, bold = True)
        level_text = font.render(f"Level {self.level}", True, COLORS["Pink"])
        self.screen.blit(level_text, (900, 20))
        

        font1 = pygame.font.SysFont("timesnewroman", 32)
        time_text = font1.render(f"Search Time: 0.00 s", True, COLORS["White"]) 
        self.screen.blit(time_text, (830, 120))

        memory_text = font1.render(f"Memory Usage: 0 MB", True, COLORS["White"]) 
        self.screen.blit(memory_text, (830, 180))

        expanded_nodes_text = font1.render(f"Expanded Nodes: 0", True, COLORS["White"])  
        self.screen.blit(expanded_nodes_text, (830, 240))
        self.draw_button("Back", 1100, 750, 80, 40, COLORS["Red"], lambda: self.level_menu(), 32)
        self.state = STATE_HOME

    # Level 3: Implement the Orange Ghost using the Uniform-Cost Search algorithm to chase Pac-Man.
    def level_3(self): 
        self.offset = 100
        self.draw_board1()
        self.board = copy.deepcopy(boards1) #check ghost và player board trỏ cùng vị trí vs board game chưa
        self.player.map = copy.deepcopy(boards1)

        self.player.offset = 100
        self.player.update_position(self.offset + 26 * 21, self.offset + 26 * 21)
        self.player.appear()

        self.orange_ghost.map = copy.deepcopy(boards1)
        self.orange_ghost.offset = 100
        self.orange_ghost.update_position(self.offset + CELL_SIZE, self.offset + CELL_SIZE)
        self.orange_ghost.target = [self.player.x_pos, self.player.y_pos]
        print((self.orange_ghost.target[1], self.orange_ghost.target[0]))

        path = self.orange_ghost.move_ucs()
        self.orange_ghost.draw_path()

        font = pygame.font.SysFont("timesnewroman", 50, bold = True)
        level_text = font.render(f"Level {self.level}", True, COLORS["Pink"])
        self.screen.blit(level_text, (900, 20))
        

        font1 = pygame.font.SysFont("timesnewroman", 32)
        time_text = font1.render(f"Search Time: 0.00 s", True, COLORS["White"]) 
        self.screen.blit(time_text, (830, 120))

        memory_text = font1.render(f"Memory Usage: 0 MB", True, COLORS["White"]) 
        self.screen.blit(memory_text, (830, 180))

        expanded_nodes_text = font1.render(f"Expanded Nodes: 0", True, COLORS["White"])  
        self.screen.blit(expanded_nodes_text, (830, 240))
        self.draw_button("Back", 1100, 750, 80, 40, COLORS["Red"], lambda: self.level_menu(), 32)
        self.state = STATE_HOME
    # Level 4: Implement the Red Ghost using the A* Search (A*) algorithm to chase Pac-Man.
    def level_4(self): 
        self.offset = 100
        self.draw_board1()
        self.board = copy.deepcopy(boards1) #check ghost và player board trỏ cùng vị trí vs board game chưa
        self.player.map = copy.deepcopy(boards1)

        self.player.offset = 100
        self.player.update_position(self.offset + 26 * 21, self.offset + 26 * 21)
        self.player.appear()

        self.red_ghost.map = copy.deepcopy(boards1)
        self.red_ghost.offset = 100
        self.red_ghost.update_position(self.offset + CELL_SIZE, self.offset + CELL_SIZE)
        self.red_ghost.target = [self.player.x_pos, self.player.y_pos]
        print((self.red_ghost.target[1], self.red_ghost.target[0]))

        path = self.red_ghost.move_astar()
        self.red_ghost.draw_path()

        font = pygame.font.SysFont("timesnewroman", 50, bold = True)
        level_text = font.render(f"Level {self.level}", True, COLORS["Pink"])
        self.screen.blit(level_text, (900, 20))
        

        font1 = pygame.font.SysFont("timesnewroman", 32)
        time_text = font1.render(f"Search Time: 0.00 s", True, COLORS["White"]) 
        self.screen.blit(time_text, (830, 120))

        memory_text = font1.render(f"Memory Usage: 0 MB", True, COLORS["White"]) 
        self.screen.blit(memory_text, (830, 180))

        expanded_nodes_text = font1.render(f"Expanded Nodes: 0", True, COLORS["White"])  
        self.screen.blit(expanded_nodes_text, (830, 240))
        self.draw_button("Back", 1100, 750, 80, 40, COLORS["Red"], lambda: self.level_menu(), 32)
        self.state = STATE_HOME
    # Level 5: Implement all ghosts (Blue, Pink, Orange, and Red) moving simultaneously in the same maze,
    # each ghost follows its respective search algorithm to chase Pac-Man and executes independently.
    def level_5(self): 
        offset_x = 100
        offset_y = 100
        self.draw_board1()
        self.board = copy.deepcopy(boards1) #check ghost và player board trỏ cùng vị trí vs board game chưa
        self.player.map = self.board

        self.player.update_position(offset_y + len(self.board[0]) * CELL_SIZE, offset_x + len(self.board) * CELL_SIZE)
        self.player.appear()

        self.blue_ghost.update_position(offset_y + CELL_SIZE, offset_x + CELL_SIZE)
        self.blue_ghost.target = (self.player.x_pos, self.player.y_pos)
        path_blue = self.blue_ghost.move_bfs()

        self.pink_ghost.update_position(offset_y + CELL_SIZE, offset_x + CELL_SIZE)
        self.pink_ghost.target = (self.player.x_pos, self.player.y_pos)
        paht_pink = self.pink_ghost.move_dfs()

        self.red_ghost.update_position(offset_y + CELL_SIZE, offset_x + CELL_SIZE)
        self.red_ghost.target = (self.player.x_pos, self.player.y_pos)
        path_red = self.red_ghost.move_astar()

        self.orange_ghost.update_position(offset_y + CELL_SIZE, offset_x + CELL_SIZE)
        self.orange_ghost.target = (self.player.x_pos, self.player.y_pos)
        path_orange = self.orange_ghost.move_ucs()

        font = pygame.font.SysFont("timesnewroman", 50, bold = True)
        level_text = font.render(f"Level {self.level}", True, COLORS["Pink"])
        self.screen.blit(level_text, (900, 20))

        font1 = pygame.font.SysFont("timesnewroman", 32)
        time_text = font1.render(f"Search Time: 0.00 s", True, COLORS["White"]) 
        self.screen.blit(time_text, (830, 120))

        memory_text = font1.render(f"Memory Usage: 0 MB", True, COLORS["White"]) 
        self.screen.blit(memory_text, (830, 180))

        expanded_nodes_text = font1.render(f"Expanded Nodes: 0", True, COLORS["White"])  
        self.screen.blit(expanded_nodes_text, (830, 240))
    # Level 6: Enable interactive game-play by allowing the player to control Pac-Man’s movement while
    # the ghosts actively chase him.
    def level_6(self): ...
    def win(self): ...
    # def draw_path(self):
    #     for x, y in self.path:
    #         self.x_pos = x
    #         self.y_pos = y
    #         screen.fill((0, 0, 0))  
    #         draw_board1() 
    #         print((x, y))
    #         screen.blit(self.img, (self.y_pos * CELL_SIZE + self.offset, self.x_pos * CELL_SIZE + self.offset))  
    #         pygame.display.update()
    #         time.sleep(0.5)
            

    def run(self): 
        running = True
        while running:
            self.screen.fill("black")
            if(self.state == STATE_HOME):
                self.home_screen()
            if(self.state == STATE_LEVEL):
                self.level_menu()
            if(self.state == STATE_PLAYING):
                self.launch_game(self.level)
            if(self.state == STATE_WIN):
                self.win()
            # if(self.state == STATE_DRAW_1):
            #     self.draw_path()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            pygame.display.flip()  # Cập nhật màn hình
        pygame.quit()
