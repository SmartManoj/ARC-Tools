import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    For rows that start and end with 4, replace 7->6 and 8->0
    '''
    result = grid.copy()

    for r in range(grid.height):
        if grid[r][0] == 4 and grid[r][grid.width - 1] == 4:
            for c in range(1, grid.width - 1):
                if result[r][c] == 7:
                    result[r][c] = 6
                elif result[r][c] == 8:
                    result[r][c] = 0

    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("d2acf2cb", solve)
