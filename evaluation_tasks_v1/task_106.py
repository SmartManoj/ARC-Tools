import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Pattern: Draw crosses through colored pixels
    1. Find all non-zero colored pixels in the input
    2. For each pixel at (row, col) with color C:
       - Draw a horizontal line across the entire row with color C
       - Draw a vertical line down the entire column with color C
    3. Where a row from one pixel intersects with a column from a different pixel,
       use color 2 (red) instead
    '''
    height, width = len(grid), len(grid[0])

    # Find all non-zero pixels
    pixels = []
    for r in range(height):
        for c in range(width):
            if grid[r][c] != 0:
                pixels.append((r, c, grid[r][c]))

    # Create output grid (start with zeros)
    output = [[0 for _ in range(width)] for _ in range(height)]

    # For each pixel, draw its cross (horizontal and vertical lines)
    for r, c, color in pixels:
        # Fill the row with this pixel's color
        for col in range(width):
            output[r][col] = color
        # Fill the column with this pixel's color
        for row in range(height):
            output[row][c] = color

    # Mark intersections with color 2 (where row from one pixel meets column from another)
    for i, (r1, c1, color1) in enumerate(pixels):
        for j, (r2, c2, color2) in enumerate(pixels):
            if i != j:
                # Intersection of row from pixel i and column from pixel j
                output[r1][c2] = 2

    return Grid(output)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("45bbe264", solve)
