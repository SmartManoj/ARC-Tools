import os
from arc_tools.grid import Grid
from arc_tools import logger
from collections import Counter
from helper import solve_task

def solve(grid: Grid):
    '''
    Pattern:
    1. Find the most frequent value in the 3x3 input
    2. Identify all positions (r, c) where this value appears
    3. Create a 9x9 output grid (3x3 blocks of 3x3 each)
    4. Place the input at each block position (r, c) where the most frequent value was found

    The output is a 9x9 grid divided into 3x3 blocks.
    Each position where the most frequent value appears becomes a "block coordinate"
    where we place a copy of the entire input.
    '''

    # Count value frequencies in the input
    flat_values = [grid[r][c] for r in range(grid.height) for c in range(grid.width)]
    counter = Counter(flat_values)
    most_frequent_value = counter.most_common(1)[0][0]

    # Find all positions where the most frequent value appears
    positions = []
    for r in range(grid.height):
        for c in range(grid.width):
            if grid[r][c] == most_frequent_value:
                positions.append((r, c))

    # Create 9x9 output grid filled with zeros
    output_data = [[0 for _ in range(9)] for _ in range(9)]

    # Place the input at each block position
    for block_r, block_c in positions:
        # Copy the entire 3x3 input to this block position
        for r in range(3):
            for c in range(3):
                output_row = block_r * 3 + r
                output_col = block_c * 3 + c
                output_data[output_row][output_col] = grid[r][c]

    return Grid(output_data)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("27f8ce4f", solve)
