import os
from arc_tools.grid import Grid
from helper import solve_task

def solve(grid: Grid):
    '''
    The input is a 12x6 grid divided into 4 sections of 3x6 each:
    - Rows 0-2: Color 5 pattern
    - Rows 3-5: Color 4 pattern
    - Rows 6-8: Color 2 pattern
    - Rows 9-11: Color 8 pattern

    The output is a 3x6 grid where each cell is determined by overlaying
    the 4 sections with priority: 5 > 4 > 8 > 2 > 0

    For each position (r, c) in the output, we check all 4 sections at that position
    and select the value with the highest priority.
    '''
    height = len(grid)
    width = len(grid[0])

    # The output should be 3x6
    output_height = height // 4
    output_width = width

    output_data = []

    # Priority order for colors: 5 > 4 > 8 > 2 > 0
    priority = {5: 5, 4: 4, 8: 3, 2: 2, 0: 0}

    for r in range(output_height):
        row = []
        for c in range(output_width):
            # Get values from all 4 sections
            values = [
                (grid[r][c], priority.get(grid[r][c], 0)),           # Section 5 (rows 0-2)
                (grid[r + 3][c], priority.get(grid[r + 3][c], 0)),   # Section 4 (rows 3-5)
                (grid[r + 6][c], priority.get(grid[r + 6][c], 0)),   # Section 2 (rows 6-8)
                (grid[r + 9][c], priority.get(grid[r + 9][c], 0))    # Section 8 (rows 9-11)
            ]
            # Pick the value with the highest priority
            best_value = max(values, key=lambda x: x[1])[0]
            row.append(best_value)
        output_data.append(row)

    return Grid(output_data)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("3d31c5b3", solve)
