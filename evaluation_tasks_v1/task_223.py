import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Overlay patterns from right half onto templates in left half.
    The grid is split vertically in half. Sections are separated by rows of all 5s.
    For each section, the left half is a template (5s and 0s), and the right half
    has a colored pattern. The output overlays the pattern onto the template,
    replacing 0s with colored values, and compresses by removing separator rows.
    '''
    import numpy as np

    height, width = grid.shape
    mid_col = width // 2

    # Split into left and right halves
    left_half = grid.data[:, :mid_col]
    right_half = grid.data[:, mid_col:]

    # Find separator rows (all 5s in the left half)
    separators = []
    for row in range(height):
        if np.all(left_half[row] == 5) and np.all(right_half[row] == 0):
            separators.append(row)

    # Process sections between separators
    result_rows = []

    for i in range(len(separators) - 1):
        start_row = separators[i] + 1
        end_row = separators[i + 1]

        # Process each row in this section
        for row in range(start_row, end_row):
            output_row = []
            for col in range(mid_col):
                if left_half[row, col] == 0:
                    # Replace 0 with the pattern value from right half
                    output_row.append(right_half[row, col])
                else:
                    # Keep the value from left half (usually 5)
                    output_row.append(left_half[row, col])
            result_rows.append(output_row)

    # Create result grid
    if len(result_rows) > 0:
        result = Grid(result_rows)
        return result
    else:
        return grid

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("93b4f4b3", solve)
