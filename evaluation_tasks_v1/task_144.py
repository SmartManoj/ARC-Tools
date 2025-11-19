import os
from arc_tools.grid import Grid
from arc_tools import logger
from helper import solve_task

def solve(grid: Grid):
    '''
    Transforms a 4x4 grid into a 16x16 grid by treating each input cell
    as a marker for a 4x4 block in the output.

    Pattern:
    1. The output is 4x the input size in each dimension (4x4 -> 16x16)
    2. Divide the output into a 4x4 grid of 4x4 blocks
    3. For each block at position (i, j):
       - If input[i][j] is non-zero: fill the block with the entire input pattern
       - If input[i][j] is zero: fill the block with zeros

    The input essentially acts as a meta-pattern determining where copies
    of itself should appear in the output.
    '''
    height = len(grid)
    width = len(grid[0])

    output_data = []

    # For each row of blocks
    for block_row in range(height):
        # For each row within the blocks
        for local_row in range(height):
            row = []
            # For each column of blocks
            for block_col in range(width):
                # Check if this block should contain the input or zeros
                if grid[block_row][block_col] != 0:
                    # Fill with the corresponding row from the input
                    row.extend(grid[local_row])
                else:
                    # Fill with zeros
                    row.extend([0] * width)
            output_data.append(row)

    return Grid(output_data)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("5b6cbef5", solve)
