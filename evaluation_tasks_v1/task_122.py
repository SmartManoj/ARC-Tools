import os
from arc_tools.grid import Grid
from arc_tools import logger
from helper import solve_task


def solve(grid: Grid):
    '''
    The grid is divided by a row of 4s into two sections:
    - Upper section (rows 0-3): contains 0s and 2s
    - Separator (row 4): all 4s
    - Lower section (rows 5-8): contains 0s and 1s

    Pattern: For each position (i, j):
    - If upper[i][j] != 0 OR lower[i][j] != 0, then output[i][j] = 3
    - Otherwise output[i][j] = 0

    This is a logical OR operation where any non-zero value results in 3.
    '''
    # Find the separator row (all 4s)
    separator_row = -1
    for i in range(len(grid)):
        if all(grid[i][j] == 4 for j in range(len(grid[0]))):
            separator_row = i
            break

    if separator_row == -1:
        # If no separator found, return empty grid
        return Grid([[]])

    # Extract upper and lower sections
    upper_rows = separator_row
    lower_start = separator_row + 1

    width = len(grid[0])  # width of grid

    # Create output
    output = []
    for i in range(upper_rows):
        row = []
        for j in range(width):
            upper_val = grid[i][j]
            lower_val = grid[lower_start + i][j]

            # Logical OR: if either is non-zero, output is 3
            if upper_val != 0 or lower_val != 0:
                row.append(3)
            else:
                row.append(0)
        output.append(row)

    return Grid(output)


if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("506d28a5", solve)
