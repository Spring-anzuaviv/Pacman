from specification import *
import copy
from BoardGame import screen

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
        self.turns = self.check_collisions()  # Kiểm tra hướng đi hợp lệ

    def draw(self):
        if self.direction == "right":  # Đi sang phải
            screen.blit(self.img, (self.x_pos, self.y_pos))
        elif self.direction == "left":
            flipped_image = pygame.transform.flip(self.img, True, False)
            screen.blit(flipped_image, (self.x_pos, self.y_pos))
        elif self.direction == "up":
            rotated_image = pygame.transform.rotate(self.img, 90)
            screen.blit(rotated_image, (self.x_pos, self.y_pos))
        elif self.direction == "down":
            rotated_image = pygame.transform.rotate(self.img, 270)
            screen.blit(rotated_image, (self.x_pos, self.y_pos))
        
        pacman_rect = pygame.Rect((self.center_x - 18, self.center_y - 18), (36, 36))
        return pacman_rect  # Trả về vùng va chạm của Pac-Man