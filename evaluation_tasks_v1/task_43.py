import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Finds a completely uniform row or column (all cells have the same non-zero color)
    and returns that color as a 1x1 grid.

    The grid contains horizontal and/or vertical lines of different colors.
    One of these lines will be completely uniform (not interrupted by other colors).
    We need to identify and return the color of that uninterrupted line.
    '''
    rows = len(grid)
    cols = len(grid[0])

    # Check for uniform rows (all cells have same non-zero color)
    for r in range(rows):
        row_values = [grid[r][c] for c in range(cols)]
        # Check if all values are the same and non-zero
        if len(set(row_values)) == 1 and row_values[0] != 0:
            return Grid([[row_values[0]]])

    # Check for uniform columns (all cells have same non-zero color)
    for c in range(cols):
        col_values = [grid[r][c] for r in range(rows)]
        # Check if all values are the same and non-zero
        if len(set(col_values)) == 1 and col_values[0] != 0:
            return Grid([[col_values[0]]])

    # Should not reach here if pattern is correct
    return Grid([[0]])

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("1a2e2828", solve)
