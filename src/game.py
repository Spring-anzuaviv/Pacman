from specification import *
from pacman import *
from ghost import *
import time
import tracemalloc
import pygame
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
        self.expanded_nodes = 0
        self.elapsed_time = 0
        self.memory_usage = 0
        self.powerup_time = 0

        self.player = Player(game = self, x_coord = 10 + 26, y_coord = 10 + 26, x_target= 10 +26, y_target= 10+26, speed = 2, direct="", dead=False, powerup=False, board=self.board, board_offset = 0)
        self.pink_ghost = Ghost(game = self, x_coord = 26 , y_coord = 26, next_x = 26 , next_y = 26, target = [26 * 20, 26 * 19], speed = 2, img=GHOST_PINK, direct=0, dead=False, powerup=False, board=self.board, board_offset = 0)
        self.blue_ghost = Ghost(game = self, x_coord = 26 , y_coord = 26, next_x = 26 , next_y = 26, target = [26 * 20, 26 * 19], speed = 2, img=GHOST_BLUE, direct=0, dead=False, powerup=False, board=self.board, board_offset = 0)
        self.orange_ghost = Ghost(game = self, x_coord = 26 , y_coord = 26, next_x = 26 , next_y = 26, target = [26 * 20, 26 * 19], speed = 2, img=GHOST_YELLOW, direct=0, dead=False, powerup=False, board=self.board, board_offset = 0)
        self.red_ghost = Ghost(game = self, x_coord = 26 , y_coord = 26, next_x = 26 , next_y = 26, target = [26 * 20, 26 * 19], speed = 2, img=GHOST_RED, direct=0, dead=False, powerup=False, board=self.board, board_offset = 0)


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
        self.draw_button("Level 1", 480, 120, 270, 50, COLORS["Pink"], lambda: self.set_state(STATE_PLAYING, 1), 50)
        self.draw_button("Level 2", 480, 220, 270, 50, COLORS["Green"], lambda: self.set_state(STATE_PLAYING, 2), 50)
        self.draw_button("Level 3", 480, 320, 270, 50, COLORS["Blue"], lambda: self.set_state(STATE_PLAYING, 3), 50)
        self.draw_button("Level 4", 480, 420, 270, 50, COLORS["Yellow"], lambda: self.set_state(STATE_PLAYING, 4), 50)
        self.draw_button("Level 5", 480, 520, 270, 50, COLORS["BACKGROUND_BLUE"], lambda: self.set_state(STATE_PLAYING, 5), 50)
        self.draw_button("Level 6", 480, 620, 270, 50, COLORS["Purple"], lambda: self.set_state(STATE_PLAYING, 6), 50)
        self.draw_button("Back", 20, 20, 80, 40, COLORS["Red"], lambda: self.exit_level_menu(), 32) 

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

    def reset_ghost(self, ghost):
        ghost.x_pos = ghost.x_pos
        ghost.y_pos = ghost.y_pos
        ghost.target = [26 * 20, 26 * 19]
        ghost.speed = 2
        ghost.dead = False
        ghost.powerup = False
        ghost.direct = 0 

    def reset_player(self):
        self.player.x_pos = self.player.x_pos
        self.player.y_pos = self.player.y_pos
        self.player.dead = False
        self.player.powerup = False
        self.player.direct = "" 


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
        self.search_time, self.expanded_nodes, self.memory_usage = self.blue_ghost.time, self.blue_ghost.expanded, self.blue_ghost.mem
        self.blue_ghost.draw_path()
        self.state = STATE_RESULT

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

        path = self.pink_ghost.move_dfs()
        self.search_time, self.expanded_nodes, self.memory_usage = self.pink_ghost.time, self.pink_ghost.expanded, self.pink_ghost.mem
        self.pink_ghost.draw_path()
        self.state = STATE_RESULT

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
        self.search_time, self.expanded_nodes, self.memory_usage = self.orange_ghost.time, self.orange_ghost.expanded, self.orange_ghost.mem
        self.orange_ghost.draw_path()
        self.state = STATE_RESULT

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
        self.search_time, self.expanded_nodes, self.memory_usage = self.red_ghost.time, self.red_ghost.expanded, self.red_ghost.mem
        self.red_ghost.draw_path()
        self.state = STATE_RESULT

    # Level 5: Implement all ghosts (Blue, Pink, Orange, and Red) moving simultaneously in the same maze,
    # each ghost follows its respective search algorithm to chase Pac-Man and executes independently.

    def level_5(self): 
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
        path_blue = self.blue_ghost.move_bfs()

        self.pink_ghost.map = copy.deepcopy(boards1)
        self.pink_ghost.offset = 100
        self.pink_ghost.update_position(self.offset + CELL_SIZE * 21, self.offset + CELL_SIZE)
        self.pink_ghost.target = [self.player.x_pos, self.player.y_pos]
        path_pink = self.pink_ghost.move_dfs()

        self.red_ghost.map = copy.deepcopy(boards1)
        self.red_ghost.offset = 100
        self.red_ghost.update_position(self.offset + CELL_SIZE, self.offset + CELL_SIZE * 21)
        self.red_ghost.target = [self.player.x_pos, self.player.y_pos]
        path_red = self.red_ghost.move_astar()

        self.orange_ghost.map = copy.deepcopy(boards1)
        self.orange_ghost.offset = 100
        self.orange_ghost.update_position(self.offset + CELL_SIZE * 10, self.offset + CELL_SIZE * 11) #Middle
        self.orange_ghost.target = [self.player.x_pos, self.player.y_pos]
        path_orange = self.orange_ghost.move_ucs()

        paths = [path_blue, path_pink, path_orange, path_red]
        print(path_blue, path_orange, path_pink, path_red)
        max_length = 0
        path = []
        for path in paths:
            max_length = max(len(path), max_length)   # Tìm đường đi dài nhất
        step = 0  # Bước hiện tại

        while step < max_length:
            self.screen.fill("black")  
            self.draw_board1()  
            self.screen.blit(PACMAN_LEFT_1, (self.blue_ghost.target[0], self.blue_ghost.target[1])) 

            # Vẽ từng ghost tại bước hiện tại
            if step < len(paths[0]):
                self.blue_ghost.update_position(paths[0][step][1] * CELL_SIZE + self.offset, paths[0][step][0]* CELL_SIZE + self.offset)
            if step < len(paths[1]):
                self.pink_ghost.update_position(paths[1][step][1]* CELL_SIZE + self.offset, paths[1][step][0]* CELL_SIZE + self.offset)
            if step < len(paths[2]):
                self.orange_ghost.update_position(paths[2][step][1]* CELL_SIZE + self.offset, paths[2][step][0]* CELL_SIZE + self.offset)
            if step < len(paths[3]):
                self.red_ghost.update_position(paths[3][step][1]* CELL_SIZE + self.offset, paths[3][step][0]* CELL_SIZE + self.offset)

            #Chỉnh lại nếu = goal thì ko vẽ
            self.blue_ghost.draw()
            time.sleep(0.1)
            self.red_ghost.draw()
            time.sleep(0.1)
            self.pink_ghost.draw()
            time.sleep(0.1)
            self.orange_ghost.draw()
            time.sleep(0.1)
            pygame.display.update()

            step += 1

        self.state = STATE_RESULT_4

    # Level 6: Enable interactive game-play by allowing the player to control Pac-Man’s movement while
    # the ghosts actively chase him.

    def level_6(self): 
        self.offset = 10
        temp = copy.deepcopy(boards2)
        self.draw_board2(boards2)
        self.board = temp
        self.player.map = temp

        self.player.offset = 10
        self.player.update_position(self.offset + 26 * 21, self.offset + 26 * 21)
        self.player.appear()

        self.blue_ghost.map = self.board
        self.blue_ghost.offset = 10
        self.blue_ghost.update_position(self.offset + CELL_SIZE, self.offset + CELL_SIZE)
        self.blue_ghost.target = (self.player.x_pos, self.player.y_pos)
        path_blue = self.blue_ghost.move_bfs()

        self.pink_ghost.map = self.board
        self.pink_ghost.offset = 10
        self.pink_ghost.update_position(self.offset + CELL_SIZE * 21, self.offset + CELL_SIZE)
        self.pink_ghost.target = (self.player.x_pos, self.player.y_pos)
        path_pink = self.pink_ghost.move_dfs()

        self.red_ghost.map = self.board
        self.red_ghost.offset = 10
        self.red_ghost.update_position(self.offset + CELL_SIZE, self.offset + CELL_SIZE * 21)
        self.red_ghost.target = (self.player.x_pos, self.player.y_pos)
        path_red = self.red_ghost.move_astar()

        self.orange_ghost.map = self.board
        self.orange_ghost.offset = 10
        self.orange_ghost.update_position(self.offset + CELL_SIZE * 10, self.offset + CELL_SIZE * 11) #Middle
        self.orange_ghost.target = (self.player.x_pos, self.player.y_pos)
        path_orange = self.orange_ghost.move_ucs()

        paths = [path_blue, path_pink, path_orange, path_red]
       
        running = True
        step = 0
        frame_count = 0
        frame_skip = 5
        # self.screen.blit(PACMAN_LEFT_1, (self.player.y_pos, self.player.x_pos))
        # time.sleep(0.5)
        clock = pygame.time.Clock()
        fps = 60
        while running and self.state == STATE_PLAYING:
            clock.tick(fps)
            frame_count += 1
            self.screen.fill("black")  # Xóa màn hình
            self.draw_board2(temp)  # Vẽ lại bản đồ
            # if self.check_collision():  # Kiểm tra va chạm đầu tiên
            #     self.game_over()
            #     return

            # Vẽ từng ghost tại bước hiện tại
            if frame_count % frame_skip == 0:
                step += 1
                if step < len(paths[0]):
                    self.blue_ghost.update_position(paths[0][step][1] * CELL_SIZE + self.offset, paths[0][step][0]* CELL_SIZE + self.offset)
                if step < len(paths[1]):
                    self.pink_ghost.update_position(paths[1][step][1]* CELL_SIZE + self.offset, paths[1][step][0]* CELL_SIZE + self.offset)
                if step < len(paths[2]):
                    self.orange_ghost.update_position(paths[2][step][1]* CELL_SIZE + self.offset, paths[2][step][0]* CELL_SIZE + self.offset)
                if step < len(paths[3]):
                    self.red_ghost.update_position(paths[3][step][1]* CELL_SIZE + self.offset, paths[3][step][0]* CELL_SIZE + self.offset)
            


            # Vẽ từng ghost tại bước hiện tại 
            self.blue_ghost.draw()
            self.pink_ghost.draw() #dfs
            self.orange_ghost.draw() #ucs
            self.red_ghost.draw()

            # Xử lý sự kiện bàn phím (Pac-Man di chuyển)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.player.update_direction(event)

            self.player.move()
            self.player.eat_food()

            # Power up
            if(self.player.powerup == True):
                self.blue_ghost.powerup = True
                self.pink_ghost.powerup = True
                self.orange_ghost.powerup = True
                self.red_ghost.powerup = True

            # Nếu Pac-Man di chuyển, tính lại BFS / DFS / A* / UCS
            new_target = [self.player.x_pos, self.player.y_pos]
            if new_target != self.blue_ghost.target:  # Kiểm tra nếu vị trí thay đổi
                self.blue_ghost.target = new_target
                self.pink_ghost.target = new_target
                self.orange_ghost.target = new_target
                self.red_ghost.target = new_target

                path_blue = self.blue_ghost.move_bfs()
                path_pink = self.pink_ghost.move_dfs()
                path_red = self.red_ghost.move_astar()
                path_orange = self.orange_ghost.move_ucs()
                max_length = 0
                paths = [path_blue, path_pink, path_orange, path_red]

                for path in paths:
                    max_length = max(len(path), max_length)   # Tìm đường đi dài nhất
                step = 0

            if step >= max_length:
                step = 0  # Reset bước đi để vẽ lại từ đầu
                
            if ((self.player.x_pos, self.player.y_pos) == (self.blue_ghost.x_pos, self.blue_ghost.y_pos) or
            (self.player.x_pos, self.player.y_pos) == (self.pink_ghost.x_pos, self.pink_ghost.y_pos) or
            (self.player.x_pos, self.player.y_pos) == (self.orange_ghost.x_pos, self.orange_ghost.y_pos) or
            (self.player.x_pos, self.player.y_pos) == (self.red_ghost.x_pos, self.red_ghost.y_pos)):
                if(self.player.powerup == False):
                    if(self.player.lives == 0):
                        self.state = STATE_GAMEOVER
                        return
                    if(self.player.powerup == False):
                        self.player.lives -= 1
                        time.sleep(0.1)
                        self.blue_ghost.update_position(self.offset + CELL_SIZE, self.offset + CELL_SIZE)
                        self.pink_ghost.update_position(self.offset + CELL_SIZE * 21, self.offset + CELL_SIZE)
                        self.red_ghost.update_position(self.offset + CELL_SIZE, self.offset + CELL_SIZE * 21)
                        self.orange_ghost.update_position(self.offset + CELL_SIZE * 10, self.offset + CELL_SIZE * 11) #Middle
                else:
                        if((self.player.x_pos, self.player.y_pos) == (self.blue_ghost.x_pos, self.blue_ghost.y_pos)):
                            self.blue_ghost.dead = True
                            self.player.score += 50
                            self.screen.blit(BG_IMG, (self.blue_ghost.x_pos, self.blue_ghost.y_pos))
                            self.blue_ghost.draw()
                            time.sleep(0.1)
                            self.blue_ghost.update_position(self.offset + CELL_SIZE, self.offset + CELL_SIZE)
                            self.blue_ghost.dead = False

                        elif((self.player.x_pos, self.player.y_pos) == (self.red_ghost.x_pos, self.red_ghost.y_pos)):
                            self.red_ghost.dead = True
                            self.player.score += 50
                            self.screen.blit(BG_IMG, (self.red_ghost.x_pos, self.red_ghost.y_pos))
                            self.red_ghost.draw()
                            self.red_ghost.update_position(self.offset + CELL_SIZE, self.offset + CELL_SIZE)
                            self.red_ghost.dead = False
                        elif((self.player.x_pos, self.player.y_pos) == (self.orange_ghost.x_pos, self.orange_ghost.y_pos)):
                            self.orange_ghost.dead = True
                            self.player.score += 50
                            self.screen.blit(BG_IMG, (self.orange_ghost.x_pos, self.orange_ghost.y_pos))
                            self.orange_ghost.draw()
                            self.orange_ghost.update_position(self.offset + CELL_SIZE, self.offset + CELL_SIZE)
                            self.orange_ghost.dead = False
                        elif((self.player.x_pos, self.player.y_pos) == (self.pink_ghost.x_pos, self.pink_ghost.y_pos)):
                            self.pink_ghost.dead = True
                            self.player.score += 50
                            self.screen.blit(BG_IMG, (self.pink_ghost.x_pos, self.pink_ghost.y_pos))
                            self.pink_ghost.draw()
                            self.pink_ghost.update_position(self.offset + CELL_SIZE, self.offset + CELL_SIZE)
                            self.pink_ghost.dead = False

            if(self.check_win()):
                self.state = STATE_WIN
            
            print(time.time() - self.player.powerup_time)
            if self.player.powerup and time.time() - self.player.powerup_time >= 7:
                print("Out of time")
                self.player.powerup = False
                self.blue_ghost.powerup = False
                self.pink_ghost.powerup = False
                self.orange_ghost.powerup = False
                self.red_ghost.powerup = False

            #for i in range self.lives: vẽ mạng vô đây
                
            pygame.display.update()
            pygame.time.delay(100)  # Tốc độ di chuyển

        self.state = STATE_HOME

    """Kiểm tra nếu Pac-Man chạm vào ma"""
    def check_collision(self): 
        # for ghost in [self.blue_ghost, self.pink_ghost, self.orange_ghost, self.red_ghost]:
        #     if abs(self.player.x_pos - ghost.x_pos) < CELL_SIZE // 2 and abs(self.player.y_pos - ghost.y_pos) < CELL_SIZE // 2:
        #         return True  # Pac-Man bị bắt
        pac_rect = pygame.Rect(self.player.x_pos, self.player.y_pos, CELL_SIZE, CELL_SIZE)
    
        for ghost in [self.blue_ghost, self.pink_ghost, self.orange_ghost, self.red_ghost]:
            ghost_rect = pygame.Rect(ghost.x_pos, ghost.y_pos, CELL_SIZE, CELL_SIZE)
            
            if pac_rect.colliderect(ghost_rect):  # Check if Pac-Man and ghost collide
                return True  
        return False
    
    """Kiểm tra nếu Pac-Man đã ăn hết tất cả pellet"""
    def check_win(self):
        for row in self.board:
            if 2 in row or 3 in row: 
                return False  
        return True  

    def win(self): 
        self.state = STATE_WIN
        self.screen.fill((0, 0, 0))  # Đặt nền màu đen
        font = pygame.font.SysFont("timesnewroman", 50, bold=True)
        win_text = font.render("YOU WIN!", True, (255, 255, 0))
        self.screen.blit(EMOJI_WIN_1, (425, 345))
        self.screen.blit(EMOJI_WIN_2, (725, 345))
        self.screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - 50))
        
        sub_font = pygame.font.SysFont("timesnewroman", 40)
        play_again_text = sub_font.render("Press Y to Play Again", True, COLORS["Yellow"])
        menu_text = sub_font.render("Press N to Go to Level Menu", True, COLORS["Yellow"])

        play_again_rect = play_again_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 50))
        menu_rect = menu_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 100))

        self.screen.blit(play_again_text, play_again_rect)
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
        

    """bị sai chỗ Y quay lại màn hình cho chạy"""
    def show_result(self):
        self.screen.fill(COLORS["Black"])
        pygame.draw.rect(self.screen, (0, 0, 0, 150), (50, 50, WIDTH - 100, HEIGHT - 150), border_radius=20)
        font = pygame.font.SysFont("timesnewroman", 50, bold=True)
        level_text = font.render(f"Level {self.level} Complete!", True, COLORS["Pink"])
        self.screen.blit(level_text, (WIDTH // 2 - level_text.get_width() // 2, 100))

        font1 = pygame.font.SysFont("timesnewroman", 32)
        time_text = font1.render(f"Search Time: {self.search_time} s", True, COLORS["White"])
        self.screen.blit(time_text, (WIDTH // 2 - time_text.get_width() // 2, 180))

        memory_text = font1.render(f"Memory Usage: {self.memory_usage} bytes", True, COLORS["White"])
        self.screen.blit(memory_text, (WIDTH // 2 - memory_text.get_width() // 2, 230))

        expanded_nodes_text = font1.render(f"Expanded Nodes: {self.expanded_nodes}", True, COLORS["White"])
        self.screen.blit(expanded_nodes_text, (WIDTH // 2 - expanded_nodes_text.get_width() // 2, 280))

        sub_font = pygame.font.SysFont("timesnewroman", 40)
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


    def game_over(self):
        self.screen.fill((0, 0, 0))  # Đặt nền màu đen
        font = pygame.font.SysFont("timesnewroman", 50, bold=True)
        text = font.render("GAME OVER", True, COLORS["Red"])
        self.screen.blit(EMOJI_LOSE, (390, 360))
        self.screen.blit(EMOJI_LOSE, (760, 360))
        self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 50))
        
        sub_font = pygame.font.SysFont("timesnewroman", 40)
        play_again_text = sub_font.render("Press Y to Play Again", True, COLORS["Yellow"])
        menu_text = sub_font.render("Press N to Go to Level Menu", True, COLORS["Yellow"])

        play_again_rect = play_again_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 50))
        menu_rect = menu_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 100))

        self.screen.blit(play_again_text, play_again_rect)
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
        

    
    def reset_game(self):
    # Đặt lại vị trí Pac-Man
        self.reset_player()

        # Đặt lại vị trí của tất cả các Ghost
        self.reset_ghost(self.blue_ghost)
        self.reset_ghost(self.pink_ghost)
        self.reset_ghost(self.red_ghost)
        self.reset_ghost(self.orange_ghost)

        # Đặt lại điểm số, trạng thái game nếu cần
        self.expanded_nodes = 0
        self.search_time = 0
        self.memory_usage = 0

    def show_result_for_four(self):
        ...

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

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            pygame.display.flip() 
        pygame.quit()
