import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    The task divides the input grid into 4 quadrants using dividing lines,
    then extracts a 3x3 region from each quadrant and combines them into a 6x6 output.

    Algorithm:
    1. Find horizontal and vertical dividing lines (complete rows/cols of same non-zero value)
    2. Split grid into 4 quadrants based on dividing lines
    3. For each quadrant, find bounding box of non-zero colored pixels (excluding divider color)
    4. Extract 3x3 region from each quadrant
    5. Combine four 3x3 regions into 6x6 output
    '''
    height = grid.height
    width = grid.width

    # Find horizontal dividing line
    h_divider_row = None
    h_divider_color = None
    for r in range(height):
        if all(grid[r][c] == grid[r][0] and grid[r][c] != 0 for c in range(width)):
            h_divider_row = r
            h_divider_color = grid[r][0]
            break

    # Find vertical dividing line
    v_divider_col = None
    v_divider_color = None
    for c in range(width):
        if all(grid[r][c] == grid[0][c] and grid[r][c] != 0 for r in range(height)):
            v_divider_col = c
            v_divider_color = grid[0][c]
            break

    # Split into 4 quadrants
    quadrants = []
    divider_colors = {h_divider_color, v_divider_color}

    # Top-left
    quadrants.append({
        'rows': (0, h_divider_row),
        'cols': (0, v_divider_col)
    })

    # Top-right
    quadrants.append({
        'rows': (0, h_divider_row),
        'cols': (v_divider_col + 1, width)
    })

    # Bottom-left
    quadrants.append({
        'rows': (h_divider_row + 1, height),
        'cols': (0, v_divider_col)
    })

    # Bottom-right
    quadrants.append({
        'rows': (h_divider_row + 1, height),
        'cols': (v_divider_col + 1, width)
    })

    # Extract 3x3 region from each quadrant
    regions = []
    for quad in quadrants:
        r_start, r_end = quad['rows']
        c_start, c_end = quad['cols']

        # Find bounding box of non-zero, non-divider colored pixels
        min_r, max_r = None, None
        min_c, max_c = None, None

        for r in range(r_start, r_end):
            for c in range(c_start, c_end):
                val = grid[r][c]
                if val != 0 and val not in divider_colors:
                    if min_r is None or r < min_r:
                        min_r = r
                    if max_r is None or r > max_r:
                        max_r = r
                    if min_c is None or c < min_c:
                        min_c = c
                    if max_c is None or c > max_c:
                        max_c = c

        # Extract 3x3 region (bounding box should be exactly 3x3)
        region = []
        for r in range(min_r, max_r + 1):
            row = []
            for c in range(min_c, max_c + 1):
                row.append(grid[r][c])
            region.append(row)
        regions.append(region)

    # Combine four 3x3 regions into 6x6 output
    output_data = []

    # Top half (top-left and top-right)
    for r in range(3):
        row = regions[0][r] + regions[1][r]
        output_data.append(row)

    # Bottom half (bottom-left and bottom-right)
    for r in range(3):
        row = regions[2][r] + regions[3][r]
        output_data.append(row)

    return Grid(output_data)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("0bb8deee", solve)
