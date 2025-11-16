import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Counts the number of solid 2x2 blocks of color 3 (green) in the input grid.
    Returns a 3x3 grid with 1s along the diagonal equal to the count (max 3).

    Pattern:
    1. Find all 2x2 blocks where all 4 cells are color 3
    2. Count these blocks
    3. Create a 3x3 output grid with that many 1s on the diagonal
    '''
    # Count 2x2 blocks of color 3
    count = 0

    # Check all possible 2x2 positions
    for y in range(grid.height - 1):
        for x in range(grid.width - 1):
            # Check if this 2x2 block is all color 3
            if (grid[y][x] == 3 and
                grid[y][x+1] == 3 and
                grid[y+1][x] == 3 and
                grid[y+1][x+1] == 3):
                count += 1

    # Create 3x3 output grid
    output_data = [[0 for _ in range(3)] for _ in range(3)]

    # Place 1s along the diagonal based on count (max 3)
    for i in range(min(count, 3)):
        output_data[i][i] = 1

    return Grid(output_data)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("3b4c2228", solve)
