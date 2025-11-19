import os
from arc_tools.grid import Grid
from arc_tools import logger
from helper import solve_task

def solve(grid: Grid):
    '''
    Pattern: This task identifies grid separators (rows/columns of all 0s) and colors them:
    - Separator columns/rows become color 2 (red) where they separate blocks of 5s
    - Separator columns/rows become color 1 (blue) at boundaries (no 5s on one side)

    Algorithm:
    1. Identify separator columns: columns that are all 0s with 5s somewhere left AND right
    2. Identify separator rows: rows that are all 0s with 5s somewhere above AND below
    3. For each separator column:
       - If row is also a separator row, set to 2
       - Else if the row has 5s on both left and right of this column, set to 2
       - Else set to 1
    4. For each separator row:
       - If column is also a separator column, set to 2 (already handled)
       - Else if the column has 5s above and below this row, set to 2
       - Else set to 1
    '''
    height = grid.height
    width = grid.width

    # Copy input to output
    output = [[grid[r][c] for c in range(width)] for r in range(height)]

    # Identify separator columns (all 0s with 5s on both sides)
    separator_cols = []
    for c in range(width):
        # Check if column is all 0s
        if all(grid[r][c] == 0 for r in range(height)):
            # Check if there are 5s somewhere to the left
            has_5_left = any(grid[r][cc] == 5 for r in range(height) for cc in range(c))
            # Check if there are 5s somewhere to the right
            has_5_right = any(grid[r][cc] == 5 for r in range(height) for cc in range(c+1, width))
            if has_5_left and has_5_right:
                separator_cols.append(c)

    # Identify separator rows (all 0s with 5s above and below)
    separator_rows = []
    for r in range(height):
        # Check if row is all 0s
        if all(grid[r][c] == 0 for c in range(width)):
            # Check if there are 5s somewhere above
            has_5_above = any(grid[rr][c] == 5 for rr in range(r) for c in range(width))
            # Check if there are 5s somewhere below
            has_5_below = any(grid[rr][c] == 5 for rr in range(r+1, height) for c in range(width))
            if has_5_above and has_5_below:
                separator_rows.append(r)

    logger.info(f"Separator columns: {separator_cols}")
    logger.info(f"Separator rows: {separator_rows}")

    # Process separator columns
    for c in separator_cols:
        for r in range(height):
            if r in separator_rows:
                # Both row and column are separators
                output[r][c] = 2
            else:
                # Check if row r has 5s to the left and right of column c
                has_5_left = any(grid[r][cc] == 5 for cc in range(c))
                has_5_right = any(grid[r][cc] == 5 for cc in range(c+1, width))
                if has_5_left and has_5_right:
                    output[r][c] = 2
                else:
                    output[r][c] = 1

    # Process separator rows
    for r in separator_rows:
        for c in range(width):
            if c not in separator_cols:  # Already processed separator cols
                # Check if column c has 5s above and below row r
                has_5_above = any(grid[rr][c] == 5 for rr in range(r))
                has_5_below = any(grid[rr][c] == 5 for rr in range(r+1, height))
                if has_5_above and has_5_below:
                    output[r][c] = 2
                else:
                    output[r][c] = 1

    return Grid(output)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("137f0df0", solve)
