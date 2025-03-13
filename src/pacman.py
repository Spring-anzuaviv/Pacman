from src.specification import *

class Player:
    def __init__(self, game, x_coord, y_coord, x_target, y_target, speed, direct, dead, powerup, board, board_offset):
        self.x_pos = x_coord
        self.y_pos = y_coord
        self.game =  game
        self.direction = direct  #"left", "right", "up", "down"
        self.dead = dead
        self.map = board  
        self.powerup = powerup  # Nếu True, Pac-Man có thể ăn ma
        self.lives = 3  # Số mạng của Pac-Man
        self.score = 0  # Điểm số
        self.offset = board_offset
        self.open_mouth = False
        self.last_move_time = 0
        self.powerup_time = 0

    def appear(self):
        self.direction = "Right"
        self.draw()


    def draw(self): 
        if self.powerup:
            if self.open_mouth:
                self.open_mouth = False
                if self.direction == "Left":
                    rect = self.game.screen.blit(PACMAN_POWERUP_LEFT_1, (self.x_pos, self.y_pos))
                    pygame.display.update(rect)
                elif self.direction == "Right":
                    rect = self.game.screen.blit(PACMAN_POWERUP_RIGHT_1, (self.x_pos, self.y_pos))
                    pygame.display.update(rect)
                elif self.direction == "Up":
                    rect = self.game.screen.blit(PACMAN_POWERUP_UP_1, (self.x_pos, self.y_pos))
                    pygame.display.update(rect)
                elif self.direction == "Down":
                    rect = self.game.screen.blit(PACMAN_POWERUP_DOWN_1, (self.x_pos, self.y_pos))
                    pygame.display.update(rect)
            else:
                self.open_mouth = True
                if self.direction == "Left":
                    rect = self.game.screen.blit(PACMAN_POWERUP_LEFT_2, (self.x_pos, self.y_pos))
                    pygame.display.update(rect)
                elif self.direction == "Right":
                    rect = self.game.screen.blit(PACMAN_POWERUP_RIGHT_2, (self.x_pos, self.y_pos))
                    pygame.display.update(rect)
                elif self.direction == "Up":
                    rect = self.game.screen.blit(PACMAN_POWERUP_UP_2, (self.x_pos, self.y_pos))
                    pygame.display.update(rect)
                elif self.direction == "Down":
                    rect = self.game.screen.blit(PACMAN_POWERUP_DOWN_2, (self.x_pos, self.y_pos))
                    pygame.display.update(rect)
        else:
                if self.open_mouth:
                    self.open_mouth = False
                    if self.direction == "Left":
                        rect = self.game.screen.blit(PACMAN_LEFT_1, (self.x_pos, self.y_pos))
                        pygame.display.update(rect)
                    if self.direction == "Right":
                        rect = self.game.screen.blit(PACMAN_RIGHT_1, (self.x_pos, self.y_pos))
                        pygame.display.update(rect)
                    if self.direction == "Up":
                        rect = self.game.screen.blit(PACMAN_UP_1, (self.x_pos, self.y_pos))
                        pygame.display.update(rect)
                    if self.direction == "Down":
                        rect = self.game.screen.blit(PACMAN_DOWN_1, (self.x_pos, self.y_pos))
                        pygame.display.update(rect) 
                else:
                    self.open_mouth = True
                    if self.direction == "Left":
                        rect = self.game.screen.blit(PACMAN_LEFT_2, (self.x_pos, self.y_pos))
                        pygame.display.update(rect)
                    if self.direction == "Right":
                        rect = self.game.screen.blit(PACMAN_RIGHT_2, (self.x_pos, self.y_pos))
                        pygame.display.update(rect)
                    if self.direction == "Up":
                        rect = self.game.screen.blit(PACMAN_UP_2, (self.x_pos, self.y_pos))
                        pygame.display.update(rect)
                    if self.direction == "Down":
                        rect = self.game.screen.blit(PACMAN_DOWN_2, (self.x_pos, self.y_pos))
                        pygame.display.update(rect)
    
    def check_collision(self, x, y):
        if((0 <= (x - self.offset) // CELL_SIZE < len(self.map[0]) and 0 <= (y - self.offset) // CELL_SIZE < len(self.map) and self.map[(y - self.offset) // CELL_SIZE ][(x - self.offset) // CELL_SIZE ] == 1) 
           or (0 <= (x - self.offset) // CELL_SIZE < len(self.map[0]) and 0 <= (y - self.offset) // CELL_SIZE < len(self.map) and self.map[(y - self.offset) // CELL_SIZE ][(x - self.offset) // CELL_SIZE ] == 4)):
            return 0
        elif ((0 <= (x - self.offset) // CELL_SIZE < len(self.map[0]) and 0 <= (y - self.offset) // CELL_SIZE < len(self.map)) 
           or (0 <= (x - self.offset) // CELL_SIZE < len(self.map[0]) and 0 <= (y - self.offset) // CELL_SIZE < len(self.map))):
            return 1
        return 0
    
    def update_direction(self, event):
        """Chỉ di chuyển Pac-Man khi có sự kiện nhấn phím"""
    
        if event.type == pygame.KEYDOWN:  
            if event.key == pygame.K_LEFT:
                self.direction = "Left"
                # new_pos_x = self.x_pos - CELL_SIZE
                # new_pos_y = self.y_pos
            elif event.key == pygame.K_RIGHT:
                self.direction = "Right"
                # new_pos_x = self.x_pos + CELL_SIZE
                # new_pos_y = self.y_pos
            elif event.key == pygame.K_UP:
                self.direction = "Up"
                # new_pos_y = self.y_pos - CELL_SIZE
                # new_pos_x = self.x_pos
            elif event.key == pygame.K_DOWN:
                self.direction = "Down"
                # new_pos_y = self.y_pos + CELL_SIZE
                # new_pos_x = self.x_pos

        #     if self.check_collision(new_pos_x, new_pos_y) == 1:
        #         return new_pos_x, new_pos_y
            
        # return self.x_pos, self.y_pos
            #self.draw()
          
    def move(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_move_time < 100:  # Giữ nguyên vị trí trong 100ms
            return
        
        self.last_move_time = current_time
    
        target_x = self.x_pos
        target_y = self.y_pos

        if self.direction == "Left":
            target_x -= CELL_SIZE
        elif self.direction == "Right":
            target_x += CELL_SIZE
        elif self.direction == "Up":
            target_y -= CELL_SIZE
        elif self.direction == "Down":
            target_y += CELL_SIZE

        if self.check_collision(target_x, target_y) == 1:
           
            while (self.x_pos, self.y_pos) != (target_x, target_y):
                rect = self.game.screen.blit(BG_IMG, (self.x_pos, self.y_pos))

                if self.x_pos < target_x:
                    self.x_pos += 1
                elif self.x_pos > target_x:
                    self.x_pos -= 1
                if self.y_pos < target_y:
                    self.y_pos += 1
                elif self.y_pos > target_y:
                    self.y_pos -= 1

                self.draw()
                pygame.display.update(rect)
                pygame.time.delay(5)
        else:
            self.draw()

    def update_board_pos(self):
        self.x_board_pos = (self.y_pos - self.offset) // CELL_SIZE
        self.y_board_pos = (self.x_pos - self.offset) // CELL_SIZE
    
    def update_position(self, x, y):
        self.x_pos = x
        self.y_pos = y
    
    def eat_food(self):
        x_board_pos = (self.y_pos - self.offset) // CELL_SIZE
        y_board_pos = (self.x_pos - self.offset) // CELL_SIZE
        if(self.map[x_board_pos][y_board_pos] == 2):
            self.score += self.offset
            self.map[x_board_pos][y_board_pos] = 5
        if(self.map[x_board_pos][y_board_pos] == 3):
            self.score += 30
            self.powerup = True
            # self.powerup_timer = pygame.time.get_ticks() + 7000  # Power-up tồn tại trong 7 giây
            self.powerup_time = time.time()
            self.map[x_board_pos][y_board_pos] = 5 # No food on path
        
    
    def get_score(self):
        return self.score

    def get_lives(self):
        return self.lives

    def check_win_condition(map):
        for row in map:
            if 2 in row or 3 in row:  # Nếu vẫn còn thức ăn (2) hoặc viên năng lượng (3)
                return False
        return True

    # Power up: chỉnh trạng thái dead của ma

    