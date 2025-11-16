import os
from arc_tools.grid import Grid
from arc_tools import logger
from helper import solve_task

def solve(grid: Grid):
    '''
    Splits the grid by a column of 1s and compares left/right sections.

    Pattern:
    1. Find the divider column (all 1s)
    2. Split grid into left (before divider) and right (after divider) sections
    3. For each position:
       - If both left and right are 0, output is 0
       - Otherwise (if either or both are 4), output is 8
    '''
    # Find the divider column (column with all 1s)
    divider_col = None
    for col in range(grid.width):
        if all(grid[row][col] == 1 for row in range(grid.height)):
            divider_col = col
            break

    if divider_col is None:
        raise ValueError("No divider column found")

    # Build the output by comparing left and right sections
    output_data = []
    for row in range(grid.height):
        output_row = []
        left_section = grid[row][:divider_col]
        right_section = grid[row][divider_col + 1:]

        for col in range(len(left_section)):
            left_val = left_section[col]
            right_val = right_section[col]

            # If both are 0, output is 0; otherwise output is 8
            if left_val == 0 and right_val == 0:
                output_row.append(0)
            else:
                output_row.append(8)

        output_data.append(output_row)

    return Grid(output_data)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("5d2a5c43", solve)
