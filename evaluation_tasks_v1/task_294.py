import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Create a pattern from a single-row input with a red cell.
    The pattern expands downward: red cells form a V-shape,
    then blue cells form an inverted V-shape below.
    '''
    # Find the red cell position in the input
    red_col = None
    for c in range(grid.width):
        if grid[0, c] == Color.RED:
            red_col = c
            break

    if red_col is None:
        return grid

    # Calculate output height: red_col + 1 rows for red pattern + red_col rows for blue pattern
    output_height = 2 * red_col + 1
    result = Grid.empty(output_height, grid.width)

    # Copy first row
    for c in range(grid.width):
        result[0, c] = grid[0, c]

    # Create expanding V-shape with red cells
    for i in range(1, red_col + 1):
        left_col = red_col - i
        right_col = red_col + i
        if 0 <= left_col < grid.width:
            result[i, left_col] = Color.RED
        if 0 <= right_col < grid.width:
            result[i, right_col] = Color.RED

    # Create inverted V-shape with blue cells
    for i in range(red_col):
        row = red_col + 1 + i
        col = i + 1
        if row < output_height and col < grid.width:
            result[row, col] = Color.BLUE

    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("c1990cce", solve)
