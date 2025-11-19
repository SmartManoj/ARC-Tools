import os
from arc_tools.grid import Grid
from arc_tools import logger
from helper import solve_task

def solve(grid: Grid):
    '''
    Pattern Analysis:
    - For each row, find horizontal runs of non-zero (colored) pixels
    - If a colored run starts at column 0: remove the rightmost pixel from that run
    - If a colored run starts at column > 0: shift the entire run left by 1 position
    - Replace all zeros (black) with 5 (gray)

    Examples:
    - [4, 4, 4] -> [4, 4, 5] (starts at 0, rightmost pixel removed)
    - [0, 0, 3, 3, 3, 3, 0, 0] -> [5, 3, 3, 3, 3, 5, 5, 5] (starts at 2, shifted left to 1)
    - [0, 3, 3, 0, 0, 0, 0, 0] -> [3, 3, 5, 5, 5, 5, 5, 5] (starts at 1, shifted left to 0)
    '''
    height = len(grid)
    width = len(grid[0])

    # Initialize output grid filled with 5 (gray)
    output_data = [[5 for _ in range(width)] for _ in range(height)]

    # Process each row
    for row_idx in range(height):
        row = grid[row_idx]

        # Find the start and end of colored (non-zero) pixels in this row
        start = -1
        end = -1
        color = 0

        for col_idx in range(width):
            if row[col_idx] != 0:
                if start == -1:
                    start = col_idx
                    color = row[col_idx]
                end = col_idx

        # If there are colored pixels in this row
        if start != -1:
            if start == 0:
                # Run starts at column 0: keep same position but remove rightmost pixel
                for col_idx in range(start, end):  # Note: end is excluded, so we skip the last pixel
                    output_data[row_idx][col_idx] = color
            else:
                # Run starts at column > 0: shift left by 1
                new_start = start - 1
                length = end - start + 1
                for i in range(length):
                    output_data[row_idx][new_start + i] = color

    return Grid(output_data)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("32e9702f", solve)
