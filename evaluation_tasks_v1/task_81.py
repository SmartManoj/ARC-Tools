import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Transforms a 6x5 grid into a 3x5 grid by performing XOR operation
    between the top half (rows 0-2) and bottom half (rows 3-5).

    Pattern:
    - Input: 6x5 grid split into two halves
      - Top half (rows 0-2): contains colors 9 and 0
      - Bottom half (rows 3-5): contains colors 4 and 0
    - Output: 3x5 grid
      - For each position (i, j):
        - If exactly one of top[i][j] or bottom[i][j] is non-zero: output is 6
        - Otherwise (both zero or both non-zero): output is 0

    This is essentially an XOR operation on the presence of color.
    '''
    # Create output grid using XOR logic
    # Top half is rows 0-2, bottom half is rows 3-5
    output_data = []
    for i in range(3):
        row = []
        for j in range(5):
            top_val = grid[i][j]
            bottom_val = grid[i + 3][j]
            # XOR: output is 6 if exactly one is non-zero, else 0
            if (top_val != 0) != (bottom_val != 0):
                row.append(6)
            else:
                row.append(0)
        output_data.append(row)

    return Grid(output_data)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("31d5ba1a", solve)
