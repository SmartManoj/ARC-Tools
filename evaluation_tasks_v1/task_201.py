import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Find the horizontal dividing line (color 5) and count colors above and below it.
    Return a 2x2 grid filled with the color that has the largest increase from
    the top section to the bottom section.
    '''
    # Find the row with the horizontal divider (color 5)
    divider_row = None
    for row_idx in range(grid.height):
        if all(grid[row_idx][col] == 5 for col in range(grid.width)):
            divider_row = row_idx
            break

    if divider_row is None:
        return grid

    # Count colors above and below the divider (excluding 0 and 5)
    color_counts_above = {}
    color_counts_below = {}

    # Count above the divider
    for row_idx in range(divider_row):
        for col_idx in range(grid.width):
            color = grid[row_idx][col_idx]
            if color != 0 and color != 5:
                color_counts_above[color] = color_counts_above.get(color, 0) + 1

    # Count below the divider
    for row_idx in range(divider_row + 1, grid.height):
        for col_idx in range(grid.width):
            color = grid[row_idx][col_idx]
            if color != 0 and color != 5:
                color_counts_below[color] = color_counts_below.get(color, 0) + 1

    # Find the color with the largest difference (below - above)
    all_colors = set(color_counts_above.keys()) | set(color_counts_below.keys())
    max_diff = -float('inf')
    result_color = None

    for color in all_colors:
        above = color_counts_above.get(color, 0)
        below = color_counts_below.get(color, 0)
        diff = below - above
        if diff > max_diff:
            max_diff = diff
            result_color = color

    # Create a 2x2 grid filled with the result color
    return Grid([[result_color, result_color], [result_color, result_color]])

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("8597cfd7", solve)
