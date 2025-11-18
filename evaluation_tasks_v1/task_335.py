import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task


def solve(grid: Grid):
    '''
    For each green (color 3) shape (hollow rectangle with a bulge):
    1. Identify which side the bulge is on (left, right, top, or bottom)
    2. Create a mirrored copy:
       - Left/right bulge → horizontal mirror, place opposite side, color blue (1)
       - Top/bottom bulge → vertical mirror, place opposite side, color light blue (8)
    3. Place copy with 1-cell gap from original

    The bulge is identified as the edge that has only one pixel.
    '''
    # Detect all green objects (color 3)
    objects = detect_objects(grid, required_colors=[Color.GREEN], go_diagonal=False)

    output = grid.copy()

    for obj in objects:
        # Get all points (pixels) in the object
        # points is a list of GridPoint objects with x and y attributes
        points = obj.points
        if not points:
            continue

        # Get bounding box from region
        # Note: in GridPoint, x is column and y is row
        min_col, min_row = obj.region.x1, obj.region.y1
        max_col, max_row = obj.region.x2, obj.region.y2

        # Convert points to (row, col) tuples
        cells = [(p.y, p.x) for p in points]

        # Find the bulge by checking which edge has only one pixel
        left_col_pixels = [(r, c) for r, c in cells if c == min_col]
        right_col_pixels = [(r, c) for r, c in cells if c == max_col]
        top_row_pixels = [(r, c) for r, c in cells if r == min_row]
        bottom_row_pixels = [(r, c) for r, c in cells if r == max_row]

        # Determine bulge side
        if len(left_col_pixels) == 1:
            bulge_side = 'left'
        elif len(right_col_pixels) == 1:
            bulge_side = 'right'
        elif len(top_row_pixels) == 1:
            bulge_side = 'top'
        elif len(bottom_row_pixels) == 1:
            bulge_side = 'bottom'
        else:
            # No clear bulge detected, skip this object
            continue

        # Create mirrored copy and place it
        if bulge_side == 'left':
            # Horizontal mirror, place to the right, use blue
            new_color = Color.BLUE.value
            for r, c in cells:
                # Mirror horizontally and shift to the right
                c_final = 2 * max_col + 2 - c
                output[r][c_final] = new_color

        elif bulge_side == 'right':
            # Horizontal mirror, place to the left, use blue
            new_color = Color.BLUE.value
            for r, c in cells:
                # Mirror horizontally and shift to the left
                c_final = 2 * min_col - 2 - c
                output[r][c_final] = new_color

        elif bulge_side == 'top':
            # Vertical mirror, place below, use light blue
            new_color = Color.LIGHT_BLUE.value
            for r, c in cells:
                # Mirror vertically and shift down
                r_final = 2 * max_row + 2 - r
                output[r_final][c] = new_color

        elif bulge_side == 'bottom':
            # Vertical mirror, place above, use light blue
            new_color = Color.LIGHT_BLUE.value
            for r, c in cells:
                # Mirror vertically and shift up
                r_final = 2 * min_row - 2 - r
                output[r_final][c] = new_color

    return output


if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("dc2e9a9d", solve)
