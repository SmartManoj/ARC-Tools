import os
import numpy as np
from arc_tools.grid import Grid
from arc_tools import logger
from helper import solve_task
from collections import Counter


def solve(grid: Grid):
    '''
    Pattern: Extract colored rectangles, flip vertically, create filled rectangles,
    and layer them starting from (0,0).

    Steps:
    1. Identify background color (most common)
    2. Find the bounding box containing all non-background pixels
    3. Flip the bounding box vertically
    4. For each color in the original input, create a filled rectangle of that size
    5. Create output sized to the largest rectangle
    6. Layer all filled rectangles starting at (0,0), with largest first
    '''
    # Convert to numpy array
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0
    grid_array = np.array([[grid[r][c] for c in range(width)] for r in range(height)])

    # Find background color (most common)
    flat = grid_array.flatten()
    bg = Counter(flat).most_common(1)[0][0]
    colors = sorted(set(flat) - {bg})

    # Find each rectangle's size in the ORIGINAL input (not flipped)
    rect_sizes = {}
    for color in colors:
        positions = np.where(grid_array == color)
        if len(positions[0]) > 0:
            r_min = positions[0].min()
            r_max = positions[0].max()
            c_min = positions[1].min()
            c_max = positions[1].max()
            height_rect = r_max - r_min + 1
            width_rect = c_max - c_min + 1
            rect_sizes[color] = {
                'height': height_rect,
                'width': width_rect,
                'area': height_rect * width_rect,
                'r_min_orig': r_min  # Store original position for ordering
            }

    # Find largest rectangle (by area)
    largest_color = max(rect_sizes.keys(), key=lambda c: rect_sizes[c]['area'])
    output_height = rect_sizes[largest_color]['height']
    output_width = rect_sizes[largest_color]['width']

    # Create output grid filled with largest color (base layer)
    output = np.full((output_height, output_width), largest_color, dtype=int)

    # Create layering order: largest first, then others sorted by height descending
    other_colors = [c for c in colors if c != largest_color]
    other_colors_sorted = sorted(other_colors, key=lambda c: rect_sizes[c]['height'], reverse=True)
    colors_sorted = [largest_color] + other_colors_sorted

    # Layer filled rectangles at (0, 0), each one on top of previous
    for color in colors_sorted:
        info = rect_sizes[color]
        # Create filled rectangle
        for r in range(min(info['height'], output_height)):
            for c in range(min(info['width'], output_width)):
                output[r, c] = color

    return Grid(output.tolist())


if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("20818e16", solve)
