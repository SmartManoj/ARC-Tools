import os
from arc_tools.grid import Grid
from arc_tools import logger
from helper import solve_task

def solve(grid: Grid):
    '''
    Extract the grid structure by counting regions separated by divider lines.
    The grid is divided by horizontal and vertical lines (a separator value).
    Output dimensions = (number of horizontal regions) × (number of vertical regions)
    All cells in output are filled with the background value.
    '''
    h, w = grid.height, grid.width

    # Find unique values
    values = set()
    for row in grid:
        values.update(row)

    if len(values) != 2:
        return Grid([[0]])

    # Determine separator and background values
    v1, v2 = list(values)
    count_v1 = sum(row.count(v1) for row in grid)
    count_v2 = sum(row.count(v2) for row in grid)

    # Separator is the less common value
    if count_v1 < count_v2:
        separator, background = v1, v2
    else:
        separator, background = v2, v1

    # Find complete separator rows (all cells in row are separator value)
    separator_rows = []
    for r in range(h):
        if all(grid[r][c] == separator for c in range(w)):
            separator_rows.append(r)

    # Find complete separator columns (all cells in column are separator value)
    separator_cols = []
    for c in range(w):
        if all(grid[r][c] == separator for r in range(h)):
            separator_cols.append(c)

    # Count regions by finding consecutive non-separator rows
    row_regions = 0
    in_region = False
    for r in range(h):
        if r not in separator_rows:
            if not in_region:
                row_regions += 1
                in_region = True
        else:
            in_region = False

    # Count regions by finding consecutive non-separator columns
    col_regions = 0
    in_region = False
    for c in range(w):
        if c not in separator_cols:
            if not in_region:
                col_regions += 1
                in_region = True
        else:
            in_region = False

    # Create output grid filled with background value
    result = Grid([[background] * col_regions for _ in range(row_regions)])

    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("7039b2d7", solve)
