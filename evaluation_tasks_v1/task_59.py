import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Pattern: Two red (2) pixels define opposite corners of a rectangle.

    Transformation:
    1. Find the two red (2) pixels in the input
    2. Draw red (2) vertical lines spanning the full height at both x-coordinates
    3. Draw red (2) horizontal lines spanning the full width at both y-coordinates
    4. Fill the interior of the rectangle (excluding border lines) with blue (1)
    5. Keep everything else black (0)
    '''
    height = grid.height
    width = grid.width

    # Find the two red pixels
    red_pixels = []
    for y in range(height):
        for x in range(width):
            if grid[y][x] == 2:  # Red color
                red_pixels.append((y, x))

    # Should have exactly 2 red pixels
    if len(red_pixels) != 2:
        logger.error(f"Expected 2 red pixels, found {len(red_pixels)}")
        return grid

    # Get coordinates of the two corners
    y1, x1 = red_pixels[0]
    y2, x2 = red_pixels[1]

    # Ensure we have the proper ordering (min, max)
    min_y, max_y = min(y1, y2), max(y1, y2)
    min_x, max_x = min(x1, x2), max(x1, x2)

    # Create output grid initialized with zeros
    output_data = [[0 for _ in range(width)] for _ in range(height)]

    # Draw vertical lines at min_x and max_x (full height)
    for y in range(height):
        output_data[y][min_x] = 2
        output_data[y][max_x] = 2

    # Draw horizontal lines at min_y and max_y (full width)
    for x in range(width):
        output_data[min_y][x] = 2
        output_data[max_y][x] = 2

    # Fill the interior rectangle with blue (1)
    # Interior is between the lines, not including them
    for y in range(min_y + 1, max_y):
        for x in range(min_x + 1, max_x):
            output_data[y][x] = 1

    return Grid(output_data)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("21f83797", solve)
