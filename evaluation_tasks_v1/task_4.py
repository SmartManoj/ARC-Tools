import os
from arc_tools.grid import Grid
from arc_tools import logger
from helper import solve_task
import numpy as np

def solve(grid: Grid):
    '''
    Pattern: Diagonal Cascade Transformation

    This task transforms colored objects by:
    1. Identifying all distinct colored regions (by bounding box for each color)
    2. Sorting them from left to right (by leftmost column, then topmost row)
    3. Placing them in a diagonal cascade starting from top-left (0,0)
    4. Each subsequent object overlaps with the previous one at position:
       (prev_row + prev_height - 1, prev_col + prev_width - 1)
    5. Later objects overwrite earlier objects where they overlap

    Example: If objects are horizontally arranged at the bottom of the grid,
    they get rearranged into a diagonal staircase from top-left, with each
    object starting where the previous one almost ends (overlap by 1 cell).
    '''
    # Convert Grid to numpy array for easier manipulation
    grid_array = np.array(list(grid))

    # Find all unique colors (excluding background 0)
    colors = set()
    for row in grid_array:
        for cell in row:
            if cell != 0:
                colors.add(int(cell))

    # For each color, find its bounding box and extract shape
    objects = []
    for color in colors:
        # Find all positions of this color
        positions = np.argwhere(grid_array == color)
        if len(positions) == 0:
            continue

        min_row = int(positions[:, 0].min())
        max_row = int(positions[:, 0].max())
        min_col = int(positions[:, 1].min())
        max_col = int(positions[:, 1].max())

        height = max_row - min_row + 1
        width = max_col - min_col + 1

        # Extract shape (bounding box for this color)
        shape = grid_array[min_row:max_row+1, min_col:max_col+1].copy()

        objects.append({
            'color': color,
            'shape': shape,
            'height': height,
            'width': width,
            'min_col': min_col,
            'min_row': min_row
        })

    # Sort objects by leftmost column, then by topmost row
    # This determines the order they'll appear in the diagonal cascade
    objects.sort(key=lambda obj: (obj['min_col'], obj['min_row']))

    # Create output grid (same size as input)
    output = np.zeros_like(grid_array)

    # Place objects in diagonal cascade pattern
    current_row = 0
    current_col = 0

    for obj in objects:
        # Place this object starting at (current_row, current_col)
        for r in range(obj['height']):
            for c in range(obj['width']):
                if obj['shape'][r, c] != 0:
                    out_r = current_row + r
                    out_c = current_col + c
                    # Check bounds and place
                    if out_r < output.shape[0] and out_c < output.shape[1]:
                        output[out_r, out_c] = obj['shape'][r, c]

        # Next object starts at diagonal offset position
        # This creates the cascading effect with overlap
        current_row += obj['height'] - 1
        current_col += obj['width'] - 1

    return Grid(output.tolist())

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("03560426", solve)
