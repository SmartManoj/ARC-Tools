import os
from arc_tools.grid import Grid
from helper import solve_task

def solve(grid: Grid):
    '''
    Transforms a 3x3 grid into a 3x12 grid by:
    1. For each row, reverse it and concatenate with the original
    2. Repeat this 6-element pattern twice to get 12 elements

    Example: [7, 5, 7] -> reversed: [7, 5, 7] -> concat: [7, 5, 7, 7, 5, 7] -> repeat: [7, 5, 7, 7, 5, 7, 7, 5, 7, 7, 5, 7]
    '''
    output_data = []

    for row in grid:
        # Convert row to list
        row_list = list(row)
        # Reverse + Original, repeated twice
        transformed_row = (row_list[::-1] + row_list) * 2
        output_data.append(transformed_row)

    return Grid(output_data)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("59341089", solve)
