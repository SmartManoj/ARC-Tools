import os
from arc_tools.grid import Grid
from arc_tools import logger
from helper import solve_task

def solve(grid: Grid):
    '''
    Find the divider row (all 2s) that splits the grid into top and bottom sections.
    Find which columns have non-zero values in the first row and last row.
    Calculate the intersection of these columns.
    If the first row has more non-zero columns, fill between it and the divider with 4s.
    If the last row has more non-zero columns, fill between the divider and it with 4s.
    Fill only the intersection columns.
    '''
    result = Grid([row[:] for row in grid])
    h, w = result.height, result.width

    # Find the divider row (all 2s)
    divider_row = -1
    for r in range(h):
        if all(result[r][c] == 2 for c in range(w)):
            divider_row = r
            break

    if divider_row == -1:
        return result

    # Get first and last rows
    first_row = result[0]
    last_row = result[h - 1]

    # Find which columns have non-zero values in first row
    first_row_cols = set(c for c in range(w) if first_row[c] != 0)

    # Find which columns have non-zero values in last row
    last_row_cols = set(c for c in range(w) if last_row[c] != 0)

    # Find intersection of columns
    intersection_cols = first_row_cols & last_row_cols

    if not intersection_cols:
        return result

    # Determine which section has more non-zero columns
    first_row_count = len(first_row_cols)
    last_row_count = len(last_row_cols)

    # Fill with 4s in the appropriate region
    if first_row_count >= last_row_count:
        # Fill between first row and divider
        for r in range(1, divider_row):
            for c in intersection_cols:
                result[r][c] = 4
    else:
        # Fill between divider and last row
        for r in range(divider_row + 1, h - 1):
            for c in intersection_cols:
                result[r][c] = 4

    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("770cc55f", solve)
