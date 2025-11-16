import os
from arc_tools.grid import Grid
from arc_tools import logger
from helper import solve_task

def solve(grid: Grid):
    '''
    Pattern:
    1. Find the row filled with all 5s (separator line)
    2. Count N = number of rows above the separator
    3. Take the value from diagonal position at index ((N-1) mod 3)
       - This cycles through positions: (0,0), (1,1), (2,2), (0,0), ...
    4. Place this value at the middle column of the last row

    The pattern creates a cycle of diagonal lookups:
    - N=1: use diagonal[0] = position (0,0)
    - N=2: use diagonal[1] = position (1,1)
    - N=3: use diagonal[2] = position (2,2)
    - N=4: use diagonal[0] = position (0,0) again
    '''
    # Find the row with all 5s (separator)
    separator_row = None
    for row_idx in range(grid.height):
        if all(grid[row_idx][col_idx] == 5 for col_idx in range(grid.width)):
            separator_row = row_idx
            break

    # Count rows above the separator
    rows_above = separator_row

    # Calculate which diagonal element to use (cycles with period 3)
    diagonal_index = (rows_above - 1) % 3

    # Get the value from the diagonal position
    value = grid[diagonal_index][diagonal_index]

    # Calculate middle column
    middle_col = grid.width // 2

    # Create output grid (copy of input)
    output_data = [[grid[r][c] for c in range(grid.width)] for r in range(grid.height)]

    # Place the value at the middle column of the last row
    output_data[grid.height - 1][middle_col] = value

    return Grid(output_data)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("27a77e38", solve)
