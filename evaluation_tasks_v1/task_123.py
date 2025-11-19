import os
from arc_tools.grid import Grid
from helper import solve_task

def solve(grid: Grid):
    '''
    Pattern: Input contains a repeating pattern with a border region filled with a marker color.
    Output: Shifts the pattern left by 1 position and extends it to fill the entire grid.

    Algorithm:
    1. Detect border color (uniform color at edges or filling a region)
    2. Find the non-border pattern region
    3. Detect the period of the repeating pattern
    4. Shift pattern left by 1 and tile to fill output
    '''
    height = len(grid)
    width = len(grid[0])

    # Detect border color - check last row and last column
    border_color = None

    # Check if last row has uniform color
    last_row = [grid[height-1][col] for col in range(width)]
    if len(set(last_row)) == 1:
        border_color = last_row[0]

    # Check if last column has uniform color
    if border_color is None:
        last_col = [grid[row][width-1] for row in range(height)]
        if len(set(last_col)) == 1:
            border_color = last_col[0]

    # If still no border found, check for rectangular border regions
    if border_color is None:
        # Check if there's a color that fills the right edge
        for col in range(width-1, -1, -1):
            col_values = [grid[row][col] for row in range(height)]
            if len(set(col_values)) == 1:
                border_color = col_values[0]
                break

    # Find pattern dimensions (non-border region)
    pattern_width = width
    pattern_height = height

    if border_color is not None:
        # Find where border starts horizontally
        for col in range(width):
            if all(grid[row][col] == border_color for row in range(height)):
                pattern_width = col
                break

        # Find where border starts vertically
        for row in range(height):
            if all(grid[row][col] == border_color for col in range(width)):
                pattern_height = row
                break

    # Detect period in first row's pattern
    first_row_pattern = [grid[0][col] for col in range(pattern_width)]
    period = detect_period(first_row_pattern)

    # Also check for row period
    first_col_pattern = [grid[row][0] for row in range(pattern_height)]
    row_period = detect_period(first_col_pattern)

    # Create output by shifting pattern left by 1
    output_data = []
    for row in range(height):
        output_row = []
        for col in range(width):
            # Shift left by 1: output[row][col] = input[row][(col+1) % period]
            src_col = (col + 1) % period
            src_row = row % row_period
            output_row.append(grid[src_row][src_col])
        output_data.append(output_row)

    return Grid(output_data)

def detect_period(sequence):
    '''Detect the period of a repeating pattern in a sequence.'''
    n = len(sequence)
    for period in range(1, n + 1):
        # Check if sequence repeats with this period
        if all(sequence[i] == sequence[i % period] for i in range(n)):
            return period
    return n

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("50a16a69", solve)
