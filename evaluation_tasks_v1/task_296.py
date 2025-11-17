import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Fill holes in the green (3) region.
    For each row, fill the space between the leftmost and rightmost green cells with green.
    '''
    result = grid.copy()

    # For each row, find leftmost and rightmost green cells and fill between them
    for r in range(grid.height):
        green_cols = []
        for c in range(grid.width):
            if grid[r, c] == Color.GREEN:
                green_cols.append(c)

        if len(green_cols) >= 2:
            # Fill between leftmost and rightmost green cells
            min_col = min(green_cols)
            max_col = max(green_cols)
            for c in range(min_col, max_col + 1):
                if result[r, c] != Color.GREEN:
                    result[r, c] = Color.GREEN

    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("c35c1b4c", solve)
