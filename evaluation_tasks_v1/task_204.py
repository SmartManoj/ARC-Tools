import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Creates a 15x15 pattern from a 3x3 input:
    - 5x5 grid of 3x3 blocks
    - Each input cell (i,j) maps to output block (i+1, j+1)
    - Filled blocks (all 5s) where input has 5, otherwise input pattern or empty
    '''
    # Create 15x15 output grid (5x5 grid of 3x3 blocks)
    output = [[0] * 15 for _ in range(15)]

    # Helper to place a 3x3 pattern at block position
    def place_block(block_row, block_col, pattern):
        for i in range(3):
            for j in range(3):
                output[block_row * 3 + i][block_col * 3 + j] = pattern[i][j]

    # Create filled 3x3 block (all 5s)
    filled = [[5, 5, 5], [5, 5, 5], [5, 5, 5]]

    # Get input as 2D list
    input_pattern = [[grid[i][j] for j in range(3)] for i in range(3)]

    # Map each input cell to corresponding output block
    for i in range(3):
        for j in range(3):
            block_row = i + 1
            block_col = j + 1

            if input_pattern[i][j] == 5:
                # Place filled block where input has 5
                place_block(block_row, block_col, filled)

    # Extend pattern to cross edges (only if corresponding middle cell has 5)
    if input_pattern[0][1] == 5:  # Top middle
        place_block(0, 2, input_pattern)
    if input_pattern[2][1] == 5:  # Bottom middle
        place_block(4, 2, input_pattern)
    if input_pattern[1][0] == 5:  # Middle left
        place_block(2, 0, input_pattern)
    if input_pattern[1][2] == 5:  # Middle right
        place_block(2, 4, input_pattern)

    # Add corner extensions based on input corners
    if input_pattern[0][0] == 5:
        place_block(0, 1, input_pattern)
        place_block(1, 0, input_pattern)
    if input_pattern[0][2] == 5:
        place_block(0, 3, input_pattern)
    if input_pattern[2][0] == 5:
        place_block(4, 1, input_pattern)
    if input_pattern[2][2] == 5:
        place_block(3, 3, filled)
        place_block(3, 4, input_pattern)
        place_block(4, 3, input_pattern)

    return Grid(output)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("8719f442", solve)
