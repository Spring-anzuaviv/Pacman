import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
from src.BoardGame import draw_board2, screen, draw_board1
from src.specification import *
from src.ghost import *
from src.menu_ScreenGame import menu, level_menu

os.environ['SDL_VIDEO_CENTERED'] = '1'

#tốc độ FPS
timer = pygame.time.Clock()
FPS = 60

# def main():
    # ghost = Ghost(x_coord = 26 , y_coord = 26, target = [26 * 20, 26 * 19], speed = 2, img=GHOST_PINK, direct=0, dead=False, powerup=False, board=boards1)
    # path = ghost.move_ucs()
    # ghost.draw_path()
    # print(path)

    # while True:
    #     timer.tick(FPS)
    #     screen.fill('black')
    #     menu()
        
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             running = False
        
    #     pygame.display.flip()
    # pygame.quit()
    
# main()

# test lại 4 thuật toán
def test_algorithms(ghost):
    algorithms = {
        "BFS": ghost.move_bfs,
        "DFS": ghost.move_dfs,
        "UCS": ghost.move_ucs,
        "A*": ghost.move_astar
    }

    results = {}

    for name, algorithm in algorithms.items():
        start_time = time.time()
        path = algorithm()
        elapsed_time = time.time() - start_time
        memory_used = sys.getsizeof(ghost.path)

 
        if path:
            print(f"{name} - Path found: {path}")
        else:
            print(f"{name} - No path found")

        results[name] = {
            "time": elapsed_time,
            "memory": memory_used,
            "path": path
        }

    return results

ghost = Ghost(x_coord = 26 , y_coord = 26, target = [26 * 20, 26 * 19], speed = 2, img=GHOST_PINK, direct=0, dead=False, powerup=False, board=boards1)

results = test_algorithms(ghost)


for algo, data in results.items():
    print(f"{algo}: Time = {data['time']:.6f}s, Memory = {data['memory']} bytes, Path = {data['path']}")

print( "start ", ghost.x_pos, ghost.y_pos)
print("end ", ghost.target)
