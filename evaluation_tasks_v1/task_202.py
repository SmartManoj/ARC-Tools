import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Repair a tiled pattern by finding the most common value for each position.
    The pattern repeats every 2 rows. For each (row mod 2, column) position,
    find the most common value across all such positions.
    '''
    from collections import Counter

    # Row pattern repeats every 2 rows
    row_period = 2

    # For each (row_position, column) pair, collect all values
    position_values = {}
    for row in range(grid.height):
        for col in range(grid.width):
            row_pos = row % row_period
            key = (row_pos, col)
            if key not in position_values:
                position_values[key] = []
            position_values[key].append(grid[row][col])

    # Find the most common value for each position
    most_common = {}
    for key, values in position_values.items():
        counter = Counter(values)
        most_common[key] = counter.most_common(1)[0][0]

    # Create output grid
    output = []
    for row in range(grid.height):
        output_row = []
        for col in range(grid.width):
            row_pos = row % row_period
            key = (row_pos, col)
            output_row.append(most_common[key])
        output.append(output_row)

    return Grid(output)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("85b81ff1", solve)
