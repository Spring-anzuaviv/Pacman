from src.specification import *
import copy


class Player:
    def __init__(self, x_coord, y_coord, target, speed, img, direct, dead, powerup, board):
        self.x_pos = x_coord  # Vị trí X của Pac-Man
        self.y_pos = y_coord  # Vị trí Y của Pac-Man
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
        #self.turns = self.check_collisions()  # Kiểm tra hướng đi hợp lệ

    def draw(self):
        from src.BoardGame import screen
        current_image = self.img[(self.frame_count // 10) % len(self.img)]

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
        if self.frame_count >= 30:  # Reset lại sau mỗi 30 frame (để lặp lại hiệu ứng)
            self.frame_count = 0