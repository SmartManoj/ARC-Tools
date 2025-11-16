import os
from arc_tools.grid import Grid, detect_objects
from arc_tools import logger
from helper import solve_task


def solve(grid: Grid):
    '''
    Pattern: P-shaped objects made of 5s (gray) need:
    1. Interior filled with 2s (red)
    2. A horizontal line of 2s one row above the shape
    3. Line extends left or right based on where the opening is:
       - If opening (interior column with 0 in top row) is on left, extend right
       - If opening is on right, extend left
    '''
    # Create a copy of the grid as a list of lists for modification
    result = [[cell for cell in row] for row in grid]

    # Detect all objects made of 5s
    objects = detect_objects(grid, ignore_colors=[0])

    for obj in objects:
        if obj.color != 5:  # Only process gray (5) objects
            continue

        # Get bounding box using points
        rows = [p.y for p in obj.points]
        cols = [p.x for p in obj.points]

        if not rows or not cols:
            continue

        min_r, max_r = min(rows), max(rows)
        min_c, max_c = min(cols), max(cols)

        # Find which columns are part of the shape
        shape_cols = sorted(set(cols))

        if len(shape_cols) < 2:
            continue

        # Find interior columns (between leftmost and rightmost)
        left_edge = shape_cols[0]
        right_edge = shape_cols[-1]

        # Fill interior with 2s
        # Interior is defined as 0s within the bounding box that are between the edges
        for r in range(min_r, max_r + 1):
            for c in range(left_edge + 1, right_edge):
                if result[r][c] == 0:
                    result[r][c] = 2

        # Find which interior column has the opening in the top row
        # The opening is the interior column that has 0 in the top row
        opening_col = None
        for c in range(left_edge + 1, right_edge):
            if grid[min_r][c] == 0:
                if opening_col is None:
                    opening_col = c
                    break

        if opening_col is None:
            continue

        # Determine direction based on opening position
        # If opening is closer to left edge, it's a left opening -> extend right
        # If opening is closer to right edge, it's a right opening -> extend left
        mid_point = (left_edge + right_edge) / 2

        # Draw horizontal line one row above the shape
        line_row = min_r - 1
        if line_row < 0:
            continue

        if opening_col < mid_point:
            # Left opening -> extend right
            for c in range(opening_col, len(result[0])):
                result[line_row][c] = 2
        else:
            # Right opening -> extend left
            for c in range(0, opening_col + 1):
                result[line_row][c] = 2

    return Grid(result)


if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("4e469f39", solve)
