from specification import *
import copy
from BoardGame import screen
class Ghost:
    def __init__(self, x_coord, y_coord, target, speed, img, direct, dead, powerup, board):
        self.x_pos = x_coord
        self.y_pos = y_coord
        self.center_x = self.x_pos + 13
        self.center_y = self.y_pos + 13
        self.target = target #position [x, y]
        self.speed = speed
        self.img = img
        self.direction = direct # 0: right, 1: left, 2: up, 3: down
        self.dead = dead
        self.turns = self.check_collisions()
        self.powerup = powerup #player can eat ghost
        self.map = board

    def draw(self):
        #Normal state
        if (not self.powerup and not self.dead):
            screen.blit(self.img, (self.x_pos, self.y_pos))
        #Power up
        elif(self.powerup and not self.dead):
            screen.blit(GHOST_POWERUP, (self.x_pos, self.y_pos))
        #Dead
        else:
           screen.blit(GHOST_DEAD, (self.x_pos, self.y_pos))
        ghost_rect = pygame.rect.Rect((self.center_x - 18, self.center_y - 18), (36, 36))
        return ghost_rect
    
    def check_collisions(self):
        cell_h = GRID_SIZE
        cell_w = GRID_SIZE
        space = 15 
        self.turns = [False, False, False, False] # up, down, left, right
        
        x, y = self.x_pos // cell_h, self.y_pos // cell_w  
        
        # Go up
        if y > 0 and self.map[y - 1][x] == 0:
            self.turns[0] = True 
        
        #Go down
        if y < len(self.map) - 1 and self.map[y + 1][x] == 0:
            self.turns[1] = True  
        
        # Go left
        if x > 0 and self.map[y][x - 1] == 0:
            self.turns[2] = True  
        
        # Go right
        if x < len(self.map[0]) - 1 and self.map[y][x + 1] == 0:
            self.turns[3] = True  
        
        return self.turns

    def move_bfs(self):...
        
    def move_dfs(self):...

    def move_ucs(self):...

    def move_astar(self):...
