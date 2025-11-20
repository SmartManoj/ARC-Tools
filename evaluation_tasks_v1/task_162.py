import os
from arc_tools.grid import Grid
from arc_tools import logger
from helper import solve_task

def solve(grid: Grid):
    '''
    Extract elements at alternating indices (0, 2, 4) from both rows and columns.
    This transforms a 6x6 grid into a 3x3 grid.
    '''
    result = []
    # Extract rows at indices 0, 2, 4
    for row_idx in [0, 2, 4]:
        row = grid[row_idx]
        # Extract columns at indices 0, 2, 4
        new_row = [row[col_idx] for col_idx in [0, 2, 4]]
        result.append(new_row)

    return Grid(result)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("68b67ca3", solve)
