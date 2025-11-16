import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Transforms a grid split by a row of 7s into a grid where 8 appears
    at positions where both sections have 0.

    Pattern:
    1. Input has two sections separated by a row of all 7s
    2. Top section: rows with 0s and 2s (6 rows)
    3. Bottom section: rows with 0s and 6s (6 rows)
    4. For each position (i, j):
       - If both top[i][j] == 0 AND bottom[i][j] == 0: output 8
       - Otherwise: output 0
    '''
    # Find the separator row (all 7s)
    separator_idx = None
    for i in range(grid.height):
        if all(grid[i][j] == 7 for j in range(grid.width)):
            separator_idx = i
            break

    if separator_idx is None:
        raise ValueError("No separator row of 7s found")

    # Extract the two sections
    top_section = []
    for i in range(separator_idx):
        top_section.append([grid[i][j] for j in range(grid.width)])

    bottom_section = []
    for i in range(separator_idx + 1, grid.height):
        bottom_section.append([grid[i][j] for j in range(grid.width)])

    # Both sections should have the same dimensions
    if len(top_section) != len(bottom_section):
        raise ValueError("Top and bottom sections have different heights")

    # Create output: 8 where both sections have 0, otherwise 0
    output_data = []
    for i in range(len(top_section)):
        row = []
        for j in range(len(top_section[0])):
            if top_section[i][j] == 0 and bottom_section[i][j] == 0:
                row.append(8)
            else:
                row.append(0)
        output_data.append(row)

    return Grid(output_data)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("0c9aba6e", solve)
