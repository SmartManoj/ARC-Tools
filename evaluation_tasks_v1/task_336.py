import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task


def solve(grid: Grid):
    '''
    Transformation pattern:
    1. Find the vertical line of 5s (separator line)
    2. Calculate new position: new_col = 2 * old_col - min_1_col + 1
       where min_1_col is the leftmost column containing a 1
    3. Move the 5-line to the new position
    4. Convert all 2s between old and new positions to 1s
    5. Keep everything else in place
    '''
    height, width = grid.height, grid.width

    # Find the column with the vertical line of 5s
    old_5_col = None
    for col in range(width):
        if all(grid[row][col] == 5 for row in range(height)):
            old_5_col = col
            break

    if old_5_col is None:
        logger.error("Could not find vertical line of 5s")
        return grid

    # Find the leftmost column containing a 1 (blue)
    min_1_col = width  # Start with max value
    for row in range(height):
        for col in range(width):
            if grid[row][col] == 1:
                min_1_col = min(min_1_col, col)

    # If no 1s found, default to 0
    if min_1_col == width:
        min_1_col = 0

    # Calculate new position for the 5-line
    new_5_col = 2 * old_5_col - min_1_col + 1

    logger.info(f"Moving 5-line from column {old_5_col} to column {new_5_col}")
    logger.info(f"2s between columns {old_5_col} and {new_5_col} will become 1s")

    # Create output grid - initialize with zeros
    output = Grid([[0 for _ in range(width)] for _ in range(height)])

    # Copy all cells
    for row in range(height):
        for col in range(width):
            cell_value = grid[row][col]

            # Clear the old 5-column
            if col == old_5_col:
                output[row][col] = 0
            # Place the new 5-column
            elif col == new_5_col:
                output[row][col] = 5
            # Convert 2s between old and new positions to 1s
            elif cell_value == 2 and old_5_col < col < new_5_col:
                output[row][col] = 1
                logger.debug(f"Converting 2 to 1 at ({row}, {col})")
            # Keep everything else as is
            else:
                output[row][col] = cell_value

    return output


if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("dd2401ed", solve)
