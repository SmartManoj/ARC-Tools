import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Find the rectangular region bounded by 5s.
    Within the interior of this region, swap the two non-zero, non-5 values.
    Keep the border (5s) and exterior unchanged.
    '''
    result = Grid([row[:] for row in grid])
    h, w = result.height, result.width

    # Find all positions with 5s
    rows_with_5 = set()
    cols_with_5 = set()
    for r in range(h):
        for c in range(w):
            if result[r][c] == 5:
                rows_with_5.add(r)
                cols_with_5.add(c)

    if not rows_with_5:
        return result

    # Find the bounds of the 5-bordered region
    min_row = min(rows_with_5)
    max_row = max(rows_with_5)
    min_col = min(cols_with_5)
    max_col = max(cols_with_5)

    # Interior is the region inside the 5s border
    interior_r_start = min_row + 1
    interior_r_end = max_row
    interior_c_start = min_col + 1
    interior_c_end = max_col

    # Find non-zero, non-5 values in the interior
    values_set = set()
    for r in range(interior_r_start, interior_r_end):
        for c in range(interior_c_start, interior_c_end):
            val = result[r][c]
            if val != 0 and val != 5:
                values_set.add(val)

    values_list = sorted(list(values_set))

    if len(values_list) < 2:
        return result

    # Get the two values to swap
    val1, val2 = values_list[0], values_list[1]

    # Swap these values in the interior
    for r in range(interior_r_start, interior_r_end):
        for c in range(interior_c_start, interior_c_end):
            if result[r][c] == val1:
                result[r][c] = val2
            elif result[r][c] == val2:
                result[r][c] = val1

    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("7ee1c6ea", solve)
