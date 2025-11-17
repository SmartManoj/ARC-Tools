import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Extract a rectangle bounded by color 1 and transpose it.
    Find the rectangular region filled with 1s (and other colors inside),
    extract it, and return its transpose.
    '''
    import numpy as np

    # Find the bounding box of non-zero values
    non_zero = np.where(grid.data != 0)
    if len(non_zero[0]) == 0:
        return grid

    min_row, max_row = np.min(non_zero[0]), np.max(non_zero[0])
    min_col, max_col = np.min(non_zero[1]), np.max(non_zero[1])

    # Extract the rectangle
    rect = grid.data[min_row:max_row+1, min_col:max_col+1]

    # Transpose it
    transposed = rect.T

    # Return as a new grid
    return Grid(transposed.tolist())

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("94133066", solve)
