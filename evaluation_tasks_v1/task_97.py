import os
from arc_tools.grid import Grid
from arc_tools import logger
from helper import solve_task


def solve(grid: Grid):
    '''
    Pattern: For each cell containing value 3, create a cross/box pattern:
    - A 5-wide horizontal box centered on the 3
    - The box extends 2 rows above and 2 rows below
    - Structure:
      Row -2: [5, 5, 5, 5, 5]
      Row -1: [2, 0, 5, 0, 2]
      Row  0: [2, 0, 3, 0, 2] (the 3 itself)
      Row +1: [2, 0, 0, 0, 2]
      Row +2: Full horizontal line of 2s with [8, 8, 8, 8, 8] in the box area
    '''
    # Create output grid as a copy of input
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0
    output_data = [[grid[r][c] for c in range(width)] for r in range(height)]

    # Find all cells with value 3
    threes = []
    for r in range(height):
        for c in range(width):
            if grid[r][c] == 3:
                threes.append((r, c))

    # For each 3, create the pattern
    for r, c in threes:
        # Calculate the 5-wide box boundaries (2 cells left and right of center)
        c_start = c - 2
        c_end = c + 2

        # Row -2: horizontal line of 5s
        if r - 2 >= 0:
            for col in range(max(0, c_start), min(width, c_end + 1)):
                output_data[r - 2][col] = 5

        # Row -1: [2, 0, 5, 0, 2]
        if r - 1 >= 0:
            for offset, value in [(-2, 2), (-1, 0), (0, 5), (1, 0), (2, 2)]:
                col = c + offset
                if 0 <= col < width:
                    output_data[r - 1][col] = value

        # Row 0: [2, 0, 3, 0, 2] (the 3 itself)
        for offset, value in [(-2, 2), (-1, 0), (0, 3), (1, 0), (2, 2)]:
            col = c + offset
            if 0 <= col < width:
                output_data[r][col] = value

        # Row +1: [2, 0, 0, 0, 2]
        if r + 1 < height:
            for offset, value in [(-2, 2), (-1, 0), (0, 0), (1, 0), (2, 2)]:
                col = c + offset
                if 0 <= col < width:
                    output_data[r + 1][col] = value

        # Row +2: Full horizontal line of 2s, with 8s in the box area
        if r + 2 < height:
            # Fill entire row with 2s
            for col in range(width):
                output_data[r + 2][col] = 2
            # Fill the 5-wide box area with 8s
            for col in range(max(0, c_start), min(width, c_end + 1)):
                output_data[r + 2][col] = 8

    return Grid(output_data)


if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("3f23242b", solve)
