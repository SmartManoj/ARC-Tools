import os
from arc_tools.grid import Grid
from arc_tools import logger
from helper import solve_task

def solve(grid: Grid):
    '''
    Transforms a 5x13 grid into a 5x6 grid by:
    1. The input is divided by column 6 (which contains all 2s)
    2. Left section: columns 0-5
    3. Right section: columns 7-12
    4. For each position (i, j):
       - Output is 1 if left[i][j] == 7 OR right[i][j] == 7
       - Output is 0 if both left[i][j] == 0 AND right[i][j] == 0

    This effectively performs a logical OR operation on the two halves,
    where 7 is treated as True and 0 is treated as False.
    '''
    height = len(grid)
    output_data = []

    for i in range(height):
        row = []
        for j in range(6):  # Output has 6 columns
            left_val = grid[i][j]      # Column 0-5
            right_val = grid[i][j + 7]  # Column 7-12 (skipping column 6)

            # OR operation: 1 if either side has a 7
            if left_val == 7 or right_val == 7:
                row.append(1)
            else:
                row.append(0)

        output_data.append(row)

    return Grid(output_data)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("195ba7dc", solve)
