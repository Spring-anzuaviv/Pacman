import pygame
from BoardGame import screen, HEIGHT, WIDTH, boards1, GRID_SIZE
class Ghost:
    def __init__(self, x_coord, y_coord, target, speed, img, direct, dead, powerup):
        self.x_pos = x_coord
        self.y_pos = y_coord
        self.center_x = self.x_pos + 22
        self.center_y = self.y_pos + 22
        self.target = target
        self.speed = speed
        self.img = img
        self.direction = direct 
        self.dead = dead
        self.turns = self.check_collisions()
        self.powerup = powerup #player can eat ghost

    def draw(self):
        #Normal state
        if (not self.powerup and not self.dead):
            screen.blit(self.img, (self.x_pos, self.y_pos))
        #Power up
        #Dead
        #else:
           # screen.blit(dead_img, (self.x_pos, self.y_pos))
        ghost_rect = pygame.rect.Rect((self.center_x - 18, self.center_y - 18), (36, 36))
        return ghost_rect
    
    def check_collisions(self):
        cell_h = GRID_SIZE
        cell_w = GRID_SIZE
        space = 15 
        self.turns = [False, False, False, False]

        #Check go up
        

    #def move_bfs(self):
        
    #def move_dfs(self):

    #def move_ucs(self):

    #def move_astar(self):
