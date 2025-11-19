import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task
from collections import Counter

def solve(grid: Grid):
    '''
    Pattern:
    1. Count the number of 8s in row 0 (call it N)
    2. Find which values in row 8 appear exactly N times
    3. Create a filtered version of row 8, keeping only values that appear N times (others become 0)
    4. Fill rows (6-N) through 5 with this filtered row

    The grid structure:
    - Row 0: Contains some 8s (the count determines the pattern)
    - Rows 1-5: Will be modified based on the pattern
    - Row 6: Horizontal line of 5s (separator)
    - Row 7: Empty row (zeros)
    - Row 8: Source row with various values
    - Row 9: Empty row (zeros)
    '''
    # Convert grid to list for easier manipulation
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0
    output_data = [[grid[r][c] for c in range(width)] for r in range(height)]

    # Count 8s in row 0
    count_8s = output_data[0].count(8)

    # Analyze row 8 to find values appearing exactly count_8s times
    row8 = output_data[8]
    value_counts = Counter(row8)

    # Find values that appear exactly count_8s times
    target_values = {value for value, count in value_counts.items() if count == count_8s}

    # Create filtered row: keep only target values, others become 0
    filtered_row = [cell if cell in target_values else 0 for cell in row8]

    # Fill rows (6 - count_8s) through 5 with the filtered row
    start_row = 6 - count_8s
    for row_idx in range(start_row, 6):
        output_data[row_idx] = filtered_row.copy()

    return Grid(output_data)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("2685904e", solve)
