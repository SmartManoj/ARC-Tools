import os
from arc_tools.grid import Grid
from arc_tools import logger
from helper import solve_task

def solve(grid: Grid):
    '''
    Pattern: Creates a checkerboard-like pattern regardless of input

    The transformation creates a specific pattern:
    - Even-indexed rows (0, 2, 4, 6, ...): all cells are 1
    - Odd-indexed rows (1, 3, 5, 7, ...): cells alternate between 1 and 0, starting with 1
      (i.e., columns at even indices are 1, columns at odd indices are 0)

    This creates a pattern like:
    1 1 1 1 1
    1 0 1 0 1
    1 1 1 1 1
    1 0 1 0 1
    1 1 1 1 1
    '''
    height = grid.height
    width = grid.width

    output_data = []

    for row_idx in range(height):
        row = []
        for col_idx in range(width):
            if row_idx % 2 == 0:
                # Even rows: all 1s
                row.append(1)
            else:
                # Odd rows: alternate 1, 0, 1, 0, ...
                if col_idx % 2 == 0:
                    row.append(1)
                else:
                    row.append(0)
        output_data.append(row)

    return Grid(output_data)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("332efdb3", solve)
