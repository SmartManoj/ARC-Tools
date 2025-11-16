import os
from arc_tools.grid import Grid
from arc_tools import logger
from helper import solve_task

def solve(grid: Grid):
    '''
    Pattern: Find a 2x2 block of zeros and extend it as a cross
    1. Locate the 2x2 block of zeros in the input
    2. Set all values in those rows to 0 (except preserve 2s)
    3. Set all values in those columns to 0 (except preserve 2s)
    '''
    # Create a copy of the grid
    output_data = [row[:] for row in grid]

    # Find the 2x2 block of zeros
    zero_rows = None
    zero_cols = None

    for r in range(len(grid) - 1):
        for c in range(len(grid[0]) - 1):
            # Check if we found a 2x2 block of zeros
            if (grid[r][c] == 0 and grid[r][c+1] == 0 and
                grid[r+1][c] == 0 and grid[r+1][c+1] == 0):
                zero_rows = (r, r+1)
                zero_cols = (c, c+1)
                break
        if zero_rows:
            break

    if zero_rows and zero_cols:
        # Zero out the rows (preserving 2s)
        for r in zero_rows:
            for c in range(len(output_data[0])):
                if output_data[r][c] != 2:
                    output_data[r][c] = 0

        # Zero out the columns (preserving 2s)
        for c in zero_cols:
            for r in range(len(output_data)):
                if output_data[r][c] != 2:
                    output_data[r][c] = 0

    return Grid(output_data)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("319f2597", solve)
