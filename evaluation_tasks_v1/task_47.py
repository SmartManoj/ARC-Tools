import os
from arc_tools.grid import Grid
from arc_tools import logger
from helper import solve_task

def solve(grid: Grid):
    '''
    Identifies "missing pieces" in 3x3 blocks within a grid.

    Pattern:
    - The grid contains 3x3 blocks of cells containing value 8
    - Blocks are separated by rows/columns of 0s at regular intervals (0, 4, 8, 12, ...)
    - Blocks are located at positions: rows/cols 1-3, 5-7, 9-11, etc.
    - For each 3x3 block, the output marks (with value 2) the cells that are 0 in the input
    - This effectively shows which cells would need to be filled to complete each 3x3 block

    Transformation:
    - For each cell in a 3x3 block:
      - If input[i][j] == 0 (missing), output[i][j] = 2
      - If input[i][j] == 8 (filled), output[i][j] = 0
    - All other cells (borders/separators) remain 0
    '''
    # Initialize output grid with all 0s
    output_data = [[0 for _ in range(grid.width)] for _ in range(grid.height)]

    # 3x3 blocks start at positions: 1, 5, 9, 13, ... (i.e., 1 + 4*n)
    # Separators are at positions: 0, 4, 8, 12, ... (i.e., 4*n)

    block_row_starts = list(range(1, grid.height, 4))
    block_col_starts = list(range(1, grid.width, 4))

    for block_row_start in block_row_starts:
        # Check if we have room for a full 3x3 block
        if block_row_start + 2 >= grid.height:
            continue

        for block_col_start in block_col_starts:
            # Check if we have room for a full 3x3 block
            if block_col_start + 2 >= grid.width:
                continue

            # Process each cell in this 3x3 block
            for r in range(3):
                for c in range(3):
                    row = block_row_start + r
                    col = block_col_start + c

                    # If the cell is 0 in input, it's "missing" from the complete block
                    # Mark it with 2 in the output
                    if grid[row][col] == 0:
                        output_data[row][col] = 2

    return Grid(output_data)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("1c0d0a4b", solve)
