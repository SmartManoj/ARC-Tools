import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Transform an n×n grid of a single color into a 15×15 grid with grid lines.

    Pattern:
    - Input: n×n grid filled with a single color
    - Output: 15×15 grid where:
      - Grid lines (horizontal and vertical) are placed at positions: n, n+(n+1), n+2*(n+1), etc.
      - The lines use the input color
      - All other cells are 0
    '''
    # Get the input dimensions and color
    h, w = grid.height, grid.width

    # Get the color from the first cell (all cells should have the same color)
    color = grid[0][0]

    # Create 15×15 output grid filled with 0s
    result = Grid([[0 for _ in range(15)] for _ in range(15)])

    # Calculate the step size for placing grid lines
    # For n×n input, step = n + 1
    step = h + 1

    # Place vertical lines
    col = h
    while col < 15:
        for row in range(15):
            result[row][col] = color
        col += step

    # Place horizontal lines
    row = h
    while row < 15:
        for col in range(15):
            result[row][col] = color
        row += step

    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("695367ec", solve)
