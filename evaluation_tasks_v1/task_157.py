import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Take a 4x4 grid with a 2x2 center block (rows 1-2, cols 1-2) surrounded by 0s.
    Expand the 2x2 block to the four corners of the 4x4 grid:
    - Top-left [1][1] → [0][0]
    - Top-right [1][2] → [0][3]
    - Bottom-left [2][1] → [3][0]
    - Bottom-right [2][2] → [3][3]
    '''
    result = Grid([[0] * grid.width for _ in range(grid.height)])

    # Extract the 2x2 center block from the input
    top_left = grid[1][1]
    top_right = grid[1][2]
    bottom_left = grid[2][1]
    bottom_right = grid[2][2]

    # Place them at the four corners
    result[0][0] = top_left
    result[0][grid.width - 1] = top_right
    result[grid.height - 1][0] = bottom_left
    result[grid.height - 1][grid.width - 1] = bottom_right

    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("66e6c45b", solve)
