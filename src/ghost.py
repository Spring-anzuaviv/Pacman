from specification import *
import copy
import time
from collections import deque
from BoardGame import screen
class Ghost:
    def __init__(self, x_coord, y_coord, target, speed, img, direct, dead, powerup, board):
        self.x_pos = x_coord
        self.y_pos = y_coord
        # self.center_x = self.x_pos + 13
        # self.center_y = self.y_pos + 13
        self.target = target #position [x, y] of pacman
        self.speed = speed
        self.img = img
        self.direction = direct # 0: right, 1: left, 2: up, 3: down
        self.dead = dead
#       self.turns = self.check_collisions()
        self.powerup = powerup #player can eat ghost
        self.map = copy.deepcopy(board)
        self.path = [] #Path found by search algorithm

    def draw(self):
        #Normal state
        if (not self.powerup and not self.dead):
            screen.blit(self.img, (self.x_pos + 100, self.y_pos + 100))
        #Power up
        elif(self.powerup and not self.dead):
            screen.blit(GHOST_POWERUP, (self.x_pos + 100, self.y_pos + 100))
        #Dead
        else:
           screen.blit(GHOST_DEAD, (self.x_pos, self.y_pos))
        pygame.display.update()
    
    # Không cần này 
    def check_collisions(self):
        cell_h = GRID_SIZE
        cell_w = GRID_SIZE
        space = 15 
        turns = [False, False, False, False] # up, down, left, right
        
        x, y = self.x_pos // cell_h, self.y_pos // cell_w  
        
        # Go up
        if y > 0 and self.map[y - 1][x] == 0:
            turns[0] = True 
        
        #Go down
        if y < len(self.map) - 1 and self.map[y + 1][x] == 0:
            turns[1] = True  
        
        # Go left
        if x > 0 and self.map[y][x - 1] == 0:
            turns[2] = True  
        
        # Go right
        if x < len(self.map[0]) - 1 and self.map[y][x + 1] == 0:
            turns[3] = True  
        
        return turns

    def move_bfs(self):  # chưa làm target thay đổi khi pacman di chuyển, chưa implement hàm vẽ 
        start_time = time.time()

        start = (self.x_pos // GRID_SIZE, self.y_pos // GRID_SIZE)
        print("Start node:", start)
        end = (self.target[0] // GRID_SIZE, self.target[1] // GRID_SIZE)  # Pac-Man
        print("Goal node: ", end)
        if self.path and (self.path[-1] == [self.target_x, self.target_y]):
            return  
        
        queue = deque([[start]])  
        visited = set([start])
        visited.clear()  
        expanded = []
        expanded.clear()

        max_queue_size = 0

        while queue:
            max_queue_size = max(max_queue_size, sys.getsizeof(queue))
            path = queue.popleft()  # Lấy đường đi hiện tại từ hàng đợi
            x, y = path[-1]  # Lấy vị trí cuối cùng trong đường đi
            
            expanded.append((x, y))  
            print(f"Expanding: {x}, {y}")

            # current_end = (self.target[0] // GRID_SIZE, self.target[1] // GRID_SIZE)
            # if current_end != end:  # Nếu end thay đổi, tính lại BFS
            # print(f"Target changed! Recomputing BFS with new end: {current_end}")
            # return self.move_bfs()

            if (x, y) == end:
                self.path = path 
                elapsed_time = time.time() - start_time
                memory_used = sys.getsizeof(visited) + max_queue_size 
                print(f"Path found! Time: {elapsed_time:.6f}s, Memory: {memory_used} bytes")

                return path  

            for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:  # Các hướng di chuyển
                next_x, next_y = x + dx, y + dy

                #Generate node
                if 0 <= next_x < len(self.map) and 0 <= next_y < len(self.map[0]) and self.map[next_x][next_y] != '1' and (next_x, next_y) not in visited:
                    new_path = path + [(next_x, next_y)]  
                    #Early stopping 
                    if (next_x, next_y) == end:
                        self.path = new_path  
                        elapsed_time = time.time() - start_time
                        memory_used = sys.getsizeof(visited) + max_queue_size
                        print(f"Goal generated! Stopping early. Time: {elapsed_time:.6f}s, Memory: {memory_used} bytes")
                        return new_path 
                    
                    queue.append(new_path) 
                    visited.add((next_x, next_y))  

        self.path = []  
        return None  


    def move_dfs(self):...

    def move_ucs(self):...

    def move_astar(self):...
