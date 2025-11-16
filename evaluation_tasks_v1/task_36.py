import os
from arc_tools.grid import Grid
from arc_tools import logger
from helper import solve_task

def solve(grid: Grid):
    '''
    Pattern: The last row contains markers (value 5) indicating which columns to fill.
    For each marked column:
    1. Extract all non-zero values and their row positions
    2. Identify unique values in order of last appearance
    3. Fill the column by partitioning it into segments:
       - Each value fills from after the previous value's last row to its own last row
       - The first value extends upward from row 0
    '''
    height = len(grid)
    width = len(grid[0])

    # Copy the input grid
    output_data = [list(row) for row in grid]

    # Find the last row (contains markers with value 5)
    last_row = grid[height - 1]

    # Identify columns to process (those with value 5 in last row)
    marked_columns = [col for col in range(width) if last_row[col] == 5]

    # Process each marked column
    for col in marked_columns:
        # Extract all non-zero values and their row positions
        non_zero_values = []
        for row in range(height):
            value = grid[row][col]
            if value != 0:
                non_zero_values.append((row, value))

        if not non_zero_values:
            continue

        # Get unique values in order, tracking their last occurrence
        value_segments = []  # List of (value, last_row)
        seen_values = {}

        for row, value in non_zero_values:
            seen_values[value] = row  # Update to last occurrence

        # Create ordered list of unique values with their last row
        for row, value in non_zero_values:
            if not value_segments or value_segments[-1][0] != value:
                # New value or different from previous
                if value in seen_values:
                    # Only add if we haven't already added this value
                    already_added = any(v == value for v, _ in value_segments)
                    if not already_added:
                        value_segments.append((value, seen_values[value]))

        # Fill the column based on segments
        start_row = 0
        for value, last_row in value_segments:
            for row in range(start_row, last_row + 1):
                output_data[row][col] = value
            start_row = last_row + 1

    return Grid(output_data)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("17b80ad2", solve)
