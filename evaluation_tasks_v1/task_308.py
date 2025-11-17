import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Extract a 3x3 grid from specific positions in the 5x5 input.
    The sampling pattern extracts non-zero cells in a diagonal/symmetric pattern.
    '''
    # The 5x5 input has a specific pattern of colored cells
    # We extract them into a 3x3 output following this mapping:
    # Output[0,0] = Input[0,0], Output[0,1] = Input[1,1], Output[0,2] = Input[0,4]
    # Output[1,0] = Input[1,3], Output[1,1] = Input[2,2], Output[1,2] = Input[3,1]
    # Output[2,0] = Input[4,0], Output[2,1] = Input[3,3], Output[2,2] = Input[4,4]

    result = Grid.empty(3, 3)

    # Row 0
    result[0, 0] = grid[0, 0]
    result[0, 1] = grid[1, 1]
    result[0, 2] = grid[0, 4]

    # Row 1
    result[1, 0] = grid[1, 3]
    result[1, 1] = grid[2, 2]
    result[1, 2] = grid[3, 1]

    # Row 2
    result[2, 0] = grid[4, 0]
    result[2, 1] = grid[3, 3]
    result[2, 2] = grid[4, 4]

    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("ca8de6ea", solve)
