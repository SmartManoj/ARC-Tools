import os
from arc_tools.grid import Grid
from arc_tools import logger
from helper import solve_task

def solve(grid: Grid):
    '''
    Pattern: Find a vertical line of 5s and create triangular patterns on both sides
    - The vertical line of 5s remains in place
    - Left side: Fill with 8s in a downward pattern (full width, then decreasing)
    - Right side: Fill with 6s in a downward contracting pattern
    '''
    # Find the vertical line of 5s
    col_idx = None
    line_length = 0

    for col in range(len(grid[0])):
        count = 0
        for row in range(len(grid)):
            if grid[row][col] == 5:
                count += 1
            else:
                break
        if count > 0:
            col_idx = col
            line_length = count
            break

    # Create output grid (copy of input)
    output = [[grid[row][col] for col in range(len(grid[0]))] for row in range(len(grid))]

    # Fill left side with 8s
    # Pattern: full width (col_idx) for (line_length + 2) rows, then decrease by 1 every 2 rows
    for row in range(len(grid)):
        if row < line_length + 2:
            left_width = col_idx
        else:
            left_width = col_idx - (row - (line_length + 2)) // 2 - 1

        if left_width > 0:
            for col in range(left_width):
                output[row][col] = 8

    # Fill right side with 6s
    # Pattern: starts with ceil((line_length - 2) / 2) width, decreases after first row then every 2 rows
    num_rows_with_6 = line_length - 2
    if num_rows_with_6 > 0:
        initial_width = (num_rows_with_6 + 1) // 2  # ceiling division

        for row in range(num_rows_with_6):
            # Width pattern: row 0 gets initial_width, then decrease by 1 after first row and every 2 rows
            # Formula: max(initial_width - ((row + 1) // 2), 1)
            right_width = max(initial_width - ((row + 1) // 2), 1)
            if right_width > 0:
                for col in range(col_idx + 1, min(col_idx + 1 + right_width, len(grid[0]))):
                    output[row][col] = 6

    return Grid(output)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("5207a7b5", solve)
