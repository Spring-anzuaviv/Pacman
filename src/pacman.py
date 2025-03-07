import pygame
from src.specification import *
from src.BoardGame import *

class Player:
    def __init__(self, x_coord, y_coord, target, speed, images, direct, dead, powerup, board):
        self.x_pos = x_coord
        self.y_pos = y_coord
        self.center_x = self.x_pos + 13
        self.center_y = self.y_pos + 13
        self.target = target
        self.speed = speed  
        self.img = images
        self.img_powerup = [POWERUP]  # Hình Powerup
        self.img_dead = DEAD  # Hình Dead
        self.direction = direct
        self.dead = dead
        self.map = board  
        self.powerup = powerup  
        self.lives = 3  
        self.score = 0  
        self.frame_count = 0  
        self.turns = [False, False, False, False]  

    def draw(self):
        # Chế độ Dead
        if self.dead:
            screen.blit(self.img_dead, (self.x_pos, self.y_pos))

        # Chế độ Powerup
        elif self.powerup:
            current_image = self.img_powerup[0]
            screen.blit(current_image, (self.x_pos, self.y_pos))

        # Bình thường
        else:
            current_image = self.img[(self.frame_count // 10) % len(self.img)]
            if self.direction == "right":
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

            self.frame_count += 1
            if self.frame_count >= 100:
                self.frame_count = 0