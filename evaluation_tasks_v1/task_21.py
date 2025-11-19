import os
from arc_tools.grid import Grid, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Pattern: Each colored pixel defines a horizontal rectangular region.

    1. Find all non-zero pixels and sort by row position
    2. Divide the grid into regions using midpoints between consecutive pixels
    3. For each region:
       - Draw horizontal borders on:
         * Row 0 (if first region)
         * The pixel's row (always)
         * Last row of grid (if last region)
       - Draw vertical borders on columns 0 and 14 (leftmost and rightmost)
       - Fill interior with 0
    '''
    height = grid.height
    width = grid.width

    # Find all colored pixels (non-zero)
    colored_pixels = []
    for row in range(height):
        for col in range(width):
            if grid[row][col] != 0:
                colored_pixels.append((row, col, grid[row][col]))

    # Sort by row position
    colored_pixels.sort(key=lambda p: p[0])

    if not colored_pixels:
        return grid

    # Calculate region boundaries for each pixel
    regions = []
    for i, (pixel_row, pixel_col, color) in enumerate(colored_pixels):
        if i == 0:
            # First region starts at row 0
            start_row = 0
        else:
            # Region starts one row after the midpoint with previous pixel
            prev_pixel_row = colored_pixels[i-1][0]
            midpoint = (prev_pixel_row + pixel_row) // 2
            start_row = midpoint + 1

        if i == len(colored_pixels) - 1:
            # Last region ends at last row
            end_row = height - 1
        else:
            # Region ends at the midpoint with next pixel
            next_pixel_row = colored_pixels[i+1][0]
            end_row = (pixel_row + next_pixel_row) // 2

        regions.append((start_row, end_row, pixel_row, color))

    # Create output grid
    output_data = [[0 for _ in range(width)] for _ in range(height)]

    # Draw each region
    for region_idx, (start_row, end_row, pixel_row, color) in enumerate(regions):
        is_first = (region_idx == 0)
        is_last = (region_idx == len(regions) - 1)

        for row in range(start_row, end_row + 1):
            for col in range(width):
                # Check if this cell should be colored
                is_top_border = (row == start_row and is_first)  # Only for first region
                is_pixel_row = (row == pixel_row)  # Horizontal line at pixel row
                is_bottom_border = (row == end_row and is_last)  # Only for last region
                is_left_border = (col == 0)  # Left edge
                is_right_border = (col == width - 1)  # Right edge

                if is_top_border or is_pixel_row or is_bottom_border or is_left_border or is_right_border:
                    output_data[row][col] = color

    return Grid(output_data)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("0f63c0b9", solve)
