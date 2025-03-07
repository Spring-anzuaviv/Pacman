from src.specification import *
import copy

class Player:
    def __init__(self, screen, x_coord, y_coord, target, speed, direct, dead, powerup, board):
        self.x_pos = x_coord
        self.y_pos = y_coord
        self.gamescreen = screen
        self.target = target #position [x, y]
        self.speed = speed  
        # self.img = img 
        self.direction = direct  #"left", "right", "up", "down"
        self.dead = dead
        self.map = board  
        self.powerup = powerup  # Nếu True, Pac-Man có thể ăn ma
        self.lives = 3  # Số mạng của Pac-Man
        self.score = 0  # Điểm số
        self.frame_count = 0 #thay đổi hình
        self.turns = [False, False, False, False] #R, L, U, D
        self.x_board_pos = (self.x_pos - 10) // CELL_SIZE ######################### Sửa lại offset
        self.y_board_pos = (self.y_pos - 10) // CELL_SIZE
        self.open_mouth = False
 
    def draw(self):
        if self.open_mouth:
            self.open_mouth = False
            if self.direction == "Left":
                rect = self.gamescreen.blit(PACMAN_LEFT_1, (self.x_pos, self.y_pos))
                pygame.display.update(rect)
            if self.direction == "Right":
                rect = self.gamescreen.blit(PACMAN_RIGHT_1, (self.x_pos, self.y_pos))
                pygame.display.update(rect)
            if self.direction == "Up":
                rect = self.gamescreen.blit(PACMAN_UP_1, (self.x_pos, self.y_pos))
                pygame.display.update(rect)
            if self.direction == "Down":
                rect = self.gamescreen.blit(PACMAN_DOWN_1, (self.x_pos, self.y_pos))
                pygame.display.update(rect) 
        else:
            self.open_mouth = True
            if self.direction == "Left":
                rect = self.gamescreen.blit(PACMAN_LEFT_2, (self.x_pos, self.y_pos))
                pygame.display.update(rect)
            if self.direction == "Right":
                rect = self.gamescreen.blit(PACMAN_RIGHT_2, (self.x_pos, self.y_pos))
                pygame.display.update(rect)
            if self.direction == "Up":
                rect = self.gamescreen.blit(PACMAN_UP_2, (self.x_pos, self.y_pos))
                pygame.display.update(rect)
            if self.direction == "Down":
                rect = self.gamescreen.blit(PACMAN_DOWN_2, (self.x_pos, self.y_pos))
                pygame.display.update(rect)
    
    def check_collision(self, x, y):
        if((0 <= (x - 10) // 26 < len(self.map) and 0 <= (y - 10) // 26 < len(self.map) and self.map[(y - 10) // 26 ][(x - 10) // 26 ] == 1) 
           or self.map[(y - 10) // 26 ][(x - 10) // 26 ] == 4):
            return 0
        return 1
    
    def move(self, event):
        """Chỉ di chuyển Pac-Man khi có sự kiện nhấn phím"""
        
        if event.type == pygame.KEYDOWN:  
            if event.key == pygame.K_LEFT:
                self.direction = "Left"
                new_pos_x = self.x_pos - CELL_SIZE
                new_pos_y = self.y_pos
            elif event.key == pygame.K_RIGHT:
                self.direction = "Right"
                new_pos_x = self.x_pos + CELL_SIZE
                new_pos_y = self.y_pos
            elif event.key == pygame.K_UP:
                self.direction = "Up"
                new_pos_y = self.y_pos - CELL_SIZE
                new_pos_x = self.x_pos
            elif event.key == pygame.K_DOWN:
                self.direction = "Down"
                new_pos_y = self.y_pos + CELL_SIZE
                new_pos_x = self.x_pos

            if self.check_collision(new_pos_x, new_pos_y) == 1:
                self.x_pos = new_pos_x
                self.y_pos = new_pos_y
                self.update_board_pos()
            self.eat_food()
            #self.draw()

    def update_board_pos(self):
        self.x_board_pos = (self.y_pos - 10) // 26
        self.y_board_pos = (self.x_pos - 10) // 26
    
    def eat_food(self):
        if(self.map[self.x_board_pos][self.y_board_pos] == 2):
            self.score += 10
            self.map[self.x_board_pos][self.y_board_pos] = 5
        if(self.map[self.x_board_pos][self.y_board_pos] == 3):
            self.score += 30
            self.powerup = True
            self.map[self.x_board_pos][self.y_board_pos] = 5 # No food on path

    