import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Expand each row by filling zeros with a symmetric pattern.

    Pattern: Each row has non-zero values followed by zeros.
    Transformation: pattern + [outer_value] * n + pattern[1:]
    where outer_value is the first/last element of the pattern,
    and n = row_length - 2*pattern_length + 1
    '''
    result_data = []

    for row_idx in range(grid.height):
        row = grid[row_idx]

        # Find the pattern (non-zero prefix)
        pattern = []
        for val in row:
            if val != 0:
                pattern.append(val)
            else:
                break

        pattern_length = len(pattern)
        row_length = len(row)

        # Calculate the number of middle fills
        middle_count = row_length - 2 * pattern_length + 1

        # Build the output row
        outer_value = pattern[0]
        output_row = pattern + [outer_value] * middle_count + pattern[1:]

        result_data.append(output_row)

    return Grid(result_data)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("62b74c02", solve)
