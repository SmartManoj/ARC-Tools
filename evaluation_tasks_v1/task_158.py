import os
from arc_tools.grid import Grid
from arc_tools import logger
from helper import solve_task


def solve(grid: Grid):
    '''
    Split input grid into two halves (left: columns 0-6, right: columns 7-13).
    Output 5 where both halves are 0 at the same position, otherwise 0.
    '''
    h, w = grid.height, grid.width

    # The input width should be 14 (two halves of 7 each)
    # Output width should be 7
    output_width = w // 2
    result = Grid([[0] * output_width for _ in range(h)])

    # Process each position
    for i in range(h):
        for j in range(output_width):
            left_val = grid[i][j]
            right_val = grid[i][j + output_width]

            # Output 5 where both halves are 0, otherwise 0
            if left_val == 0 and right_val == 0:
                result[i][j] = 5
            else:
                result[i][j] = 0

    return result


if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("66f2d22f", solve)
