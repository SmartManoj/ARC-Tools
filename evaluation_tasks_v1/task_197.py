import os
from arc_tools.grid import Grid
from arc_tools import logger
from helper import solve_task

def solve(grid: Grid):
    '''
    Create a horizontally and vertically symmetric output.

    For each row in the input:
    - Create output row as: reversed(row) + original(row)

    Then stack rows in order:
    - First, all rows from last to first (reversed order)
    - Then, all rows from first to last (original order)

    This creates both horizontal and vertical symmetry.
    '''
    result_rows = []
    h = grid.height
    w = grid.width

    # For each row, create: reversed(row) + original(row)
    row_pairs = []
    for r in range(h):
        row = [grid[r][c] for c in range(w)]
        reversed_row = row[::-1]
        output_row = reversed_row + row
        row_pairs.append(output_row)

    # First add rows in reverse order (rows h-1 down to 0)
    for r in range(h - 1, -1, -1):
        result_rows.append(row_pairs[r])

    # Then add rows in original order (rows 0 to h-1)
    for r in range(h):
        result_rows.append(row_pairs[r])

    # Create result grid
    result = Grid(result_rows)
    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("833dafe3", solve)
