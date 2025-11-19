import os
from arc_tools.grid import Grid, detect_objects
from arc_tools import logger
from helper import solve_task

def solve(grid: Grid):
    '''
    Detects red (color 2) objects in the input grid and arranges them in a 7x7 output.

    Pattern:
    1. Find all red objects (ignoring black background)
    2. Sort objects by position (top-to-bottom, left-to-right)
    3. Take the first 4 objects
    4. Split into two rows (first 2 and last 2 objects)
    5. Within each row, sort by x-coordinate (left-to-right)
    6. Arrange in a 2x2 grid of 3x3 objects with separators:
       - Top row: leftmost and rightmost objects (rows 0-2, cols 0-2 and 4-6)
       - Bottom row: leftmost and rightmost objects (rows 4-6, cols 0-2 and 4-6)
       - Row 3 and column 3 are separators (all 0s)
    '''
    # Detect red objects
    objects = detect_objects(grid, ignore_colors=[0])

    # Sort by position (top-to-bottom, left-to-right)
    objects_sorted = sorted(objects, key=lambda obj: (obj.region.y1, obj.region.x1))

    # Create 7x7 output grid (all zeros initially)
    output = [[0] * 7 for _ in range(7)]

    # Split into top row and bottom row, then sort each by x-coordinate
    top_row = sorted(objects_sorted[:2], key=lambda obj: obj.region.x1)
    bottom_row = sorted(objects_sorted[2:4], key=lambda obj: obj.region.x1)

    # Place objects in 2x2 grid layout
    all_objects = [
        (top_row[0], 0, 0),      # top-left
        (top_row[1], 0, 4),      # top-right
        (bottom_row[0], 4, 0),   # bottom-left
        (bottom_row[1], 4, 4),   # bottom-right
    ]

    for obj, row_offset, col_offset in all_objects:
        # Copy the 3x3 object into the output
        for r in range(obj.height):
            for c in range(obj.width):
                output[row_offset + r][col_offset + c] = obj[r][c]

    return Grid(output)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("1990f7a8", solve)
