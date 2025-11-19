import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Pattern: For each gray (8) hollow rectangle, create both horizontal and vertical
    symmetry for the red (2) pixels within the rectangle.

    Steps:
    1. Find gray (8) rectangular regions
    2. For each rectangle, find the inner area (excluding the border of 8s)
    3. Find all red (2) pixels
    4. Mirror red pixels both horizontally and vertically to create full symmetry
    '''
    # Create output grid as a copy of input
    output = grid.copy()

    # Detect all objects
    objects = detect_objects(grid)

    # Filter to only objects containing gray (8)
    gray_objects = [obj for obj in objects if obj.color == 8]

    for obj in gray_objects:
        # Get the bounding box of this object from the region
        min_col = obj.region.x1
        max_col = obj.region.x2
        min_row = obj.region.y1
        max_row = obj.region.y2

        # Find the inner rectangle (area enclosed by the gray border)
        # The inner area is where we apply symmetry
        inner_min_row, inner_max_row = min_row + 1, max_row - 1
        inner_min_col, inner_max_col = min_col + 1, max_col - 1

        # Skip if inner area is too small
        if inner_min_row >= inner_max_row or inner_min_col >= inner_max_col:
            continue

        # Find all red (2) pixels in the bounding box
        red_pixels = []
        for r in range(min_row, max_row + 1):
            for c in range(min_col, max_col + 1):
                if grid[r][c] == 2:
                    red_pixels.append((r, c))

        if not red_pixels:
            continue

        # Calculate center points for mirroring
        center_row = (inner_min_row + inner_max_row) / 2.0
        center_col = (inner_min_col + inner_max_col) / 2.0

        # Create set of all red pixels (original + mirrors)
        all_red = set(red_pixels)

        # Mirror each red pixel horizontally and vertically
        for r, c in red_pixels:
            # Horizontal mirror (across vertical center line)
            mirror_col = int(2 * center_col - c)
            if inner_min_col <= mirror_col <= inner_max_col:
                all_red.add((r, mirror_col))

            # Vertical mirror (across horizontal center line)
            mirror_row = int(2 * center_row - r)
            if inner_min_row <= mirror_row <= inner_max_row:
                all_red.add((mirror_row, c))

            # Diagonal mirror (both horizontal and vertical)
            if inner_min_col <= mirror_col <= inner_max_col and inner_min_row <= mirror_row <= inner_max_row:
                all_red.add((mirror_row, mirror_col))

        # Apply all red pixels to the output
        for r, c in all_red:
            output[r][c] = 2

    return output

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("18419cfa", solve)
