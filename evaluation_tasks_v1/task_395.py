import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Draw rectangle border using the non-zero color found in input
    '''
    # Find the non-zero color
    color = None
    for r in range(grid.height):
        for c in range(grid.width):
            if grid[r][c] != 0:
                color = grid[r][c]
                break
        if color is not None:
            break

    if color is None:
        return grid

    # Create output with border
    output = [[0] * grid.width for _ in range(grid.height)]

    # Draw border
    for r in range(grid.height):
        for c in range(grid.width):
            if r == 0 or r == grid.height - 1 or c == 0 or c == grid.width - 1:
                output[r][c] = color

    return Grid(output)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("fc754716", solve)
