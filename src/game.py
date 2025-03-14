from specification import *
from pacman import *
from ghost import *
import time
import tracemalloc
import pygame
import random

class Game:
    def __init__(self): 
    # Menu screen
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(APP_CAPTION)
        self.font = pygame.font.Font("PressStart2P.ttf", 25)
        self.background_image1 = pygame.image.load(MENU_LOGO_1)
        self.background_image2 = pygame.image.load(MENU_LOGO_2)
        self.background_image1 = pygame.transform.scale(self.background_image1, (WIDTH//2.2, HEIGHT//2.2))
        self.background_image2 = pygame.transform.scale(self.background_image2, (WIDTH//1.8, HEIGHT//3))
        self.state = "home"
        self.level = 0
        self.board = []
        self.path = []
        self.img = None
        self.offset = (0, 0)
        self.expanded_nodes = 0
        self.search_time = 0
        self.memory_usage = 0
        self.powerup_time = 0

        self.player = Player(game = self, x_coord = 10 + 26, y_coord = 10 + 26, x_target= 10 +26, y_target= 10+26, speed = 2, direct="", dead=False, powerup=False, board=self.board, board_offset=(0,0))
        self.pink_ghost = Ghost(game = self, x_coord = 26 , y_coord = 26, next_x = 26 , next_y = 26, target = [26 * 20, 26 * 19], speed = 2, img=GHOST_PINK, direct=0, dead=False, powerup=False, board=self.board, board_offset = (0,0))
        self.blue_ghost = Ghost(game = self, x_coord = 26 , y_coord = 26, next_x = 26 , next_y = 26, target = [26 * 20, 26 * 19], speed = 2, img=GHOST_BLUE, direct=0, dead=False, powerup=False, board=self.board, board_offset = (0,0))
        self.orange_ghost = Ghost(game = self, x_coord = 26 , y_coord = 26, next_x = 26 , next_y = 26, target = [26 * 20, 26 * 19], speed = 2, img=GHOST_ORANGE, direct=0, dead=False, powerup=False, board=self.board, board_offset = (0,0))
        self.red_ghost = Ghost(game = self, x_coord = 26 , y_coord = 26, next_x = 26 , next_y = 26, target = [26 * 20, 26 * 19], speed = 2, img=GHOST_RED, direct=0, dead=False, powerup=False, board=self.board, board_offset = (0,0))
    
        self.click_sound = pygame.mixer.Sound(MOUSE_CLICK_SOUND)
        self.win_music = pygame.mixer.Sound(WIN_MUSIC)
        self.lose_music = pygame.mixer.Sound(LOSE_MUSIC)
        self.menu_music = pygame.mixer.Sound(MENU_BG_MUSIC)
        self.die_sound = pygame.mixer.Sound(DIE_SOUND)
        self.powerup_sound = pygame.mixer.Sound(POWER_UP_SOUND)

    def draw_board1(self):
        maze_width = len(boards1[0]) * GRID_SIZE
        maze_height = len(boards1) * GRID_SIZE
        offset_x = (WIDTH - maze_width) // 2
        offset_y = (HEIGHT - maze_height) // 2

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
        font = pygame.font.Font("PressStart2P.ttf", fontsize)
        text_surface = font.render(text, True, COLORS["Black"])
        self.screen.blit(text_surface, (x + (width - text_surface.get_width()) // 2, y + (height - text_surface.get_height()) // 2))
        
        mouse_x, mouse_y = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        
        if x < mouse_x < x + width and y < mouse_y < y + height:
            if click[0] == 1 and action:
                self.click_sound.play()
                action()

    def set_state(self, new_state, new_level):
        # self.menu_music.stop()
        self.state = new_state
        if new_level:
            self.level = new_level  

    def level_menu(self):
        self.menu_music.stop()
        self.state = STATE_LEVEL
        self.screen.fill("Black")
        self.draw_button("Level 1", 480, 150, 270, 50, COLORS["Pink"], lambda: self.set_state(STATE_PLAYING, 1), 25)
        self.draw_button("Level 2", 480, 250, 270, 50, COLORS["Green"], lambda: self.set_state(STATE_PLAYING, 2), 25)
        self.draw_button("Level 3", 480, 350, 270, 50, COLORS["Blue"], lambda: self.set_state(STATE_PLAYING, 3), 25)
        self.draw_button("Level 4", 480, 450, 270, 50, COLORS["Yellow"], lambda: self.set_state(STATE_PLAYING, 4), 25)
        self.draw_button("Level 5", 480, 550, 270, 50, COLORS["BACKGROUND_BLUE"], lambda: self.set_state(STATE_PLAYING, 5), 25)
        self.draw_button("Level 6", 480, 650, 270, 50, COLORS["Purple"], lambda: self.set_state(STATE_PLAYING, 6), 25)
        self.draw_button("Back", 20, 20, 80, 40, COLORS["Red"], lambda: self.exit_level_menu(), 15) 

        level_text = self.font.render("Choose Your Level", True, COLORS["Yellow"])
        self.screen.blit(level_text, (WIDTH // 2 - level_text.get_width() // 2, 50))   

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
        elif self.level == 6:
            self.level_6()

    def exit_level_menu(self):
        # self.menu_music.stop()
        self.state = "home"
        global screen_running
        screen_running = False
        self.home_screen()
    
    def exit_game(self):
        pygame.quit()
        sys.exit()

    def home_screen(self):
        self.menu_music.play()
        self.screen.blit(self.background_image1, (350, 30))
        self.screen.blit(self.background_image2, (320, 380))
        self.draw_button("START GAME", 100, 650, 270, 60, COLORS["Green"], self.level_menu, 23)
        self.draw_button("HOW TO PLAY", 445, 650, 330, 60, COLORS["Yellow"], self.how_to_play_screen, 25)
        self.draw_button("EXIT", 850, 650, 270, 60, COLORS["Red"], self.exit_game, 25)

    def reset_player(self):
        self.player.x_pos = self.player.offset[0] + CELL_SIZE
        self.player.y_pos = self.player.offset[1] + CELL_SIZE
        self.player.dead = False
        self.player.powerup = False
        self.player.direction = "" 
        self.player.lives = 3
        self.player.score = 0
        self.player.last_move_time = 0
        self.player.open_mouth = False

    def reset_game(self):
        self.offset = boards1_offset
        self.board = copy.deepcopy(boards1) #check ghost và player board trỏ cùng vị trí vs board game chưa
        self.player.map = copy.deepcopy(boards1)

        self.player.offset = boards1_offset
        self.player.update_position(self.offset[0] + 26, self.offset[1] + 26)
       
    ''' Level 1:  Implement the Blue Ghost using Breadth-First Search (BFS) algorithm to chase Pac-Man '''
    def level_1(self):
        self.offset = boards1_offset
        self.draw_board1()
        self.board = copy.deepcopy(boards1) #check ghost và player board trỏ cùng vị trí vs board game chưa
        self.player.map = copy.deepcopy(boards1)

        self.player.offset = boards1_offset
        self.player.update_position(self.offset[0] + 26 * 21, self.offset[1] + 26 * 21)
        self.player.appear()

        self.blue_ghost.map = copy.deepcopy(boards1)
        self.blue_ghost.offset = boards1_offset
        self.blue_ghost.update_position(self.offset[0] + CELL_SIZE * 1, self.offset[1] + CELL_SIZE * 1)
        self.blue_ghost.target = [self.player.x_pos, self.player.y_pos]
        print((self.blue_ghost.target[1], self.blue_ghost.target[0]))

        path = self.blue_ghost.move_bfs()
        self.search_time, self.expanded_nodes, self.memory_usage = self.blue_ghost.time, self.blue_ghost.expanded, self.blue_ghost.mem
        self.blue_ghost.draw_path()
        
        self.state = STATE_RESULT

    ''' Level 2: Implement the Pink Ghost using the Depth-First Search (DFS) algorithm to chase Pac-Man. '''
    def level_2(self): 
        self.offset = boards1_offset
        self.draw_board1()
        self.board = copy.deepcopy(boards1) 
        self.player.map = copy.deepcopy(boards1)

        self.player.offset = boards1_offset
        self.player.update_position(self.offset[0] + 26 * 21, self.offset[1] + 26 * 21)
        self.player.appear()

        self.pink_ghost.map = copy.deepcopy(boards1)
        self.pink_ghost.offset = boards1_offset
        self.pink_ghost.update_position(self.offset[0] + CELL_SIZE, self.offset[1] + CELL_SIZE)
        self.pink_ghost.target = [self.player.x_pos, self.player.y_pos]

        path = self.pink_ghost.move_dfs()
        self.search_time, self.expanded_nodes, self.memory_usage = self.pink_ghost.time, self.pink_ghost.expanded, self.pink_ghost.mem
        self.pink_ghost.draw_path()
        self.state = STATE_RESULT

    ''' Level 3: Implement the Orange Ghost using the Uniform-Cost Search algorithm to chase Pac-Man '''
    def level_3(self): 
        self.offset = boards1_offset
        self.draw_board1()
        self.board = copy.deepcopy(boards1) #check ghost và player board trỏ cùng vị trí vs board game chưa
        self.player.map = copy.deepcopy(boards1)

        self.player.offset = boards1_offset
        self.player.update_position(self.offset[0] + 26 * 21, self.offset[1] + 26 * 21)
        self.player.appear()

        self.orange_ghost.map = copy.deepcopy(boards1)
        self.orange_ghost.offset = boards1_offset
        self.orange_ghost.update_position(self.offset[0] + CELL_SIZE, self.offset[1] + CELL_SIZE)
        self.orange_ghost.target = [self.player.x_pos, self.player.y_pos]
        print((self.orange_ghost.target[1], self.orange_ghost.target[0]))

        path = self.orange_ghost.move_ucs()
        self.search_time, self.expanded_nodes, self.memory_usage = self.orange_ghost.time, self.orange_ghost.expanded, self.orange_ghost.mem
        self.orange_ghost.draw_path()
        self.state = STATE_RESULT

    ''' Level 4: Implement the Red Ghost using the A* Search (A*) algorithm to chase Pac-Man '''
    def level_4(self): 
        self.offset = boards1_offset
        self.draw_board1()
        self.board = copy.deepcopy(boards1) #check ghost và player board trỏ cùng vị trí vs board game chưa
        self.player.map = copy.deepcopy(boards1)

        self.player.offset = boards1_offset
        self.player.update_position(self.offset[0] + 26 * 21, self.offset[1] + 26 * 21)
        self.player.appear()

        self.red_ghost.map = copy.deepcopy(boards1)
        self.red_ghost.offset = boards1_offset
        self.red_ghost.update_position(self.offset[0] + CELL_SIZE, self.offset[1] + CELL_SIZE)
        self.red_ghost.target = [self.player.x_pos, self.player.y_pos]
        print((self.red_ghost.target[1], self.red_ghost.target[0]))

        path = self.red_ghost.move_astar()
        self.search_time, self.expanded_nodes, self.memory_usage = self.red_ghost.time, self.red_ghost.expanded, self.red_ghost.mem
        self.red_ghost.draw_path()
        self.state = STATE_RESULT

    ''' Level 5: Implement all ghosts (Blue, Pink, Orange, and Red) moving simultaneously in the same maze,
     each ghost follows its respective search algorithm to chase Pac-Man and executes independently. '''

    def level_5(self): 
        self.offset = boards1_offset
        self.draw_board1()
        
        self.board = copy.deepcopy(boards1)
        self.player.map = copy.deepcopy(boards1)
        self.player.offset = boards1_offset
        self.player.update_position(self.offset[0] + 26 * 21, self.offset[1] + 26 * 21)

        ghosts = [
            {"ghost": self.blue_ghost, "pos": (1, 1), "move_func": self.blue_ghost.move_bfs},
            {"ghost": self.pink_ghost, "pos": (21, 1), "move_func": self.pink_ghost.move_dfs},
            {"ghost": self.red_ghost, "pos": (1, 21), "move_func": self.red_ghost.move_astar},
            {"ghost": self.orange_ghost, "pos": (10, 11), "move_func": self.orange_ghost.move_ucs},
        ]
        
        paths = []
        for data in ghosts:
            ghost = data["ghost"]
            ghost.map = copy.deepcopy(boards1)
            ghost.offset = boards1_offset
            ghost.update_position(self.offset[0] + CELL_SIZE * data["pos"][0], self.offset[1] + CELL_SIZE * data["pos"][1])
            ghost.target = [self.player.x_pos, self.player.y_pos]
            paths.append(data["move_func"]()) 

        max_length = max(len(path) for path in paths)
        step = 0  

        while step < max_length:
            self.screen.fill("black")  
            self.draw_board1()  
            self.screen.blit(PACMAN_LEFT_1, (self.blue_ghost.target[0], self.blue_ghost.target[1])) 
            for i, data in enumerate(ghosts):
                ghost = data["ghost"]
                if step < len(paths[i]):
                    ghost.update_position(paths[i][step][1] * CELL_SIZE + self.offset[0], paths[i][step][0] * CELL_SIZE + self.offset[1])
                
                if not ghost.check_collision():
                    ghost.draw()
                time.sleep(0.1)

            # Exit
            button_rect = pygame.Rect(20, 20, 190, 35)

            pygame.draw.rect(self.screen, (200, 0, 0), button_rect) 
            font = pygame.font.Font("PressStart2P.ttf", 15)
            text = font.render("See result", True, (0, 0, 0))  
            self.screen.blit(text, (button_rect.x + 20, button_rect.y + 10))
 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(event.pos): 
                        self.click_sound.play()
                        step = 2**31
            pygame.display.update()
            step += 1

        self.state = STATE_RESULT_4


    ''' Level 6: Enable interactive game-play by allowing the player to control Pac-Man’s movement while
    the ghosts actively chase him. '''
    def level_6(self): 
        self.reset_player()
        self.offset = (10, 10)
        temp = copy.deepcopy(boards2)
        self.draw_board2(boards2)
        self.board = temp
        self.player.map = temp
        self.player.offset = (10, 10)
        self.player.update_position(self.offset[0] + CELL_SIZE, self.offset[1] + CELL_SIZE)
        self.player.appear()

        ghosts = [
            {"ghost": self.blue_ghost, "pos": (1, 27), "method": self.blue_ghost.move_bfs},
            {"ghost": self.pink_ghost, "pos": (31, 27), "method": self.pink_ghost.move_dfs},
            {"ghost": self.red_ghost, "pos": (31, 1), "method": self.red_ghost.move_astar},
            {"ghost": self.orange_ghost, "pos": (15, 17), "method": self.orange_ghost.move_ucs}
        ]

        for ghost_data in ghosts:
            ghost = ghost_data["ghost"]
            x, y = ghost_data["pos"]
            ghost.map = self.board
            ghost.offset = (10, 10)
            ghost.update_position(self.offset[0] + CELL_SIZE * x, self.offset[1] + CELL_SIZE * y)
            ghost.target = (self.player.x_pos, self.player.y_pos)

        paths = [ghost_data["method"]() for ghost_data in ghosts]

        running = True
        step = 0
        frame_count = 0
        frame_skip = 5
        clock = pygame.time.Clock()
        fps = 60
        
        while running and self.state == STATE_PLAYING:
            clock.tick(fps)
            frame_count += 1
            self.screen.fill("black")  
            self.draw_board2(temp)  

            if frame_count % frame_skip == 0:
                step += 1
                for i, ghost_data in enumerate(ghosts):
                    if step < len(paths[i]):
                        ghost = ghost_data["ghost"]
                        x, y = paths[i][step]
                        ghost.update_position(y * CELL_SIZE + self.offset[0], x * CELL_SIZE + self.offset[1])

            for ghost_data in ghosts:
                ghost_data["ghost"].draw()

            #Player move
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.player.update_direction(event)

            self.player.move()
            self.player.eat_food()

            # Power-up logic
            if self.player.powerup:
                for ghost_data in ghosts:
                    ghost_data["ghost"].powerup = True

            new_target = [self.player.x_pos, self.player.y_pos]
            if new_target != ghosts[0]["ghost"].target:
                for ghost_data in ghosts:
                    ghost_data["ghost"].target = new_target
                paths = [ghost_data["method"]() for ghost_data in ghosts]
                max_length = max(len(path) for path in paths)
                step = 0

            if step >= max_length:
                step = 0  # Reset bước đi để vẽ lại từ đầu

            for ghost_data in ghosts:
                ghost = ghost_data["ghost"]
                if (self.player.x_pos, self.player.y_pos) == (ghost.x_pos, ghost.y_pos):
                    if not self.player.powerup:
                        self.die_sound.play()
                        self.player.lives -= 1
                        if self.player.lives == 0:
                            self.state = STATE_GAMEOVER
                            return
                        time.sleep(0.8)
                        self.player.update_position(self.offset[0] + CELL_SIZE, self.offset[1] + CELL_SIZE)
                    else:
                        self.powerup_sound.play()
                        ghost.dead = True
                        self.player.score += 50
                        self.screen.blit(BG_IMG, (ghost.x_pos, ghost.y_pos))
                        ghost.draw()
                        time.sleep(0.2)
                        x, y = ghost_data["pos"]
                        ghost.update_position(self.offset[0] + CELL_SIZE * x, self.offset[1] + CELL_SIZE * y)
                        ghost.dead = False

            # Win condition check
            if self.check_win():
                self.state = STATE_WIN

            # Power-up time check
            if self.player.powerup and time.time() - self.player.powerup_time >= 7:
                self.player.powerup = False
                for ghost_data in ghosts:
                    ghost_data["ghost"].powerup = False

            # Draw lives and score
            self.draw_lives_and_score()

            # Exit
            self.draw_button("Exit", 1080, 30, 80, 40, COLORS["Red"], lambda: self.level_menu(), 15) 

            pygame.display.update()
            pygame.time.delay(100)  
        # self.state = STATE_HOME
   
    def draw_lives_and_score(self):
        font = pygame.font.Font("PressStart2P.ttf", 20)
        lives_text = font.render("Lives: ", True, COLORS["Pink"])
        self.screen.blit(lives_text, (910, 215))
        for i in range(self.player.lives):
            self.screen.blit(PACMAN_LIVE, (1040 + i * (CELL_SIZE + 5), 210))
        score_text = font.render(f"Score: {self.player.score}", True, COLORS["Pink"])
        self.screen.blit(score_text, (910, 150))
    
    def check_win(self):
        for row in self.board:
            if 2 in row or 3 in row: 
                return False  
        return True  

    def win(self): 
        self.state = STATE_WIN
        self.screen.fill((0, 0, 0))  # Đặt nền màu đen
        font = pygame.font.Font("PressStart2P.ttf", 25)
        self.win_music.play()
        win_text = font.render("YOU WIN!", True, (255, 255, 0))
        self.screen.blit(EMOJI_WIN_1, (425, 345))
        self.screen.blit(EMOJI_WIN_2, (725, 345))
        self.screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - 50))
        
        sub_font = pygame.font.Font("PressStart2P.ttf", 20)
        menu_text = sub_font.render("Press N to Go to Level Menu", True, COLORS["White"])
        menu_rect = menu_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 100))
        self.screen.blit(menu_text, menu_rect)
        
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:  
                        self.state = STATE_PLAYING
                        self.level = 6
                        return
                    elif event.key == pygame.K_n:
                        self.state = STATE_LEVEL
                        return
        
    def show_result(self):
        self.screen.fill(COLORS["Black"])
        pygame.draw.rect(self.screen, (0, 0, 0, 150), (50, 50, WIDTH - 100, HEIGHT - 150), border_radius=20)
        font = pygame.font.Font("PressStart2P.ttf", 25)
        level_text = font.render(f"Level {self.level} Complete!", True, COLORS["Pink"])
        self.screen.blit(level_text, (WIDTH // 2 - level_text.get_width() // 2, 100))

        font1 = pygame.font.Font("PressStart2P.ttf", 20)
        time_text = font1.render(f"Search Time: {self.search_time} s", True, COLORS["White"])
        self.screen.blit(time_text, (WIDTH // 2 - time_text.get_width() // 2, 180))

        memory_text = font1.render(f"Memory Usage: {self.memory_usage} bytes", True, COLORS["White"])
        self.screen.blit(memory_text, (WIDTH // 2 - memory_text.get_width() // 2, 230))

        expanded_nodes_text = font1.render(f"Expanded Nodes: {self.expanded_nodes}", True, COLORS["White"])
        self.screen.blit(expanded_nodes_text, (WIDTH // 2 - expanded_nodes_text.get_width() // 2, 280))

        sub_font = pygame.font.Font("PressStart2P.ttf", 20)
        menu_text = sub_font.render("Press N to go to Level Menu", True, COLORS["Yellow"])
        menu_rect = menu_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
        self.screen.blit(menu_text, menu_rect)

        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_n: 
                        self.state = STATE_LEVEL
                        waiting = False

    def show_result_for_four(self):
        self.screen.fill(COLORS["Black"])
        pygame.draw.rect(self.screen, (0, 0, 0, 150), (50, 50, WIDTH - 100, HEIGHT - 150), border_radius=20)
        font = pygame.font.Font("PressStart2P.ttf", 25)
        level_text = font.render(f"Level {self.level} Complete!", True, COLORS["Yellow"])
        self.screen.blit(level_text, (WIDTH // 2 - level_text.get_width() // 2, 50))

        font1 = pygame.font.Font("PressStart2P.ttf", 20)

        time_text = font1.render(f"Search time of the Blue ghost: {self.blue_ghost.time} s", True, COLORS["Blue"])
        self.screen.blit(time_text, (WIDTH // 2 - time_text.get_width() // 2, 130))
        memory_text = font1.render(f"Memory usage of the Blue ghost: {self.blue_ghost.mem} bytes", True, COLORS["Blue"])
        self.screen.blit(memory_text, (WIDTH // 2 - memory_text.get_width() // 2, 170))
        expanded_nodes_text = font1.render(f"Expanded nodes of the Blue ghost: {self.blue_ghost.expanded}", True, COLORS["Blue"])
        self.screen.blit(expanded_nodes_text, (WIDTH // 2 - expanded_nodes_text.get_width() // 2, 210))

        time_text = font1.render(f"Search time of the Pink ghost: {self.pink_ghost.time} s", True, COLORS["Pink"])
        self.screen.blit(time_text, (WIDTH // 2 - time_text.get_width() // 2, 290))
        memory_text = font1.render(f"Memory usage of the Pink ghost: {self.pink_ghost.mem} bytes", True, COLORS["Pink"])
        self.screen.blit(memory_text, (WIDTH // 2 - memory_text.get_width() // 2, 330))
        expanded_nodes_text = font1.render(f"Expanded nodes of the Pink ghost: {self.pink_ghost.expanded}", True, COLORS["Pink"])
        self.screen.blit(expanded_nodes_text, (WIDTH // 2 - expanded_nodes_text.get_width() // 2, 370))

        time_text = font1.render(f"Search time of the Red ghost: {self.red_ghost.time} s", True, COLORS["Red"])
        self.screen.blit(time_text, (WIDTH // 2 - time_text.get_width() // 2, 450))
        memory_text = font1.render(f"Memory usage of the Red ghost: {self.red_ghost.mem} bytes", True, COLORS["Red"])
        self.screen.blit(memory_text, (WIDTH // 2 - memory_text.get_width() // 2, 490))
        expanded_nodes_text = font1.render(f"Expanded nodes of the Red ghost: {self.red_ghost.expanded}", True, COLORS["Red"])
        self.screen.blit(expanded_nodes_text, (WIDTH // 2 - expanded_nodes_text.get_width() // 2, 530))

        time_text = font1.render(f"Search time of the Orange ghost: {self.orange_ghost.time} s", True, COLORS["Orange"])
        self.screen.blit(time_text, (WIDTH // 2 - time_text.get_width() // 2, 610))
        memory_text = font1.render(f"Memory usage of the Orange ghost: {self.orange_ghost.mem} bytes", True, COLORS["Orange"])
        self.screen.blit(memory_text, (WIDTH // 2 - memory_text.get_width() // 2, 650))
        expanded_nodes_text = font1.render(f"Expanded nodes of the Orange ghost: {self.orange_ghost.expanded}", True, COLORS["Orange"])
        self.screen.blit(expanded_nodes_text, (WIDTH // 2 - expanded_nodes_text.get_width() // 2, 690))

        sub_font = pygame.font.Font("PressStart2P.ttf", 20)
        menu_text = sub_font.render("Press N to go to Level Menu", True, COLORS["Yellow"])
        menu_rect = menu_text.get_rect(center=(WIDTH // 2, HEIGHT - 70))
        self.screen.blit(menu_text, menu_rect)

        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_n: 
                        self.state = STATE_LEVEL
                        waiting = False


    def game_over(self):
        self.screen.fill((0, 0, 0))  # Đặt nền màu đen
        font = pygame.font.Font("PressStart2P.ttf", 20)
        self.lose_music.play()
        text = font.render("GAME OVER", True, COLORS["Red"])
        self.screen.blit(EMOJI_LOSE, (390, 360))
        self.screen.blit(EMOJI_LOSE, (760, 360))
        self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 50))

        score_text = font.render(f"SCORE: {self.player.score}", True, COLORS["White"])
        self.screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + 5))

        sub_font = pygame.font.Font("PressStart2P.ttf", 20)
        menu_text = sub_font.render("Press N to Go to Level Menu", True, COLORS["Yellow"])

        menu_rect = menu_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 90))
        self.screen.blit(menu_text, menu_rect)
        
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:  
                        self.reset_game()
                        self.state = STATE_PLAYING
                        return
                    elif event.key == pygame.K_n:
                        self.state = STATE_LEVEL
                        return

    def how_to_play_screen(self):
        self.menu_music.stop()
        self.state = STATE_HOW_TO_PLAY
        title_font = pygame.font.Font("PressStart2P.ttf", 30)  
        text_font = pygame.font.Font("PressStart2P.ttf", 18)   
        instructions = [
            "MOVE:",
            "Use arrow keys to move Pac-Man.",
            "  ↑ Arrow - Move Up",
            "  ↓ Arrow - Move Down",
            "  ← Arrow - Move Left",
            "  → Arrow - Move Right",
            "",
            "RULES:",
            "- Avoid ghosts or lose a life!",
            "- Eat small dots (+10 points).",
            "- Eat big dots (Power Pellet) (+30 points).",
            "  → Power-Up: Pacman can eat ghosts (+50 points).",
            "",
            "WIN: Eat all dots to clear the level.",
            "LOSE: You lose if you run out of 3 lives.",
        ]
        title_text = title_font.render(f"HOW TO PLAY", True, COLORS["Yellow"])
        self.screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))
        y_offset = 150  # Vị trí bắt đầu
        for line in instructions:
            text_surface = text_font.render(line, True, COLORS["White"])
            text_rect = text_surface.get_rect(center=(600, y_offset))  # Căn giữa nội dung
            self.screen.blit(text_surface, text_rect)
            y_offset += 40  # Khoảng cách giữa các dòng

        button_rect = pygame.Rect(20, 20, 115, 40)

        pygame.draw.rect(self.screen, (200, 0, 0), button_rect) 
        
        text = text_font.render("Back", True, COLORS["Black"])  
        self.screen.blit(text, (button_rect.x + 20, button_rect.y + 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos): 
                    self.click_sound.play()
                    self.state = STATE_HOME
        pygame.display.flip()

        
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
            if(self.state == STATE_GAMEOVER):
                self.game_over()
            if(self.state == STATE_RESULT):
                self.show_result()
            if(self.state == STATE_RESULT_4):
                self.show_result_for_four()
            if(self.state == STATE_HOW_TO_PLAY):
                self.how_to_play_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            pygame.display.flip() 
        pygame.quit()
