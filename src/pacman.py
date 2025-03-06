from src.specification import *
import copy


class Player:
    def __init__(self, x_coord, y_coord, target, speed, img, direct, dead, powerup, board):
        self.x_pos = x_coord
        self.y_pos = y_coord
        self.center_x = self.x_pos + 13
        self.center_y = self.y_pos + 13
        self.target = target #position [x, y]
        self.speed = speed  
        self.img = img 
        self.direction = direct  #"left", "right", "up", "down"
        self.dead = dead
        self.map = board  
        self.powerup = powerup  # Nếu True, Pac-Man có thể ăn ma
        self.lives = 3  # Số mạng của Pac-Man
        self.score = 0  # Điểm số
        self.frame_count = 0 #thay đổi hình
        self.turns = [False, False, False, False] #R, L, U, D

    def draw(self):
        from src.BoardGame import screen
        current_image = self.img[(self.frame_count // 20) % len(self.img)]

        if self.direction == "right":  # Đi sang phải
            screen.blit(current_image, (self.x_pos, self.y_pos))
        elif self.direction == "left":
            flipped_image = pygame.transform.flip(current_image, True, False)
            screen.blit(flipped_image, (self.x_pos, self.y_pos))
        elif self.direction == "up":
            rotated_image = pygame.transform.rotate(current_image, 90)
            screen.blit(rotated_image, (self.x_pos, self.y_pos))
        elif self.direction == "down":
            rotated_image = pygame.transform.rotate(current_image, 270)
            screen.blit(rotated_image, (self.x_pos, self.y_pos))
        
        self.frame_count += 1  # Tăng frame để chuyển đổi hình ảnh
        if self.frame_count >= 100:  # Reset lại sau mỗi 30 frame (để lặp lại hiệu ứng)
            self.frame_count = 0

    '''def reset_position(self, x_start, y_start):
        self.x_pos = x_start
        self.y_pos = y_start
        self.center_x = self.x_pos + 13  # Cập nhật lại vị trí trung tâm
        self.center_y = self.y_pos + 13'''

    def move(self, direction):
        #update sau khi dùng phím
        new_x, new_y = self.x_pos, self.y_pos
        if direction == "right":
            new_x = self.x_pos + self.speed
            new_y = self.y_pos
        elif direction == "left":
            new_x = self.x_pos - self.speed
            new_y = self.y_pos
        elif direction == "up":
            new_x = self.x_pos
            new_y = self.y_pos - self.speed
        elif direction == "down":
            new_x = self.x_pos
            new_y = self.y_pos + self.speed
        else:
            return

        # Kiểm tra va chạm với biên giới màn hình
        if new_x < 0 or new_x >= WIDTH - 26: 
            return 
        if new_y < 0 or new_y >= HEIGHT - 26:  
            return
                
        #check collision, đúng r
        if(self.check_collision(new_x, new_y)):
            self.x_pos = new_x
            self.y_pos = new_y
            self.center_x = self.x_pos + GRID_SIZE // 2
            self.center_y = self.y_pos + GRID_SIZE // 2

            self.direction = direction

    def check_collision(self, x, y):
        #check xem vị trí (x, y) có phải là wall k0, chỗ này đúng r
        grid_x = (x + GRID_SIZE // 2) // GRID_SIZE
        grid_y = (y + GRID_SIZE // 2) // GRID_SIZE
        if self.map[grid_y][grid_x] in [1,4,0]:
            return False
        return True
    