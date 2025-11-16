import os
from arc_tools.grid import Grid
from arc_tools import logger
from helper import solve_task


def solve(grid: Grid):
    '''
    Pattern: Find a rectangular canvas region and overlay patterns from outside onto it
    based on matching special colors.

    Steps:
    1. Find the largest rectangular region filled with a single color (the canvas)
    2. Extract the canvas as the base output
    3. Find patterns with 2s around special colors outside the canvas
    4. For each special color that appears in both a pattern and the canvas:
       - Overlay the pattern at the canvas position of that color
       - Only overlay non-zero values (2s and special colors)
    '''
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0

    # Find the canvas - largest rectangular region of one color (excluding 0 and 2)
    canvas_color = None
    canvas_bounds = None
    max_area = 0

    # Try each potential canvas color
    for test_color in range(1, 10):
        if test_color == 2:
            continue

        # Find all positions with this color
        positions = []
        for r in range(height):
            for c in range(width):
                if grid[r][c] == test_color:
                    positions.append((r, c))

        if not positions:
            continue

        # Find bounding box
        min_r = min(p[0] for p in positions)
        max_r = max(p[0] for p in positions)
        min_c = min(p[1] for p in positions)
        max_c = max(p[1] for p in positions)

        area = (max_r - min_r + 1) * (max_c - min_c + 1)

        # Check if this forms a solid rectangle (mostly filled)
        rect_cells = (max_r - min_r + 1) * (max_c - min_c + 1)
        filled_cells = len(positions)

        if filled_cells >= rect_cells * 0.7 and area > max_area:  # At least 70% filled
            max_area = area
            canvas_color = test_color
            canvas_bounds = (min_r, max_r, min_c, max_c)

    if canvas_color is None:
        return grid

    min_r, max_r, min_c, max_c = canvas_bounds
    canvas_height = max_r - min_r + 1
    canvas_width = max_c - min_c + 1

    # Extract canvas
    output = [[grid[min_r + r][min_c + c] for c in range(canvas_width)]
              for r in range(canvas_height)]

    # Find all special colors (non-0, non-2, non-canvas-color) and their positions
    special_colors = {}
    for r in range(height):
        for c in range(width):
            val = grid[r][c]
            if val != 0 and val != 2 and val != canvas_color:
                if val not in special_colors:
                    special_colors[val] = []
                special_colors[val].append((r, c))

    # For each special color, check if it appears both inside and outside the canvas
    for color, positions in special_colors.items():
        # Find position of this color within the canvas (target position)
        canvas_positions = [p for p in positions if min_r <= p[0] <= max_r and min_c <= p[1] <= max_c]

        # Find positions outside the canvas (pattern positions)
        pattern_positions = [p for p in positions if not (min_r <= p[0] <= max_r and min_c <= p[1] <= max_c)]

        if not canvas_positions or not pattern_positions:
            continue  # Need both inside and outside occurrences

        # Use the first occurrence of each
        canvas_r, canvas_c = canvas_positions[0]
        pattern_r, pattern_c = pattern_positions[0]

        # Find the pattern: connected region of 2s around the pattern position
        # We'll extract a bounding box around the pattern position that includes all nearby 2s
        pattern_cells = {}  # (offset_r, offset_c): value

        # Find all 2s and the special color within a small region
        for dr in range(-2, 3):
            for dc in range(-2, 3):
                check_r = pattern_r + dr
                check_c = pattern_c + dc
                if 0 <= check_r < height and 0 <= check_c < width:
                    val = grid[check_r][check_c]
                    if val == 2 or val == color:
                        pattern_cells[(dr, dc)] = val

        # Overlay the pattern onto the output at the canvas position
        for (dr, dc), val in pattern_cells.items():
            out_r = (canvas_r - min_r) + dr
            out_c = (canvas_c - min_c) + dc

            if 0 <= out_r < canvas_height and 0 <= out_c < canvas_width:
                output[out_r][out_c] = val

    return Grid(output)


if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("414297c0", solve)
