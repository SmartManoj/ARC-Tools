import os
from arc_tools.grid import Grid
from arc_tools import logger
from helper import solve_task

def solve(grid: Grid):
    '''
    The input is a 5x9 grid divided by a vertical line (column 4 with value 4).
    - Left section: columns 0-3
    - Right section: columns 5-8

    The output is a 5x4 grid where each cell is:
    - 2 if exactly one of (left, right) is non-zero (XOR logic)
    - 0 if both are zero or both are non-zero

    This performs a logical XOR on the "non-zero" state of corresponding cells
    from the left and right sections.
    '''
    output_data = []

    for i in range(len(grid)):
        row = []
        for j in range(4):
            left_val = grid[i][j]
            right_val = grid[i][j + 5]  # Skip column 4 (the divider)

            # XOR: output 2 if exactly one is non-zero
            left_nonzero = left_val != 0
            right_nonzero = right_val != 0

            if left_nonzero != right_nonzero:
                row.append(2)
            else:
                row.append(0)

        output_data.append(row)

    return Grid(output_data)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("34b99a2b", solve)
