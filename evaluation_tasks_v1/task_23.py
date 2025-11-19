import os
from arc_tools.grid import Grid
from arc_tools import logger
from helper import solve_task

def solve(grid: Grid):
    '''
    Pattern: Find 3 colored pixels and create a triangle formation at their center.

    1. Identify the 3 non-zero pixels in the input
    2. Keep original pixels unchanged
    3. Add a triangle formation at the center of their bounding box:
       - Two pixels will be on the same row (the "pair")
       - One pixel is alone (the "single")
       - If pair's row < single's row: triangle points down
       - If pair's row > single's row: triangle points up
       - A new pixel with value 5 is placed at the triangle center
    '''
    # Copy the input grid
    output = grid.copy()

    # Find all non-zero pixels
    pixels = []
    for r in range(grid.height):
        for c in range(grid.width):
            if grid[r][c] != 0:
                pixels.append((r, c, grid[r][c]))

    if len(pixels) != 3:
        logger.warning(f"Expected 3 pixels, found {len(pixels)}")
        return output

    # Calculate bounding box center
    rows = [p[0] for p in pixels]
    cols = [p[1] for p in pixels]
    center_row = (min(rows) + max(rows)) // 2
    center_col = (min(cols) + max(cols)) // 2

    # Find which two pixels share the same row (the pair)
    row_counts = {}
    for r, c, val in pixels:
        if r not in row_counts:
            row_counts[r] = []
        row_counts[r].append((r, c, val))

    pair = None
    single = None
    pair_row = None
    single_row = None

    for row, pixel_list in row_counts.items():
        if len(pixel_list) == 2:
            pair = pixel_list
            pair_row = row
        elif len(pixel_list) == 1:
            single = pixel_list[0]
            single_row = row

    if pair is None or single is None:
        logger.warning("Could not find pair and single pixel")
        return output

    # Sort pair by column to get left and right pixels
    pair_sorted = sorted(pair, key=lambda p: p[1])
    left_pixel = pair_sorted[0]
    right_pixel = pair_sorted[1]

    # Determine triangle orientation and place pixels
    if pair_row < single_row:
        # Pair is higher up, triangle points down
        # Top row: pair pixels
        output[center_row - 1][center_col - 1] = left_pixel[2]
        output[center_row - 1][center_col + 1] = right_pixel[2]
        # Middle: value 5
        output[center_row][center_col] = 5
        # Bottom: single pixel
        output[center_row + 1][center_col - 1] = single[2]
    else:
        # Pair is lower down, triangle points up
        # Top: single pixel
        output[center_row - 1][center_col + 1] = single[2]
        # Middle: value 5
        output[center_row][center_col] = 5
        # Bottom row: pair pixels
        output[center_row + 1][center_col - 1] = left_pixel[2]
        output[center_row + 1][center_col + 1] = right_pixel[2]

    return output

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("11e1fe23", solve)
