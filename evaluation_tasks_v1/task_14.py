import os
from arc_tools.grid import Grid
from helper import solve_task

def solve(grid: Grid):
    '''
    Pattern: Extrapolate diagonal sequence
    1. Find all 1s on the diagonal (where row == col)
    2. Calculate the step size between consecutive 1s
    3. Continue the pattern with 2s using the same step size
    '''
    # Create output grid as a copy of input
    output = grid.copy()

    # Find all positions with value 1 on the diagonal
    ones_positions = []
    for row in range(grid.height):
        for col in range(grid.width):
            if grid[row][col] == 1:
                ones_positions.append((row, col))

    # Sort positions by row (should already be sorted, but to be safe)
    ones_positions.sort()

    # Calculate the step size
    if len(ones_positions) >= 2:
        # Calculate step from first two positions
        step = ones_positions[1][0] - ones_positions[0][0]

        # Get the last position with a 1
        last_row, last_col = ones_positions[-1]

        # Continue the pattern with 2s
        next_row = last_row + step
        next_col = last_col + step

        while next_row < grid.height and next_col < grid.width:
            output[next_row][next_col] = 2
            next_row += step
            next_col += step

    return output

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("0b17323b", solve)
