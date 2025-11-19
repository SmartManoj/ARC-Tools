import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Pattern: Yellow (4) cells form lines that act as axes of reflection.
    The transformation creates perfect symmetry across these axes by mirroring values.

    For horizontal yellow lines: reflect vertically (mirror rows)
    For vertical yellow lines: reflect horizontally (mirror columns)
    '''

    # Create output grid as a copy of input
    output_data = [[cell for cell in row] for row in grid]
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0

    # Track which rows have horizontal yellow axes
    horizontal_axes = set()
    for r in range(height):
        yellow_count = sum(1 for c in range(width) if grid[r][c] == 4)
        if yellow_count >= 3:
            horizontal_axes.add(r)

    # Find horizontal lines of 4s (potential horizontal axes)
    for r in horizontal_axes:
        # Determine the shape's color (non-0, non-4 color near the axis)
        shape_color = None
        for dr in [-1, -2, -3, 1, 2, 3]:
            check_r = r + dr
            if 0 <= check_r < height:
                for c in range(width):
                    if grid[check_r][c] not in [0, 4]:
                        shape_color = grid[check_r][c]
                        break
                if shape_color:
                    break

        # Determine the column range for this shape by looking only at cells matching the shape color or axis
        min_col = width
        max_col = -1
        for test_r in range(max(0, r-10), min(height, r+11)):
            for c in range(width):
                val = grid[test_r][c]
                # Only include if it's the shape color, OR it's a 4 on the axis row
                if val == shape_color or (val == 4 and test_r == r):
                    min_col = min(min_col, c)
                    max_col = max(max_col, c)

        # Determine which side has more content (for deciding mirror direction)
        above_count = sum(
            1 for test_r in range(max(0, r-8), r)
            for c in range(min_col, max_col + 1)
            if grid[test_r][c] == shape_color
        )
        below_count = sum(
            1 for test_r in range(r+1, min(height, r+9))
            for c in range(min_col, max_col + 1)
            if grid[test_r][c] == shape_color
        )

        # Mirror rows to create symmetry
        for distance in range(1, 10):
            row_above = r - distance
            row_below = r + distance

            if 0 <= row_above < height and 0 <= row_below < height:
                # Mirror within the column range
                for c in range(min_col, max_col + 1):
                    val_above = grid[row_above][c]
                    val_below = grid[row_below][c]

                    # Create symmetry based on which side has more content overall
                    if above_count >= below_count:
                        # Above is fuller or equal, prefer above
                        output_data[row_below][c] = val_above
                    else:
                        # Below is fuller, prefer below
                        output_data[row_above][c] = val_below

    # Track which columns have vertical yellow axes
    vertical_axes = set()
    for c in range(width):
        yellow_count = sum(1 for r in range(height) if grid[r][c] == 4)
        if yellow_count >= 3:
            vertical_axes.add(c)

    # Find vertical lines of 4s (potential vertical axes)
    for c in vertical_axes:
        # Determine the shape's color (non-0, non-4 color near the axis)
        shape_color = None
        for dc in [-1, -2, -3, 1, 2, 3]:
            check_c = c + dc
            if 0 <= check_c < width:
                for r in range(height):
                    if output_data[r][check_c] not in [0, 4]:
                        shape_color = output_data[r][check_c]
                        break
                if shape_color:
                    break

        # Determine the row range: start with rows that have 4s in the axis column
        min_row = height
        max_row = -1
        for r in range(height):
            if output_data[r][c] == 4:
                min_row = min(min_row, r)
                max_row = max(max_row, r)

        # Extend to include continuous rows with sufficient shape color nearby
        # Expand upwards
        for r in range(min_row - 1, -1, -1):
            shape_count = sum(
                1 for test_c in range(max(0, c-5), min(width, c+6))
                if output_data[r][test_c] == shape_color
            )
            # Require at least 2 cells of the shape color to include this row
            if shape_count >= 2:
                min_row = r
            else:
                break

        # Expand downwards
        for r in range(max_row + 1, height):
            shape_count = sum(
                1 for test_c in range(max(0, c-5), min(width, c+6))
                if output_data[r][test_c] == shape_color
            )
            # Require at least 2 cells of the shape color to include this row
            if shape_count >= 2:
                max_row = r
            else:
                break

        # Determine which side has more content (for deciding mirror direction)
        left_count = sum(
            1 for r in range(min_row, max_row + 1)
            for test_c in range(max(0, c-8), c)
            if output_data[r][test_c] == shape_color
        )
        right_count = sum(
            1 for r in range(min_row, max_row + 1)
            for test_c in range(c+1, min(width, c+9))
            if output_data[r][test_c] == shape_color
        )

        # Mirror columns to create symmetry
        for distance in range(1, 10):
            col_left = c - distance
            col_right = c + distance

            if 0 <= col_left < width and 0 <= col_right < width:
                # Mirror within the row range
                for r in range(min_row, max_row + 1):
                    val_left = output_data[r][col_left]
                    val_right = output_data[r][col_right]

                    # Avoid copying 4s from horizontal axes
                    if val_left == 4 and r in horizontal_axes:
                        val_left = 0
                    if val_right == 4 and r in horizontal_axes:
                        val_right = 0

                    # Create symmetry based on which side has more content overall
                    if left_count >= right_count:
                        # Left side is fuller or equal, prefer left
                        output_data[r][col_right] = val_left
                    else:
                        # Right side is fuller, prefer right
                        output_data[r][col_left] = val_right

    return Grid(output_data)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("5b692c0f", solve)
