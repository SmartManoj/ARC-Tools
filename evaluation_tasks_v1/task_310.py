import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Extend a diagonal pattern by doubling the grid size.
    The input contains 2x2 blocks of alternating colors along the diagonal.
    The output continues this pattern to double the dimensions.
    '''
    # Output is double the size
    result = Grid.empty(grid.height * 2, grid.width * 2)

    # Copy the input to the top-left
    for r in range(grid.height):
        for c in range(grid.width):
            result[r, c] = grid[r, c]

    # Find the pattern - look for 2x2 blocks along the diagonal
    # The pattern is typically [[color1, color2], [color2, color1]]
    # Find the colors used
    colors = set()
    for r in range(grid.height):
        for c in range(grid.width):
            if grid[r, c] != Color.BLACK:
                colors.add(grid[r, c])

    if len(colors) == 2:
        color1, color2 = sorted(colors)

        # Continue the diagonal pattern for the rest of the output
        # The pattern repeats as 2x2 blocks along the diagonal
        for i in range(grid.height, result.height, 2):
            if i < result.height and i < result.width:
                result[i, i] = color1
                if i + 1 < result.height and i < result.width:
                    result[i + 1, i] = color2
            if i < result.height and i + 1 < result.width:
                result[i, i + 1] = color2
                if i + 1 < result.height and i + 1 < result.width:
                    result[i + 1, i + 1] = color1

    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("cad67732", solve)
