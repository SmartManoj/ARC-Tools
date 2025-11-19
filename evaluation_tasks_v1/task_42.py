import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Pattern Analysis:
    - Input has a grey (8) rectangle containing colored 2x2 blocks
    - The grey rectangle is divided into 4 quadrants
    - Each quadrant may contain a 2x2 colored block
    - Output is a 2x2 grid where each cell represents the color found in that quadrant
    - If no colored block in a quadrant, output 0

    Steps:
    1. Find the grey (8) rectangle boundaries
    2. Divide it into 4 equal quadrants
    3. For each quadrant, find the colored 2x2 block (non-0, non-8)
    4. Return 2x2 grid with colors from each quadrant
    '''

    # Find the grey rectangle boundaries
    min_row, max_row = None, None
    min_col, max_col = None, None

    for r in range(grid.height):
        for c in range(grid.width):
            if grid[r][c] == 8:
                if min_row is None:
                    min_row = r
                max_row = r
                if min_col is None or c < min_col:
                    min_col = c
                if max_col is None or c > max_col:
                    max_col = c

    # Calculate quadrant boundaries
    mid_row = (min_row + max_row + 1) // 2
    mid_col = (min_col + max_col + 1) // 2

    # Define quadrants: (row_start, row_end, col_start, col_end)
    quadrants = [
        (min_row, mid_row - 1, min_col, mid_col - 1),      # top-left
        (min_row, mid_row - 1, mid_col, max_col),          # top-right
        (mid_row, max_row, min_col, mid_col - 1),          # bottom-left
        (mid_row, max_row, mid_col, max_col)               # bottom-right
    ]

    # Find colored block in each quadrant
    output = [[0, 0], [0, 0]]

    for quad_idx, (r_start, r_end, c_start, c_end) in enumerate(quadrants):
        # Scan quadrant for colored blocks (non-0, non-8)
        for r in range(r_start, r_end + 1):
            for c in range(c_start, c_end + 1):
                if r < grid.height and c < grid.width:
                    color = grid[r][c]
                    if color != 0 and color != 8:
                        # Found a colored block
                        if quad_idx == 0:  # top-left
                            output[0][0] = color
                        elif quad_idx == 1:  # top-right
                            output[0][1] = color
                        elif quad_idx == 2:  # bottom-left
                            output[1][0] = color
                        else:  # bottom-right
                            output[1][1] = color
                        break
            else:
                continue
            break

    return Grid(output)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("19bb5feb", solve)
