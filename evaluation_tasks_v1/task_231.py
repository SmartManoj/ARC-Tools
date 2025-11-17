import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Find marker pairs (same colored non-0, non-8 pixels) that define rectangles.
    For each rectangle:
    - Fill the border (top row, bottom row, left col, right col) with the marker color
    - Replace the middle cell in each 3x3 block pattern (where center is 0) with the marker color
    '''
    result = grid.copy()

    # Find all markers (non-0, non-8 values)
    markers = {}
    for r in range(grid.height):
        for c in range(grid.width):
            color = grid[r][c]
            if color not in [0, 8]:
                if color not in markers:
                    markers[color] = []
                markers[color].append((r, c))

    # Process each color's markers
    for color, positions in markers.items():
        if len(positions) != 2:
            continue

        # Get the bounding rectangle
        (r1, c1), (r2, c2) = positions
        min_r, max_r = min(r1, r2), max(r1, r2)
        min_c, max_c = min(c1, c2), max(c1, c2)

        # Find the separator rows and columns (where index % 4 == 0) that bound the rectangle
        # If a marker is on a separator, use that; otherwise use the nearest separator
        if min_r % 4 == 0:
            top_separator = min_r
        else:
            top_separator = (min_r // 4) * 4

        if max_r % 4 == 0:
            bottom_separator = max_r
        else:
            bottom_separator = ((max_r // 4) + 1) * 4
            if bottom_separator >= grid.height:
                bottom_separator = grid.height - 1

        if min_c % 4 == 0:
            left_separator = min_c
        else:
            left_separator = (min_c // 4) * 4

        if max_c % 4 == 0:
            right_separator = max_c
        else:
            right_separator = ((max_c // 4) + 1) * 4
            if right_separator >= grid.width:
                right_separator = grid.width - 1

        # Fill the border of the rectangle
        # Top separator row (horizontal)
        for c in range(left_separator, right_separator + 1):
            result[top_separator][c] = color
        # Bottom separator row (horizontal)
        for c in range(left_separator, right_separator + 1):
            result[bottom_separator][c] = color
        # Left separator column (vertical)
        for r in range(top_separator, bottom_separator + 1):
            result[r][left_separator] = color
        # Right separator column (vertical)
        for r in range(top_separator, bottom_separator + 1):
            result[r][right_separator] = color

        # Replace middle cells in 3x3 patterns within the rectangle
        # The middle row of each 3x3 block has pattern: 8 0 8
        # These occur at rows where r % 4 == 2 and cols where c % 4 == 2
        for r in range(top_separator, bottom_separator + 1):
            for c in range(left_separator + 1, right_separator):
                # Check if this is a middle cell in a 3x3 block pattern
                # Middle rows: r % 4 == 2, Middle cols: c % 4 == 2
                if (r % 4 == 2 and c % 4 == 2 and
                    grid[r][c] == 0 and
                    c > 0 and c < grid.width - 1 and
                    grid[r][c - 1] == 8 and grid[r][c + 1] == 8):
                    result[r][c] = color

    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("97239e3d", solve)
