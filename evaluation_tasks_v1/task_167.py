import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Combine three 5x5 layers stacked vertically (15x5 input) into a single 5x5 output.
    The input grid has three layers:
    - Rows 0-4: Layer 1 (contains 1s and 0s)
    - Rows 5-9: Layer 2 (contains 8s and 0s)
    - Rows 10-14: Layer 3 (contains 6s and 0s)

    Priority rule for each output cell: layer3 > layer1 > layer2
    If layer3[i][j] != 0, output[i][j] = layer3[i][j]
    Else if layer1[i][j] != 0, output[i][j] = layer1[i][j]
    Else if layer2[i][j] != 0, output[i][j] = layer2[i][j]
    Else output[i][j] = 0
    '''
    # Extract the three layers
    layer1 = [row[:] for row in grid[0:5]]     # rows 0-4
    layer2 = [row[:] for row in grid[5:10]]    # rows 5-9
    layer3 = [row[:] for row in grid[10:15]]   # rows 10-14

    # Create output grid
    result = Grid([[0] * 5 for _ in range(5)])

    # Apply priority rule
    for i in range(5):
        for j in range(5):
            if layer3[i][j] != 0:
                result[i][j] = layer3[i][j]
            elif layer1[i][j] != 0:
                result[i][j] = layer1[i][j]
            elif layer2[i][j] != 0:
                result[i][j] = layer2[i][j]
            else:
                result[i][j] = 0

    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("6a11f6da", solve)
