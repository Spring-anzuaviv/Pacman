from specification import *
class Ghost:
    def __init__(self, game, x_coord, y_coord, next_x, next_y, target, speed, img, direct, dead, powerup, board, board_offset):
        self.x_pos = x_coord
        self.y_pos = y_coord
        self.target = target 
        self.img = img
        self.direction = direct 
        self.dead = dead
        self.powerup = powerup # Player can eat ghost
        self.map = board
        self.path = [] #Path found by search algorithm
        self.offset = board_offset
        self.game = game
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
        button_rect = pygame.Rect(20, 20, 190, 35)
        for x, y in self.path:
            self.x_pos = y * CELL_SIZE + self.offset[0]
            self.y_pos = x * CELL_SIZE + self.offset[1]
            self.game.screen.fill((0, 0, 0))  
            self.game.draw_board1() 
            self.game.screen.blit(PACMAN_LEFT_1, (self.target[0], self.target[1])) 
            if not self.check_collision():
                self.game.screen.blit(self.img, (self.x_pos , self.y_pos )) 

            pygame.draw.rect(self.game.screen, (200, 0, 0), button_rect) 
            font = pygame.font.Font("PressStart2P.ttf", 15)
            text = font.render("See result", True, (0, 0, 0))  
            self.game.screen.blit(text, (button_rect.x + 20, button_rect.y + 10))

            pygame.display.update()
            time.sleep(0.5)  
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(event.pos): 
                        click_sound = pygame.mixer.Sound(MOUSE_CLICK_SOUND)
                        click_sound.play()
                        return 

    def check_collision(self):
        return [self.x_pos, self.y_pos] == self.target
        
    def move_bfs(self):
        print("BFS")
        start_time = time.time()
        start = ((self.y_pos - self.offset[1]) // GRID_SIZE, (self.x_pos - self.offset[0]) // GRID_SIZE)
        end = ((self.target[1] - self.offset[1]) // GRID_SIZE, (self.target[0] - self.offset[0]) // GRID_SIZE)
        print("Start node:", start)
        print("Goal node:", end)

        if self.path and self.path[-1] == [self.target[0], self.target[1]]:
            elapsed_time = time.time() - start_time
            memory_used = sys.getsizeof(self.path)
            print(f"Path already exists! Time: {elapsed_time:.6f}s, Memory: {memory_used} bytes")
            return self.path

        queue = deque([[start]])
        visited = set()
        visited.add(start)

        expanded_nodes = 0
        max_queue_size = sys.getsizeof(queue)
        
        while queue:
            max_queue_size = max(max_queue_size, sys.getsizeof(queue))
            path = queue.popleft()
            x, y = path[-1]
            expanded_nodes += 1

            if (x, y) == end:
                elapsed_time = time.time() - start_time
                memory_used = sys.getsizeof(queue) + sys.getsizeof(visited)
                print(f"Path found! Time: {elapsed_time:.6f}s, Memory: {memory_used} bytes, Nodes: {expanded_nodes}")
                self.path = path
                self.time, self.expanded, self.mem = elapsed_time, expanded_nodes, memory_used
                return path

            for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                next_x, next_y = x + dx, y + dy
                if (0 <= next_x < len(self.map) and 0 <= next_y < len(self.map[0]) and 
                    self.map[next_x][next_y] not in {1, 4} and (next_x, next_y) not in visited):

                    new_path = path + [(next_x, next_y)]
                    
                    if (next_x, next_y) == end:
                        elapsed_time = time.time() - start_time
                        memory_used = sys.getsizeof(queue) + sys.getsizeof(visited)
                        print(f"Goal reached! Stopping early. Time: {elapsed_time:.6f}s, Memory: {memory_used} bytes")
                        self.path = new_path
                        self.time, self.expanded, self.mem = elapsed_time, expanded_nodes, memory_used
                        return new_path

                    queue.append(new_path)
                    visited.add((next_x, next_y))

        elapsed_time = time.time() - start_time
        memory_used = sys.getsizeof(queue) + sys.getsizeof(visited)
        print(f"No path found. Time: {elapsed_time:.6f}s, Memory: {memory_used} bytes, Nodes: {expanded_nodes}")
        self.path = []
        self.time, self.expanded, self.mem = elapsed_time, expanded_nodes, memory_used
        return []

    def move_dfs(self):
        print("DFS")
        start_time = time.time()  
        path = []
        start = ((self.y_pos - self.offset[1]) // GRID_SIZE, (self.x_pos - self.offset[0]) // GRID_SIZE)
        end = ((self.target[1] - self.offset[1]) // GRID_SIZE, (self.target[0] - self.offset[0]) // GRID_SIZE)

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

        start = ((self.y_pos - self.offset[1]) // GRID_SIZE, (self.x_pos - self.offset[0]) // GRID_SIZE)
        end = ((self.target[1] - self.offset[1]) // GRID_SIZE, (self.target[0] - self.offset[0]) // GRID_SIZE)

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

        start_time = time.time()

        start = ((self.y_pos - self.offset[1]) // GRID_SIZE, (self.x_pos - self.offset[0]) // GRID_SIZE)
        end = ((self.target[1] - self.offset[1]) // GRID_SIZE, (self.target[0] - self.offset[0]) // GRID_SIZE)
        
        def heuristic(x, y):
            return (abs(x - end[0]) + abs(y - end[1])) # Khoảng cách Manhattan
            
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
            
            visited.add((x, y))
            expanded.append((x, y))
            expanded_nodes += 1
           

            if (x, y) == end:
                elapsed_time = time.time() - start_time
                memory_used = sys.getsizeof(visited) + max_pq_size
                print(f"Path found! Time: {elapsed_time:.6f}s, Memory: {memory_used} bytes")
                self.path = path
                self.time, self.expanded, self.mem = elapsed_time, expanded_nodes,  memory_used
                return path

            for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                next_x, next_y = x + dx, y + dy
                if (0 <= next_x < len(self.map) and 0 <= next_y < len(self.map[0]) and self.map[next_x][next_y] != 1 and self.map[next_x][next_y] != 4 ):
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
 