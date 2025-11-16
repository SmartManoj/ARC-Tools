import os
from arc_tools.grid import Grid
from arc_tools import logger
from helper import solve_task


def solve(grid: Grid):
    '''
    Pattern: "Unwinding" a shape diagonally from bottom-right to top-left.

    For each non-zero pixel at position (row, col):
    - Calculate how many rows from the bottom of the shape's bounding box
    - Shift the pixel left by that many columns
    - Pixels that would have negative column indices are clipped (removed)

    The transformation creates a diagonal "staircase" effect where:
    - The bottom row stays in place
    - Each row above shifts progressively more to the left
    '''
    # Get grid dimensions
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0

    # Find bounding box of all non-zero pixels
    min_row, max_row = None, None
    min_col, max_col = None, None

    for r in range(height):
        for c in range(width):
            if grid[r][c] != 0:
                if min_row is None:
                    min_row = r
                max_row = r
                if min_col is None or c < min_col:
                    min_col = c
                if max_col is None or c > max_col:
                    max_col = c

    # If no non-zero pixels, return original grid
    if min_row is None:
        return grid

    # Create output grid (all zeros)
    output_data = [[0 for _ in range(width)] for _ in range(height)]

    # Transform each non-zero pixel
    end_row = max_row
    for r in range(height):
        for c in range(width):
            if grid[r][c] != 0:
                # Calculate row distance from bottom of shape
                row_from_bottom = end_row - r

                # Calculate new column position (shift left)
                new_col = c - row_from_bottom

                # Only place pixel if new position is valid (non-negative column)
                if new_col >= 0:
                    output_data[r][new_col] = grid[r][c]

    return Grid(output_data)


if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("423a55dc", solve)
