import os
from arc_tools.grid import Grid
from helper import solve_task

def solve(grid: Grid):
    '''
    Replaces 0s in the grid with colors based on column position.

    Pattern:
    1. Find all columns that contain at least one 0
    2. Sort these columns by their index (left to right)
    3. Assign sequential colors (1, 2, 3, 4, ...) to each column
    4. Replace all 0s in each column with that column's assigned color
    '''
    # Find all columns that contain at least one 0
    columns_with_zeros = set()
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == 0:
                columns_with_zeros.add(col)

    # Sort columns and assign colors (1-indexed)
    sorted_columns = sorted(columns_with_zeros)
    column_to_color = {col: idx + 1 for idx, col in enumerate(sorted_columns)}

    # Create output grid by replacing 0s with their column's color
    output_data = []
    for row in range(len(grid)):
        new_row = []
        for col in range(len(grid[0])):
            if grid[row][col] == 0:
                new_row.append(column_to_color[col])
            else:
                new_row.append(grid[row][col])
        output_data.append(new_row)

    return Grid(output_data)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("575b1a71", solve)
