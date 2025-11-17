import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Tile the input grid N times horizontally and vertically, where N is the
    number of unique colors in the grid.

    For example, if the input is 3x3 with 3 unique colors, the output will be
    a 9x9 grid with the 3x3 pattern repeated 3 times in each direction.
    '''
    # Count unique colors in the grid
    unique_colors = set()
    for row in grid:
        for val in row:
            unique_colors.add(val)

    num_unique = len(unique_colors)

    # Create output grid by tiling the input N times
    height, width = grid.shape
    result = Grid([[0 for _ in range(width * num_unique)] for _ in range(height * num_unique)])

    for tile_r in range(num_unique):
        for tile_c in range(num_unique):
            for r in range(height):
                for c in range(width):
                    result[tile_r * height + r][tile_c * width + c] = grid[r][c]

    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("a59b95c0", solve)
