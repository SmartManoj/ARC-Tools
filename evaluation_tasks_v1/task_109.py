import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Transforms input grid by:
    1. Inverting colors (swap 0 with non-zero values, non-zero with 0)
    2. Tiling the inverted grid in a 2x2 pattern (doubling dimensions)

    Pattern:
    - Find the non-zero color in the input
    - Swap all 0s with that color and all instances of that color with 0
    - Create output that tiles the inverted grid 2 times horizontally and 2 times vertically
    '''
    height = len(grid)
    width = len(grid[0])

    # Find the non-zero color in the grid
    non_zero_color = None
    for row in grid:
        for cell in row:
            if cell != 0:
                non_zero_color = cell
                break
        if non_zero_color is not None:
            break

    # Create inverted grid (swap 0 with non-zero color)
    inverted = []
    for row in grid:
        inverted_row = []
        for cell in row:
            if cell == 0:
                inverted_row.append(non_zero_color)
            else:
                inverted_row.append(0)
        inverted.append(inverted_row)

    # Tile the inverted grid 2x2
    output_data = []

    # Repeat the pattern twice vertically
    for _ in range(2):
        # For each row in the inverted grid
        for row in inverted:
            # Repeat the row twice horizontally
            output_data.append(row * 2)

    return Grid(output_data)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("48131b3c", solve)
