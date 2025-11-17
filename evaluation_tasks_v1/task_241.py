import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Find lines of gray (5) pixels and replicate patterns along those lines.

    For horizontal gray lines: take the vertical pattern (column values) and extend horizontally
    For vertical gray lines: take the horizontal pattern (row values) and extend vertically

    The gray line acts as both a marker and part of the region to fill.
    '''
    result = grid.copy()
    height, width = grid.shape

    # Find all vertical gray lines (columns with multiple 5s)
    vertical_gray_lines = []
    for col in range(width):
        gray_rows = [row for row in range(height) if grid[row][col] == 5]
        if len(gray_rows) > 1:
            vertical_gray_lines.append((col, gray_rows))

    # Find all horizontal gray lines (rows with multiple 5s)
    horizontal_gray_lines = []
    for row in range(height):
        gray_cols = [col for col in range(width) if grid[row][col] == 5]
        if len(gray_cols) > 1:
            horizontal_gray_lines.append((row, gray_cols))

    # For horizontal gray lines: replicate vertical patterns horizontally
    for gray_row, gray_cols in horizontal_gray_lines:
        # For each row, extend its values horizontally along the gray columns
        for row in range(height):
            # Find pattern in this row (values on the gray columns)
            pattern_col = None
            for col in gray_cols:
                if grid[row][col] != 0 and grid[row][col] != 5:
                    pattern_col = col
                    break

            if pattern_col is not None:
                # Extend this value to all gray columns
                pattern_value = grid[row][pattern_col]
                for col in gray_cols:
                    if grid[row][col] == 0 or grid[row][col] == 5:
                        result[row][col] = pattern_value

    # For vertical gray lines: replicate horizontal patterns vertically
    for gray_col, gray_rows in vertical_gray_lines:
        # Find the pattern rows (rows with multiple non-black/non-gray values adjacent to gray column)
        pattern_rows = []
        for row in gray_rows:
            pattern_count = 0
            for col in range(width):
                if col != gray_col and grid[row][col] != 0 and grid[row][col] != 5:
                    pattern_count += 1
            if pattern_count > 1:  # Row has a substantial pattern (not just 1 pixel)
                pattern_rows.append(row)

        if pattern_rows:
            # Replicate the pattern vertically
            pattern_idx = 0
            for row in gray_rows:
                for col in range(width):
                    if col != gray_col and (grid[row][col] == 0 or grid[row][col] == 5):
                        # Use the corresponding value from the pattern
                        pattern_row = pattern_rows[pattern_idx % len(pattern_rows)]
                        if grid[pattern_row][col] != 0 and grid[pattern_row][col] != 5:
                            result[row][col] = grid[pattern_row][col]
                pattern_idx += 1

    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("9c1e755f", solve)
