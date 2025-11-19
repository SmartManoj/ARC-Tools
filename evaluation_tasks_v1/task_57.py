import os
from arc_tools.grid import Grid
from arc_tools import logger
from helper import solve_task

def solve(grid: Grid):
    '''
    Pattern: The grid is divided into rectangular cells by red (2) dividers.
    Within each cell, blue (1) pixels are shifted away from the cell boundaries:
    - If blue pixels touch the first row of a cell: shift down by 1
    - If blue pixels touch the last row of a cell: shift up by 1
    - If blue pixels touch the first column of a cell: shift right by 1
    - If blue pixels touch the last column of a cell: shift left by 1
    - Red divider pixels remain unchanged
    '''
    height = grid.height
    width = grid.width

    # Find divider rows and columns (cells with value 2)
    divider_rows = []
    divider_cols = set()

    for r in range(height):
        if 2 in grid[r]:
            divider_rows.append(r)
            for c in range(width):
                if grid[r][c] == 2:
                    divider_cols.add(c)

    divider_cols = sorted(divider_cols)

    # Create output grid initialized with input
    output = [row[:] for row in grid]

    # Process each cell defined by dividers
    # Include regions before first divider and after last divider
    row_ranges = []
    if divider_rows:
        if divider_rows[0] > 0:
            row_ranges.append((0, divider_rows[0]))
        for i in range(len(divider_rows) - 1):
            row_ranges.append((divider_rows[i] + 1, divider_rows[i + 1]))
        if divider_rows[-1] < height - 1:
            row_ranges.append((divider_rows[-1] + 1, height))
    else:
        row_ranges.append((0, height))

    col_ranges = []
    if divider_cols:
        if divider_cols[0] > 0:
            col_ranges.append((0, divider_cols[0]))
        for i in range(len(divider_cols) - 1):
            col_ranges.append((divider_cols[i] + 1, divider_cols[i + 1]))
        if divider_cols[-1] < width - 1:
            col_ranges.append((divider_cols[-1] + 1, width))
    else:
        col_ranges.append((0, width))

    # Process each cell
    for r_start, r_end in row_ranges:
        for c_start, c_end in col_ranges:
            # Find all blue pixels in this cell
            blue_pixels = []
            for r in range(r_start, r_end):
                for c in range(c_start, c_end):
                    if grid[r][c] == 1:
                        blue_pixels.append((r, c))

            if not blue_pixels:
                continue

            # Determine which boundaries the object touches
            min_r = min(r for r, c in blue_pixels)
            max_r = max(r for r, c in blue_pixels)
            min_c = min(c for r, c in blue_pixels)
            max_c = max(c for r, c in blue_pixels)

            touches_first_row = (min_r == r_start)
            touches_last_row = (max_r == r_end - 1)
            touches_first_col = (min_c == c_start)
            touches_last_col = (max_c == c_end - 1)

            # Calculate shift
            shift_r = 0
            shift_c = 0

            if touches_first_row:
                shift_r = 1
            elif touches_last_row:
                shift_r = -1

            if touches_first_col:
                shift_c = 1
            elif touches_last_col:
                shift_c = -1

            # Clear original blue pixels in this cell
            for r, c in blue_pixels:
                output[r][c] = 0

            # Place shifted blue pixels
            for r, c in blue_pixels:
                new_r = r + shift_r
                new_c = c + shift_c
                if 0 <= new_r < height and 0 <= new_c < width:
                    output[new_r][new_c] = 1

    return Grid(output)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("20981f0e", solve)
