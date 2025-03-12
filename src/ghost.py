
from specification import *
class Ghost:
    def __init__(self, game, x_coord, y_coord, next_x, next_y, target, speed, img, direct, dead, powerup, board, board_offset):
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
        self.next_x_pos = next_x
        self.next_y_pos = next_y
        self.time = 0
        self.expanded = 0
        self.mem = 0
        

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
            self.time, self.expanded, self.mem = elapsed_time, expanded_nodes,  memory_used
            return self.path
        
        queue = deque([[start]])  
        visited = set([start])
        visited.clear()  
        expanded = []
        expanded.clear()

        expanded_nodes = 0
        max_queue_size = 0

        while queue:
            max_queue_size = max(max_queue_size, sys.getsizeof(queue))
            path = queue.popleft()  # Lấy đường đi hiện tại từ hàng đợi
            x, y = path[-1]  # Lấy vị trí cuối cùng trong đường đi
            expanded.append((x, y))  
            expanded_nodes += 1
            #print(f"Expanding: {x}, {y}")

            if (x, y) == end:
                self.path = path 
                elapsed_time = time.time() - start_time
                memory_used = sys.getsizeof(visited) + max_queue_size 
                print(f"Path found! Time: {elapsed_time:.6f}s, Memory: {memory_used} bytes, Nodes: {expanded_nodes}")
                self.time, self.expanded, self.mem = elapsed_time, expanded_nodes,  memory_used
                return path
            
            for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:  # Các hướng di chuyển
                next_x, next_y = x + dx, y + dy
                #Generate node
                if 0 <= next_x < len(self.map) and 0 <= next_y < len(self.map[0]) and self.map[next_x][next_y] != 1 and self.map[next_x][next_y] != 4  and (next_x, next_y) not in visited:
                    new_path = path + [(next_x, next_y)]  

                    #Early stopping 
                    if (next_x, next_y) == end:
                        self.path = new_path  
                        elapsed_time = time.time() - start_time
                        memory_used = sys.getsizeof(visited) + max_queue_size
                        print(f"Goal generated! Stopping early. Time: {elapsed_time:.6f}s, Memory: {memory_used} bytes")
                        self.time, self.expanded, self.mem = elapsed_time, expanded_nodes,  memory_used

                        return new_path
                    
                    queue.append(new_path) 
                    visited.add((next_x, next_y))  
        self.path = []  
        self.time, self.expanded, self.mem = elapsed_time, expanded_nodes,  memory_used
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
        expanded_nodes = 0

        while stack:
            max_stack_size = max(max_stack_size, sys.getsizeof(stack)) 
            (x, y), path = stack.pop()
            
            expanded.append((x, y))  
            expanded_nodes += 1
            #print(f"Expanding: {x}, {y}")

            if (x, y) == end:
                elapsed_time = time.time() - start_time  
                memory_used = sys.getsizeof(visited) + max_stack_size  
                print(f"Path found! Time: {elapsed_time:.6f}s, Memory: {memory_used} bytes, Nodes expanded: {len(expanded)}")
                self.path = path
                self.time, self.expanded, self.mem = elapsed_time, expanded_nodes,  memory_used
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
                        self.time, self.expanded, self.mem = elapsed_time, expanded_nodes,  memory_used
                        return new_path

                    stack.append(((next_x, next_y), new_path))

        elapsed_time = time.time() - start_time
        memory_used = sys.getsizeof(visited) + max_stack_size
        print(f"No path found. Time: {elapsed_time:.6f}s, Memory: {memory_used} bytes, Nodes expanded: {len(expanded)}")
        self.time, self.expanded, self.mem = elapsed_time, expanded_nodes, memory_used
        return []
    

    def move_ucs(self):
      
        start_time = time.time()

        start = ((self.y_pos - self.offset) // GRID_SIZE, (self.x_pos - self.offset) // GRID_SIZE)
        end = ((self.target[1] - self.offset) // GRID_SIZE, (self.target[0] - self.offset) // GRID_SIZE)

        def g_cost (x,y):  # chi phí cho mỗi bước đi
            unit = WIDTH // GRID_SIZE + HEIGHT // GRID_SIZE - 2 # khoảng cách lớn nhất giữa 2 điểm làm đơn vị, để khi lấy distance_to_pacman/unit <= 1
            base_cost = 1
            distance_to_pacman = (abs(x - end[0]) + abs(y - end[1])) 
            if(distance_to_pacman != 1): # nếu không phải là điểm kế cận thì kiểm tra xem có gần tường không
                if(x - 1 < 0 or x + 1 >= WIDTH // GRID_SIZE or y - 1 < 0 or y + 1 >= HEIGHT // GRID_SIZE):
                    return 2 #nếu gần đến tường thì chi phí sẽ cao hơn 
            if(self.powerup == True):
                avoid_pacman = ( 1 - distance_to_pacman/unit) # nếu pacman đang có powerup thì ma có nguy cơ bị ăn nên cần tránh xa pacman ; cách càng xa chi phí avoid càng th
                return base_cost + avoid_pacman
            else:
                return  base_cost + distance_to_pacman/unit # nếu pacman không có powerup thì ma sẽ cố gắng tiếp cận

        pq = [(0, start, [start])]  # (cost, position, path)
        visited = set()
        expanded = []
        max_pq_size = 0
        expanded_nodes = 0

        while pq:
            max_pq_size = max(max_pq_size, sys.getsizeof(pq))  
            cost, (x, y), path = heapq.heappop(pq)

            if (x, y) in visited:  # Nếu nút đã từng mở rộng thì bỏ qua
                continue  
            else:
                visited.add((x, y))  # Đánh dấu đã thăm khi lấy ra khỏi hàng đợi
                expanded.append((x, y))  
                expanded_nodes += 1

            if (x, y) == end:
                elapsed_time = time.time() - start_time
                memory_used = sys.getsizeof(visited) + max_pq_size
                print(f"Path found! Time: {elapsed_time:.6f}s, Memory: {memory_used} bytes, Nodes expanded: {len(expanded)}")
                self.path = path
                self.time, self.expanded, self.mem = elapsed_time, expanded_nodes,  memory_used
                return path

            for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                next_x, next_y = x + dx, y + dy
                if (0 <= next_x < len(self.map) and 0 <= next_y < len(self.map[0]) and self.map[next_x][next_y] != 1 and self.map[next_x][next_y] != 4 and (next_x, next_y) not in visited):
                    new_cost = cost + g_cost(next_x, next_y)  # Mỗi bước đi có chi phí tuân theo hàm g_cost
                    new_path = path + [(next_x, next_y)]
                    heapq.heappush(pq, (new_cost, (next_x, next_y), new_path))

        elapsed_time = time.time() - start_time
        memory_used = sys.getsizeof(visited) + max_pq_size
        self.time, self.expanded, self.mem = elapsed_time, expanded_nodes,  memory_used

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
        
        def g_cost (x,y):  # chi phí cho mỗi bước đi
            unit = WIDTH // GRID_SIZE + HEIGHT // GRID_SIZE - 2 # khoảng cách lớn nhất giữa 2 điểm làm đơn vị, để khi lấy distance_to_pacman/unit <= 1
            base_cost = 1
            distance_to_pacman = (abs(x - end[0]) + abs(y - end[1])) 
            if(distance_to_pacman != 1): # nếu không phải là điểm kế cận thì kiểm tra xem có gần tường không
              if(x - 1 < 0 or x + 1 >= WIDTH // GRID_SIZE or y - 1 < 0 or y + 1 >= HEIGHT // GRID_SIZE):
                    return 2 #nếu gần đến tường thì chi phí sẽ cao hơn 
            if(self.powerup == True):
                avoid_pacman = ( 1 - distance_to_pacman/unit) # nếu pacman đang có powerup thì ma có nguy cơ bị ăn nên cần tránh xa pacman ; cách càng xa chi phí avoid càng th
                return base_cost + avoid_pacman
            else:
                return  1 + distance_to_pacman/unit # nếu pacman không có powerup thì ma sẽ cố gắng tiếp cận
            return base_cost
            
        g_n = {start: 0}
        f_n = {start: heuristic(*start)}

        pq = [(heuristic(*start), start, [start])]
        visited = set()
        expanded = []
        max_pq_size = 0
        expanded_nodes = 0      

        while pq:
            max_pq_size = max(max_pq_size, len(pq))
            cost, (x, y), path = heapq.heappop(pq) 

            if (x, y) in visited:  # Bỏ qua nếu đã thăm
                continue
            else:
                visited.add((x, y))
                expanded.append((x, y))
                expanded_nodes += 1
           

            if (x, y) == end:
                elapsed_time = time.time() - start_time
                memory_used = sys.getsizeof(visited)
                print(f"Path found! Time: {elapsed_time:.6f}s, Memory: {memory_used} bytes")
                self.path = path
                self.time, self.expanded, self.mem = elapsed_time, expanded_nodes,  memory_used
                return path

            for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                next_x, next_y = x + dx, y + dy
                if (0 <= next_x < len(self.map) and 0 <= next_y < len(self.map[0]) and self.map[next_x][next_y] != 1 and self.map[next_x][next_y] != 4 and (next_x, next_y) not in visited):
                    new_g = g_n[(x, y)] + g_cost(next_x, next_y) 
                    new_f = new_g + heuristic(next_x, next_y)

                    if (next_x, next_y) not in g_n or new_g < g_n[(next_x, next_y)]:
                        g_n[(next_x, next_y)] = new_g
                        f_n[(next_x, next_y)] = new_f
                        new_path = path + [(next_x, next_y)]
                        heapq.heappush(pq, (new_f, (next_x, next_y), new_path))

        elapsed_time = time.time() - start_time
        memory_used = sys.getsizeof(visited) + max_pq_size
        print(f"No path found. Time: {elapsed_time:.6f}s, Memory: {memory_used} bytes, Nodes expanded: {len(expanded)}")
        self.time, self.expanded, self.mem = elapsed_time, expanded_nodes,  memory_used
        return []
    
    def update_next(self, x, y):
        self.next_x_pos = x
        self.next_y_pos = y
       
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
 
