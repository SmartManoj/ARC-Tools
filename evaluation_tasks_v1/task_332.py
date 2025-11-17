import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Find the line of symmetry between mirrored patterns and draw a line of 3s.
    The line can be either horizontal or vertical depending on the pattern orientation.
    '''
    result = grid.copy()

    # Find the colored object(s)
    non_zero_rows = set()
    non_zero_cols = set()

    for i in range(grid.height):
        for j in range(grid.width):
            if grid[i][j] != 0:
                non_zero_rows.add(i)
                non_zero_cols.add(j)

    if not non_zero_rows or not non_zero_cols:
        return result

    # Find the gap (empty row or column) in the middle of the pattern
    min_row, max_row = min(non_zero_rows), max(non_zero_rows)
    min_col, max_col = min(non_zero_cols), max(non_zero_cols)

    # Check for horizontal symmetry (empty row in the middle)
    for row in range(min_row, max_row + 1):
        is_empty = all(grid[row][col] == 0 for col in range(grid.width))
        if is_empty:
            # Check if there are non-zero rows both above and below
            has_above = any(r < row for r in non_zero_rows)
            has_below = any(r > row for r in non_zero_rows)
            if has_above and has_below:
                # Draw horizontal line
                for col in range(grid.width):
                    result[row][col] = 3
                return result

    # Check for vertical symmetry (empty column in the middle)
    for col in range(min_col, max_col + 1):
        is_empty = all(grid[row][col] == 0 for row in range(grid.height))
        if is_empty:
            # Check if there are non-zero columns both left and right
            has_left = any(c < col for c in non_zero_cols)
            has_right = any(c > col for c in non_zero_cols)
            if has_left and has_right:
                # Draw vertical line
                for row in range(grid.height):
                    result[row][col] = 3
                return result

    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("da2b0fe3", solve)
