from src.specification import *
import copy

class Player:
    def __init__(self, screen, x_coord, y_coord, speed, direct, dead, powerup, board, board_offset):
        self.x_pos = x_coord
        self.y_pos = y_coord
        self.gamescreen = screen
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
        self.offset = board_offset
        self.x_board_pos = (self.x_pos - self.offset) // CELL_SIZE ######################### Sửa lại offset
        self.y_board_pos = (self.y_pos - self.offset) // CELL_SIZE
        self.open_mouth = False

    def appear(self):
        self.direction = "Left"
        self.draw()

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
        if((0 <= (x - self.offset) // CELL_SIZE < len(self.map[0]) and 0 <= (y - self.offset) // CELL_SIZE < len(self.map) and self.map[(y - self.offset) // CELL_SIZE ][(x - self.offset) // CELL_SIZE ] == 1) 
           or (0 <= (x - self.offset) // CELL_SIZE < len(self.map[0]) and 0 <= (y - self.offset) // CELL_SIZE < len(self.map) and self.map[(y - self.offset) // CELL_SIZE ][(x - self.offset) // CELL_SIZE ] == 4)):
            return 0
        elif ((0 <= (x - self.offset) // CELL_SIZE < len(self.map[0]) and 0 <= (y - self.offset) // CELL_SIZE < len(self.map)) 
           or (0 <= (x - self.offset) // CELL_SIZE < len(self.map[0]) and 0 <= (y - self.offset) // CELL_SIZE < len(self.map))):
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
        self.x_board_pos = (self.y_pos - self.offset) // CELL_SIZE
        self.y_board_pos = (self.x_pos - self.offset) // CELL_SIZE
    
    def update_position(self, x, y):
        self.x_pos = x
        self.y_pos = y
    
    def eat_food(self):
        if(self.map[self.x_board_pos][self.y_board_pos] == 2):
            self.score += self.offset
            self.map[self.x_board_pos][self.y_board_pos] = 5
        if(self.map[self.x_board_pos][self.y_board_pos] == 3):
            self.score += 30
            self.powerup = True
            self.map[self.x_board_pos][self.y_board_pos] = 5 # No food on path

    # Power up: chỉnh trạng thái dead của ma

    # Thắng: num đếm thức ăn, = 0 hiện mhinh thắng
    
    # Thua: chạm ma, dead = True, nếu còn mạng, vẽ lại vị trí bắt đầu
    # ko còn mạng thì hiển thị màn hình thua