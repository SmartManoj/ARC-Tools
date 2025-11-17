import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Split the grid at the column of 4s (separator).
    For each cell in the left and right halves, output 2 if either side is non-zero, else 0.
    '''
    # Find the separator column (all 4s)
    separator_col = None
    for col in range(grid.width):
        if all(grid[row][col] == 4 for row in range(grid.height)):
            separator_col = col
            break

    if separator_col is None:
        return grid

    # Create output grid
    result_data = []
    for row in range(grid.height):
        result_row = []
        for col_offset in range(separator_col):
            left_val = grid[row][col_offset]
            right_val = grid[row][separator_col + 1 + col_offset]

            # Output 2 if either side is non-zero, else 0
            if left_val != 0 or right_val != 0:
                result_row.append(2)
            else:
                result_row.append(0)
        result_data.append(result_row)

    return Grid(result_data)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("e133d23d", solve)
