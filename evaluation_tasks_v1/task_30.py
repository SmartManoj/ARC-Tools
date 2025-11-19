import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Pattern Analysis for task 140c817e:

    For each blue pixel (value 1) in the input:
    1. Draw a horizontal line (fill entire row with 1)
    2. Draw a vertical line (fill entire column with 1)
    3. Replace the original pixel with red (2) - intersection point
    4. Add cyan pixels (3) at the 4 diagonal positions (top-left, top-right,
       bottom-left, bottom-right) forming a small diagonal cross around the red center

    The output is a grid with crossing lines centered on each original blue pixel,
    with cyan markers at the diagonal positions around each intersection.
    '''
    height = grid.height
    width = grid.width

    # Start with a copy of the input grid
    output = [[grid[r][c] for c in range(width)] for r in range(height)]

    # Find all blue pixels (value 1) in the input
    blue_pixels = []
    for r in range(height):
        for c in range(width):
            if grid[r][c] == 1:
                blue_pixels.append((r, c))

    # For each blue pixel, draw the cross pattern
    for r, c in blue_pixels:
        # Fill the entire row with 1
        for col in range(width):
            output[r][col] = 1

        # Fill the entire column with 1
        for row in range(height):
            output[row][c] = 1

        # Set the center pixel to red (2)
        output[r][c] = 2

        # Set diagonal pixels to cyan (3) if within bounds
        # Top-left
        if r > 0 and c > 0:
            output[r-1][c-1] = 3
        # Top-right
        if r > 0 and c < width - 1:
            output[r-1][c+1] = 3
        # Bottom-left
        if r < height - 1 and c > 0:
            output[r+1][c-1] = 3
        # Bottom-right
        if r < height - 1 and c < width - 1:
            output[r+1][c+1] = 3

    return Grid(output)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("140c817e", solve)
