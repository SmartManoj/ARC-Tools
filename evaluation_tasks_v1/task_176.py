import os
from arc_tools.grid import Grid
from arc_tools import logger
from helper import solve_task

def solve(grid: Grid):
    '''
    Find the horizontal marker line containing 1s and non-1 values (2, 8).
    For each non-1 value, extend a vertical line upward:
    - Top cell gets the marker value
    - Cells below get 1s until reaching the marker line
    - Extension height depends on the marker value:
      - Value 2: extends 5 rows total
      - Value 8: extends 4 rows total
    '''
    result = Grid([row[:] for row in grid])
    h, w = result.height, result.width

    # Extension heights for each marker value
    extension_heights = {2: 5, 8: 4}

    # Find the marker line (row containing 1s and other values)
    marker_row = -1
    for r in range(h):
        if 1 in result[r] and (2 in result[r] or 8 in result[r]):
            marker_row = r
            break

    if marker_row == -1:
        return result

    # For each non-1 value in the marker line
    for col in range(w):
        val = result[marker_row][col]
        if val not in [0, 1]:
            # Get extension height for this value
            ext_height = extension_heights.get(val, 0)
            if ext_height == 0:
                continue

            # Calculate top row for extension
            top_row = marker_row - (ext_height - 1)

            # Ensure it doesn't go above the grid
            top_row = max(0, top_row)

            # Place the marker value at the top
            result[top_row][col] = val

            # Fill the rows below with 1s (until just before the marker line)
            for r in range(top_row + 1, marker_row):
                result[r][col] = 1

    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("72a961c9", solve)
