import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Pattern: Remove the object with the fewest 9s (maroon cells).

    The grid contains multiple objects made of 3s (cyan) and 9s (maroon).
    One object is "noise" and should be removed - specifically, the object
    that contains the minimum number of 9s.
    '''
    # Create output as copy of input
    output = grid.copy()

    # Detect all objects (connected components of non-zero cells)
    objects = detect_objects(grid, ignore_colors=[Color.BLACK], go_diagonal=False)

    if len(objects) == 0:
        return output

    # Find the object with the minimum number of 9s
    min_count_9 = float('inf')
    obj_to_remove = None

    for obj in objects:
        count_9 = sum(1 for point in obj.points if grid[point.y][point.x] == 9)

        if count_9 < min_count_9:
            min_count_9 = count_9
            obj_to_remove = obj

    # Remove the object with the fewest 9s
    if obj_to_remove:
        for point in obj_to_remove.points:
            output[point.y][point.x] = 0

    return output

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("54db823b", solve)
