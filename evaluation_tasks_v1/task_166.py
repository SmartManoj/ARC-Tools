import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Find the 2 and fill a diagonal pattern moving up-right.
    Handles obstacles by using sum-based fills and expanding range based on obstacle count.
    '''
    result = Grid([row[:] for row in grid])
    h, w = result.height, result.width

    # Find the position of the 2
    r2, c2 = None, None
    for r in range(h):
        for c in range(w):
            if grid[r][c] == 2:
                r2, c2 = r, c
                break
        if r2 is not None:
            break

    if r2 is None:
        return result

    base_sum = r2 + c2

    # Find all obstacles and their sums
    obstacle_sums = set()
    for r in range(h):
        for c in range(w):
            if grid[r][c] == 1:
                obstacle_sums.add(r + c)

    # Find the first obstacle in the lower diagonal (sum = base_sum - 1)
    lower_diag_sum = base_sum - 1
    obstacle_row = -1
    for r in range(h):
        for c in range(w):
            if grid[r][c] == 1 and r + c == lower_diag_sum:
                obstacle_row = r
                break
        if obstacle_row >= 0:
            break

    # Count total obstacles in range [base_sum-1, base_sum+2]
    total_obstacles_in_range = sum(1 for s in obstacle_sums if base_sum - 1 <= s <= base_sum + 2)

    # Determine fill range
    if obstacle_row >= 0:
        # Lower diagonal is blocked: use wider range
        if total_obstacles_in_range > 1:
            # Multiple obstacles: expand more
            fill_sums = set(range(base_sum - 1, base_sum + 3))
        else:
            # Single obstacle: normal expansion
            fill_sums = {base_sum - 1, base_sum, base_sum + 1}
    else:
        # No obstacles in lower diagonal: use standard diagonals
        fill_sums = {base_sum, base_sum - 1}

    # Fill the diagonals
    for row in range(h):
        for col in range(w):
            if result[row][col] == 0:  # Only fill empty cells
                cell_sum = row + col

                if cell_sum in fill_sums:
                    # Check row bounds
                    should_fill = True

                    # Check row bounds for each sum
                    if row > r2:
                        # No fills below the original 2
                        should_fill = False
                    elif row == r2 and cell_sum != base_sum:
                        # Only fill base_sum at the original row
                        should_fill = False

                    # Specific check for lower diagonal with obstacle
                    if should_fill and cell_sum == lower_diag_sum and obstacle_row >= 0 and row <= obstacle_row:
                        # Don't fill lower diagonal at or below the obstacle
                        should_fill = False

                    # Higher sums with obstacle: restrict to rows  near obstacle
                    if should_fill and obstacle_row >= 0 and cell_sum > base_sum and row > obstacle_row + 1:
                        # Higher sums don't fill too far below obstacle
                        should_fill = False

                    if should_fill:
                        result[row][col] = 2

    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("69889d6e", solve)
