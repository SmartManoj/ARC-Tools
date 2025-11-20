import os
from arc_tools.grid import Grid
from arc_tools import logger
from helper import solve_task

def solve(grid: Grid):
    '''
    Divide grid by lines of 3s (both horizontal and vertical).
    For each resulting quadrant, fill with a spiral pattern of 4s and 0s.
    '''
    result = Grid([row[:] for row in grid])
    h, w = result.height, result.width

    # Find horizontal and vertical divider lines (all 3s)
    h_dividers = []
    v_dividers = []

    for r in range(h):
        if all(result[r][c] == 3 for c in range(w)):
            h_dividers.append(r)

    for c in range(w):
        if all(result[r][c] == 3 for r in range(h)):
            v_dividers.append(c)

    # Handle cases with dividers
    if h_dividers and v_dividers:
        # Create quadrants based on dividers
        h_div = h_dividers[0]
        v_div = v_dividers[0]

        quadrants = [
            (list(range(0, h_div)), list(range(0, v_div))),        # top-left
            (list(range(0, h_div)), list(range(v_div + 1, w))),    # top-right
            (list(range(h_div + 1, h)), list(range(0, v_div))),    # bottom-left
            (list(range(h_div + 1, h)), list(range(v_div + 1, w))) # bottom-right
        ]

        for row_indices, col_indices in quadrants:
            if row_indices and col_indices:
                fill_spiral(result, row_indices, col_indices)
    elif h_dividers:
        # Only horizontal divider
        h_div = h_dividers[0]
        fill_spiral(result, list(range(0, h_div)), list(range(w)))
        fill_spiral(result, list(range(h_div + 1, h)), list(range(w)))
    elif v_dividers:
        # Only vertical divider
        v_div = v_dividers[0]
        fill_spiral(result, list(range(h)), list(range(0, v_div)))
        fill_spiral(result, list(range(h)), list(range(v_div + 1, w)))
    else:
        # No dividers - fill entire grid
        fill_spiral(result, list(range(h)), list(range(w)))

    return result


def fill_spiral(grid, rows, cols):
    '''
    Fill a region with a pattern of 4s and 0s using nested layers.
    '''
    if not rows or not cols:
        return

    rows_sorted = sorted(rows)
    cols_sorted = sorted(cols)

    r_min, r_max = rows_sorted[0], rows_sorted[-1]
    c_min, c_max = cols_sorted[0], cols_sorted[-1]

    _fill_region(grid, r_min, r_max, c_min, c_max, 4)


def _fill_region(grid, r_min, r_max, c_min, c_max, start_value):
    '''Recursively fill a rectangular region with alternating pattern.'''
    if r_min > r_max or c_min > c_max:
        return

    height = r_max - r_min + 1
    width = c_max - c_min + 1

    # Fill first row entirely with start_value
    for c in range(c_min, c_max + 1):
        if grid[r_min][c] == 0:
            grid[r_min][c] = start_value

    if height == 1:
        return

    # Fill second row with opposite value
    opposite = 0 if start_value == 4 else 4
    for c in range(c_min, c_max + 1):
        if grid[r_min + 1][c] == 0:
            grid[r_min + 1][c] = opposite

    if height == 2:
        return

    # Fill third row with start_value
    for c in range(c_min, c_max + 1):
        if grid[r_min + 2][c] == 0:
            grid[r_min + 2][c] = start_value

    if height == 3:
        return

    # If there are more rows and columns, recursively handle the rest
    if width > 2:
        # Fix first 2 columns for remaining rows (starting from row 3)
        for r in range(r_min + 3, r_max + 1):
            if grid[r][c_min] == 0:
                grid[r][c_min] = start_value
            if grid[r][c_min + 1] == 0:
                grid[r][c_min + 1] = opposite

        # Recursively fill the inner region
        _fill_region(grid, r_min + 3, r_max, c_min + 2, c_max, opposite)
    else:
        # No more columns to recurse, just fill remaining rows
        if height > 4:
            # Fill remaining rows alternating
            for r in range(r_min + 3, r_max + 1):
                row_offset = r - r_min
                row_value = start_value if row_offset % 2 == 0 else opposite
                for c in range(c_min, c_max + 1):
                    if grid[r][c] == 0:
                        grid[r][c] = row_value

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("759f3fd3", solve)
