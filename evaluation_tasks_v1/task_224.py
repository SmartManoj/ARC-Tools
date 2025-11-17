import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Mirror patterns horizontally within rectangles formed by 8s.
    Find rectangles bounded by 8s and mirror the content inside each
    rectangle horizontally (left side mirrors to right side and vice versa).
    '''
    import numpy as np

    result = grid.copy()

    # Detect objects (rectangles) formed by 8s
    objects = detect_objects(grid, colors=[8], connectivity=2, monochromatic=False)

    for obj in objects:
        # Get bounding box
        min_row, min_col = np.min(obj.points, axis=0)
        max_row, max_col = np.max(obj.points, axis=0)

        # Check if this forms a rectangle border
        # A rectangle should have 8s on the border
        is_rectangle = True

        # Check top and bottom edges
        for c in range(min_col, max_col + 1):
            if grid.data[min_row, c] != 8 or grid.data[max_row, c] != 8:
                is_rectangle = False
                break

        # Check left and right edges
        if is_rectangle:
            for r in range(min_row, max_row + 1):
                if grid.data[r, min_col] != 8 or grid.data[r, max_col] != 8:
                    is_rectangle = False
                    break

        if not is_rectangle:
            continue

        # Mirror the content horizontally inside the rectangle
        inner_min_col = min_col + 1
        inner_max_col = max_col - 1
        inner_min_row = min_row + 1
        inner_max_row = max_row - 1

        if inner_min_col >= inner_max_col:
            continue

        # Calculate middle column
        mid_col = (inner_min_col + inner_max_col) / 2.0

        # Mirror each row
        for r in range(inner_min_row, inner_max_row + 1):
            for c in range(inner_min_col, inner_max_col + 1):
                # Calculate mirrored column
                dist_from_mid = c - mid_col
                mirror_col = int(mid_col - dist_from_mid + 0.5)

                if inner_min_col <= mirror_col <= inner_max_col:
                    # If either position has a non-zero value, copy to both
                    val1 = grid.data[r, c]
                    val2 = grid.data[r, mirror_col]

                    if val1 != 0 and val2 == 0:
                        result.data[r, mirror_col] = val1
                    elif val2 != 0 and val1 == 0:
                        result.data[r, c] = val2

    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("93c31fbe", solve)
