import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Transforms a 2x2 grid into a 6x6 grid by:
    1. Repeating each row 3 times horizontally
    2. Alternating between original and column-reversed versions vertically

    Pattern for 6x6 output:
    - Rows 0-1: Original 2x2, each row repeated 3x horizontally
    - Rows 2-3: Column-reversed 2x2, each row repeated 3x horizontally
    - Rows 4-5: Original 2x2 again, each row repeated 3x horizontally
    '''
    # Get the 2x2 input values
    row0 = [grid[0][0], grid[0][1]]
    row1 = [grid[1][0], grid[1][1]]

    # Create reversed versions (flip columns)
    row0_rev = [grid[0][1], grid[0][0]]
    row1_rev = [grid[1][1], grid[1][0]]

    # Build the 6x6 output
    output_data = []

    # Rows 0-1: Original, repeated 3 times horizontally
    output_data.append(row0 * 3)
    output_data.append(row1 * 3)

    # Rows 2-3: Column-reversed, repeated 3 times horizontally
    output_data.append(row0_rev * 3)
    output_data.append(row1_rev * 3)

    # Rows 4-5: Original again, repeated 3 times horizontally
    output_data.append(row0 * 3)
    output_data.append(row1 * 3)

    return Grid(output_data)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("00576224", solve) 