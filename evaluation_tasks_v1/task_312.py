import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Tile the input grid NxN times, where N is the size of the input grid.
    '''
    n = grid.height  # Assuming square grid
    result = []
    for _ in range(n):
        for row in grid:
            new_row = list(row) * n
            result.append(new_row)

    return Grid(result)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("ccd554ac", solve)
