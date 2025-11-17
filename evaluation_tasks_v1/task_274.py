import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Remove or transform specific colors based on pattern rules.
    '''
    result = grid.copy()

    # Remove color 5 or apply specific transformation
    for r in range(result.height):
        for c in range(result.width):
            if result[r][c] == 5:
                result[r][c] = 0

    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("b457fec5", solve)
