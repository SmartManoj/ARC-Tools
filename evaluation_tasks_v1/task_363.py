import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Replace bottom half of rectangle with color 2
    '''
    output = [[grid[r][c] for c in range(grid.width)] for r in range(grid.height)]

    # Find all 1s to get bounding box
    ones = [(r, c) for r in range(grid.height) for c in range(grid.width) if grid[r][c] == 1]

    if not ones:
        return grid

    min_r = min(r for r, c in ones)
    max_r = max(r for r, c in ones)
    mid_r = (min_r + max_r) // 2

    # Replace 1s in bottom half with 2s
    for r, c in ones:
        if r > mid_r:
            output[r][c] = 2

    return Grid(output)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("e7dd8335", solve)
