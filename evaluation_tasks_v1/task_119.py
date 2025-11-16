import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Pattern: Find a colored marker block (color > 1) and create a cross pattern
    by filling all cells in the same rows and columns with that color,
    but preserving 0's (which act as separators).

    Steps:
    1. Find all cells with color > 1 (the special marker)
    2. Identify which rows and columns contain this marker
    3. Fill all non-zero cells in those rows with the marker color
    4. Fill all non-zero cells in those columns with the marker color
    '''
    # Find the special color and its positions
    special_color = None
    special_rows = set()
    special_cols = set()

    for r in range(grid.height):
        for c in range(grid.width):
            if grid[r][c] > 1:
                special_color = grid[r][c]
                special_rows.add(r)
                special_cols.add(c)

    # Create output grid as a copy
    output = grid.copy()

    # Fill rows where special color appears
    for r in special_rows:
        for c in range(grid.width):
            if grid[r][c] != 0:  # Don't replace 0's
                output[r][c] = special_color

    # Fill columns where special color appears
    for c in special_cols:
        for r in range(grid.height):
            if grid[r][c] != 0:  # Don't replace 0's
                output[r][c] = special_color

    return output

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("4f537728", solve)
