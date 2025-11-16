import os
from arc_tools.grid import Grid
from helper import solve_task

def solve(grid: Grid):
    '''
    Extracts non-zero values from a sparse grid divided into 3x3 blocks.

    The input grid is divided into a 3x3 grid of blocks, and each block contains
    exactly one non-zero value. The output is a 3x3 grid containing these values
    in their corresponding positions.
    '''
    height = len(grid)
    width = len(grid[0])

    # Calculate block size
    block_height = height // 3
    block_width = width // 3

    # Create 3x3 output
    output_data = []

    for block_row in range(3):
        row_data = []
        for block_col in range(3):
            # Find the non-zero value in this block
            start_row = block_row * block_height
            end_row = start_row + block_height
            start_col = block_col * block_width
            end_col = start_col + block_width

            # Search for non-zero value in this block
            value = 0
            for r in range(start_row, end_row):
                for c in range(start_col, end_col):
                    if grid[r][c] != 0:
                        value = grid[r][c]
                        break
                if value != 0:
                    break

            row_data.append(value)
        output_data.append(row_data)

    return Grid(output_data)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("5783df64", solve)
