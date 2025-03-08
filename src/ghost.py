from specification import *
class Ghost:
    def __init__(self, game, x_coord, y_coord, target, speed, img, direct, dead, powerup, board, board_offset):
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
        self.offset = board_offset
        self.game = game

    def draw(self):
        #Normal state
        if (not self.powerup and not self.dead):
            self.game.screen.blit(self.img, (self.x_pos, self.y_pos))
        #Power up
        elif(self.powerup and not self.dead):
            self.game.screen.blit(GHOST_POWERUP, (self.x_pos, self.y_pos))
        #Dead
        else:
           self.game.screen.blit(GHOST_DEAD, (self.x_pos, self.y_pos))
        pygame.display.update()
        time.sleep(0.1)  


    def draw_path(self):
        # Pacman's position changes
        print(self.path)
        end = self.target
        for x, y in self.path:
            self.x_pos = y * CELL_SIZE + self.offset
            self.y_pos = x * CELL_SIZE + self.offset
            self.game.screen.fill((0, 0, 0))  
            self.game.draw_board1() # Màn hình cũ
            self.game.screen.blit(PACMAN_LEFT_1, (self.target[0], self.target[1])) 
            self.game.screen.blit(self.img, (self.x_pos , self.y_pos )) 
            # print((self.target[1], self.target[0]))
            pygame.display.update()
            time.sleep(0.5)  

    def draw_ghost(self, x, y):
        self.game.screen.blit(self.img, (y * CELL_SIZE + self.offset, x * CELL_SIZE + self.offset))
        pygame.display.update()

    def draw_multipaths(self, paths): ...
        
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

    def move_bfs(self):
        print("BFS")
        start_time = time.time()
        path = []
        start = ((self.y_pos - self.offset) // GRID_SIZE, (self.x_pos - self.offset) // GRID_SIZE)
        print("Start node:", start)
        end = ((self.target[1] - self.offset) // GRID_SIZE, (self.target[0] - self.offset) // GRID_SIZE)  # Pac-Man
        print("Goal node: ", end)
        if self.path and (self.path[-1] == [self.target[0], self.target[1]]):
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
            #print(f"Expanding: {x}, {y}")

            if (x, y) == end:
                self.path = path 
                elapsed_time = time.time() - start_time
                memory_used = sys.getsizeof(visited) + max_queue_size 
                print(f"Path found! Time: {elapsed_time:.6f}s, Memory: {memory_used} bytes")

                return path  
            for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:  # Các hướng di chuyển
                next_x, next_y = x + dx, y + dy
                #Generate node
                if 0 <= next_x < len(self.map) and 0 <= next_y < len(self.map[0]) and self.map[next_x][next_y] != 1 and self.map[next_x][next_y] != 4  and (next_x, next_y) not in visited:
                    new_path = path + [(next_x, next_y)]  
                    #print((next_x, next_y))
                    #print("Value: ", self.map[next_x][next_y])

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
        return []  

    def move_dfs(self):
        print("DFS")
        start_time = time.time()  
        path = []
        start = ((self.y_pos - self.offset) // GRID_SIZE, (self.x_pos - self.offset) // GRID_SIZE)
        end = ((self.target[1] - self.offset) // GRID_SIZE, (self.target[0] - self.offset) // GRID_SIZE)

        stack = [(start, [start])]
        visited = set()
        expanded = []  
        max_stack_size = 0  

        while stack:
            max_stack_size = max(max_stack_size, sys.getsizeof(stack)) 
            (x, y), path = stack.pop()
            
            expanded.append((x, y))  
            #print(f"Expanding: {x}, {y}")

            if (x, y) == end:
                elapsed_time = time.time() - start_time  
                memory_used = sys.getsizeof(visited) + max_stack_size  
                print(f"Path found! Time: {elapsed_time:.6f}s, Memory: {memory_used} bytes, Nodes expanded: {len(expanded)}")
                self.path = path
                return path

            visited.add((x, y))

            for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                next_x, next_y = x + dx, y + dy
                if 0 <= next_x < len(self.map) and 0 <= next_y < len(self.map[0]) and self.map[next_x][next_y] != 1 and self.map[next_x][next_y] != 4 and (next_x, next_y) not in visited:
                    new_path = path + [(next_x, next_y)]
                   # print(f"Checking node: ({next_x}, {next_y}), Value: {self.map[next_x][next_y]}")

                    if (next_x, next_y) == end:
                        elapsed_time = time.time() - start_time
                        memory_used = sys.getsizeof(visited) + max_stack_size
                        print(f"Goal generated! Early stopping. Time: {elapsed_time:.6f}s, Memory: {memory_used} bytes, Nodes expanded: {len(expanded)}")
                        self.path = path
                        return new_path

                    stack.append(((next_x, next_y), new_path))

        elapsed_time = time.time() - start_time
        memory_used = sys.getsizeof(visited) + max_stack_size
        print(f"No path found. Time: {elapsed_time:.6f}s, Memory: {memory_used} bytes, Nodes expanded: {len(expanded)}")
        return []
    

    def move_ucs(self):
        print("UCS")

        start_time = time.time()

        start = ((self.y_pos - self.offset) // GRID_SIZE, (self.x_pos - self.offset) // GRID_SIZE)
        end = ((self.target[1] - self.offset) // GRID_SIZE, (self.target[0] - self.offset) // GRID_SIZE)

        pq = [(0, start, [start])]  # (cost, position, path)
        visited = set()
        expanded = []
        max_pq_size = 0

        while pq:
            max_pq_size = max(max_pq_size, sys.getsizeof(pq))  
            cost, (x, y), path = heapq.heappop(pq)

            if (x, y) in visited:  # Nếu nút đã từng mở rộng thì bỏ qua
                continue  

            visited.add((x, y))  # Đánh dấu đã thăm khi lấy ra khỏi hàng đợi

            expanded.append((x, y))  
            #print(f"Expanding: {x}, {y}, Cost: {cost}")

            if (x, y) == end:
                elapsed_time = time.time() - start_time
                memory_used = sys.getsizeof(visited) + max_pq_size
                print(f"Path found! Time: {elapsed_time:.6f}s, Memory: {memory_used} bytes, Nodes expanded: {len(expanded)}")
                self.path = path
                return path

            for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                next_x, next_y = x + dx, y + dy
                if 0 <= next_x < len(self.map) and 0 <= next_y < len(self.map[0]) and self.map[next_x][next_y] != 1 and self.map[next_x][next_y] != 4:
                    new_cost = cost + 1  # Mỗi bước đi có chi phí cố định là 1
                    new_path = path + [(next_x, next_y)]
                    heapq.heappush(pq, (new_cost, (next_x, next_y), new_path))
        elapsed_time = time.time() - start_time
        memory_used = sys.getsizeof(visited) + max_pq_size
        print(f"No path found. Time: {elapsed_time:.6f}s, Memory: {memory_used} bytes, Nodes expanded: {len(expanded)}")
        return []

    def move_astar(self):
        print("A*")

        def heuristic(x, y):
            manhatta = (abs(x - self.target[0] // GRID_SIZE) + abs(y - self.target[1]//GRID_SIZE))
            return manhatta

        start_time = time.time()
        start = ((self.y_pos - self.offset) // GRID_SIZE, (self.x_pos - self.offset) // GRID_SIZE)
        end = ((self.target[1] - self.offset) // GRID_SIZE, (self.target[0] - self.offset) // GRID_SIZE)

        g_n = {start: 0}
        f_n = {start: heuristic(*start)}

        pq = [(heuristic(*start), start, [start])]
        visited = set()
        expanded = []
        max_pq_size = 0

       

        while pq:
            max_pq_size = max(max_pq_size, len(pq))
            cost, (x, y), path = heapq.heappop(pq) 

            if (x, y) in visited:  # Bỏ qua nếu đã thăm
                continue
            
            visited.add((x, y))
            expanded.append((x, y))
            #print(f"Expanding: {x}, {y}, cost: {cost}, h_n: {heuristic(x,y)}, g_n: {g_n[(x, y)]}")

            if (x, y) == end:
                elapsed_time = time.time() - start_time
                print(f"Path found! Time: {elapsed_time:.6f}s, Memory: {sys.getsizeof(visited)} bytes")
                self.path = path
                return path  

            for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                next_x, next_y = x + dx, y + dy
                if 0 <= next_x < len(self.map) and 0 <= next_y < len(self.map[0]) and self.map[next_x][next_y] != 1 and self.map[next_x][next_y] != 4 and (next_x, next_y) not in visited:
                    new_g = g_n[(x, y)] + 1
                    new_f = new_g + heuristic(next_x, next_y)

                    if (next_x, next_y) not in g_n or new_g < g_n[(next_x, next_y)]:
                        g_n[(next_x, next_y)] = new_g
                        f_n[(next_x, next_y)] = new_f
                        new_path = path + [(next_x, next_y)]
                        heapq.heappush(pq, (new_f, (next_x, next_y), new_path))

        elapsed_time = time.time() - start_time
        memory_used = sys.getsizeof(visited) + max_pq_size
        print(f"No path found. Time: {elapsed_time:.6f}s, Memory: {memory_used} bytes, Nodes expanded: {len(expanded)}")
        return []
    
    def update_position(self, x, y):
        self.x_pos = x
        self.y_pos = y


class AStarSolver:
    def __init__(self, x_pos, y_pos, target, map_data):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.target = target
        self.map = map_data

    # Power up: đổi ảnh, nếu bị ăn thì dead, trở về vị trí bắt dâu
 