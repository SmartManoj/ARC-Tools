import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Replace gray (5) cells with the color from the leftmost non-black cell in the same row.
    Each row has a color marker on the left that indicates what color the gray cells should become.
    '''
    result = grid.copy()

    for r in range(grid.height):
        # Find the leftmost non-black, non-gray color in this row
        row_color = None
        for c in range(grid.width):
            if grid[r, c] != Color.BLACK and grid[r, c] != Color.GRAY:
                row_color = grid[r, c]
                break

        # If we found a row color, replace all gray cells with it
        if row_color is not None:
            for c in range(grid.width):
                if grid[r, c] == Color.GRAY:
                    result[r, c] = row_color

    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("c7d4e6ad", solve)
