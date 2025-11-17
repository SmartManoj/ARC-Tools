import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Reduce 5x5 grid to 2x2 by extracting pattern.
    '''
    # Create 2x2 output
    result = Grid([[0] * 2 for _ in range(2)])

    # Extract pattern
    for r in range(2):
        for c in range(2):
            result[r][c] = grid[r*2][c*2]

    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("be03b35f", solve)
