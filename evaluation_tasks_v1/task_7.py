import os
from arc_tools.grid import Grid
from helper import solve_task

def solve(grid: Grid):
    '''
    Pattern Analysis for task 0692e18c:
    - Input is a 3x3 grid, output is a 9x9 grid
    - For each cell (r, c) with non-zero value v in the input:
      - Create a 3x3 pattern that is the "inverse" of the input:
        * Where input has value v, the pattern has 0
        * Where input has value != v (including 0), the pattern has v
      - Place this 3x3 pattern in the output at position [3*r:3*r+3, 3*c:3*c+3]

    Example: If input is:
    [0, 7, 0]
    [7, 7, 7]
    [0, 7, 0]

    For cell (0,1) with value 7, the pattern becomes:
    [7, 0, 7]  (positions with 7 in input become 0, positions with 0 become 7)
    [0, 0, 0]
    [7, 0, 7]

    This pattern is placed at output[0:3, 3:6]
    '''
    height = grid.height
    width = grid.width

    # Create output grid (3x larger in each dimension)
    output_data = [[0 for _ in range(width * 3)] for _ in range(height * 3)]

    # Process each cell in the input
    for r in range(height):
        for c in range(width):
            value = grid[r][c]

            # Only process non-zero cells
            if value != 0:
                # Create the inverse pattern for this value
                # For each position in the input grid
                for i in range(height):
                    for j in range(width):
                        # Calculate output position
                        out_r = 3 * r + i
                        out_c = 3 * c + j

                        # If input position has the same value, output gets 0
                        # If input position has different value, output gets the value
                        if grid[i][j] == value:
                            output_data[out_r][out_c] = 0
                        else:
                            output_data[out_r][out_c] = value

    return Grid(output_data)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("0692e18c", solve)
