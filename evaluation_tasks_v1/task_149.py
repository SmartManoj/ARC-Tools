import os
from arc_tools.grid import Grid
from helper import solve_task

def solve(grid: Grid):
    '''
    Upscales the grid by 2x - each cell becomes a 2x2 block of the same value.

    Pattern:
    - Each input cell at position (r, c) with value v
    - Becomes a 2x2 block in the output at positions:
      (2*r, 2*c), (2*r, 2*c+1), (2*r+1, 2*c), (2*r+1, 2*c+1)
    - All with value v

    If input is H x W, output is (2*H) x (2*W)
    '''
    height = len(grid)
    width = len(grid[0])

    # Create output grid with doubled dimensions
    output_data = []

    for r in range(height):
        # Each row in input becomes 2 rows in output
        row1 = []
        row2 = []
        for c in range(width):
            value = grid[r][c]
            # Each cell becomes 2 cells horizontally
            row1.extend([value, value])
            row2.extend([value, value])

        # Add both rows (vertical duplication)
        output_data.append(row1)
        output_data.append(row2)

    return Grid(output_data)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("60c09cac", solve)
