import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Invert the grid: swap the non-zero color with 0, and fill 0s with a color that depends on the input color.
    - Color 3 -> fill with 1
    - Color 5 -> fill with 4
    - Color 8 -> fill with 2
    '''
    result = Grid([row[:] for row in grid])
    h, w = result.height, result.width

    # Find the non-zero color in the input
    non_zero_color = None
    for r in range(h):
        for c in range(w):
            if result[r][c] != 0:
                non_zero_color = result[r][c]
                break
        if non_zero_color is not None:
            break

    # If no non-zero color found, return as is
    if non_zero_color is None:
        return result

    # Map input color to fill color for 0s
    fill_color_map = {
        3: 1,
        5: 4,
        8: 2
    }

    fill_color = fill_color_map.get(non_zero_color, non_zero_color)

    # Transform: swap non-zero with 0, and 0 with fill color
    for r in range(h):
        for c in range(w):
            if result[r][c] == non_zero_color:
                result[r][c] = 0
            else:  # result[r][c] == 0
                result[r][c] = fill_color

    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("6ea4a07e", solve)
