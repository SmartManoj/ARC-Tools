import os
from arc_tools.grid import Grid
from arc_tools import logger
from helper import solve_task

def solve(grid: Grid):
    '''
    Transforms a 3x3 grid into a 6x6 grid by expanding each cell into a 2x2 block:
    - Cell with value 5 → [[1, 2], [2, 1]]
    - Cell with value 0 → [[0, 0], [0, 0]]

    Each input cell at position (i, j) maps to output positions (2*i:2*i+2, 2*j:2*j+2)
    '''
    # Create 6x6 output grid
    output_data = [[0 for _ in range(6)] for _ in range(6)]

    # Process each cell in the 3x3 input
    for i in range(3):
        for j in range(3):
            value = grid[i][j]

            # Calculate output position (top-left of 2x2 block)
            out_i = i * 2
            out_j = j * 2

            if value == 5:
                # Replace with [[1, 2], [2, 1]] pattern
                output_data[out_i][out_j] = 1
                output_data[out_i][out_j + 1] = 2
                output_data[out_i + 1][out_j] = 2
                output_data[out_i + 1][out_j + 1] = 1
            # else value == 0, already initialized to 0

    return Grid(output_data)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("2072aba6", solve)
