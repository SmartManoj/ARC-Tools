import os
from arc_tools.grid import Grid
from arc_tools import logger
from helper import solve_task

def solve(grid: Grid):
    '''
    Pattern: Grid contains a 2x2 corner with distinct colors and a data region.
    The corner can be in any corner of the grid (surrounded by 8s).
    The data region contains 0s and a target value (non-0, non-8).

    Replace each occurrence of the target value at position (row, col) with:
    corner[row // (height//2)][col // (width//2)]

    This divides the grid into quadrants and uses the corresponding corner color.
    '''
    height = grid.height
    width = grid.width

    # Find the 2x2 corner by looking for a region without 8s or 0s
    corner = None
    corner_row_start = None
    corner_col_start = None

    # Check all four corners
    # Top-left
    if grid[0][0] not in [0, 8] and grid[0][1] not in [0, 8] and \
       grid[1][0] not in [0, 8] and grid[1][1] not in [0, 8]:
        corner = [[grid[0][0], grid[0][1]], [grid[1][0], grid[1][1]]]
        corner_row_start, corner_col_start = 0, 0
    # Top-right
    elif grid[0][width-2] not in [0, 8] and grid[0][width-1] not in [0, 8] and \
         grid[1][width-2] not in [0, 8] and grid[1][width-1] not in [0, 8]:
        corner = [[grid[0][width-2], grid[0][width-1]], [grid[1][width-2], grid[1][width-1]]]
        corner_row_start, corner_col_start = 0, width-2
    # Bottom-left
    elif grid[height-2][0] not in [0, 8] and grid[height-2][1] not in [0, 8] and \
         grid[height-1][0] not in [0, 8] and grid[height-1][1] not in [0, 8]:
        corner = [[grid[height-2][0], grid[height-2][1]], [grid[height-1][0], grid[height-1][1]]]
        corner_row_start, corner_col_start = height-2, 0
    # Bottom-right
    elif grid[height-2][width-2] not in [0, 8] and grid[height-2][width-1] not in [0, 8] and \
         grid[height-1][width-2] not in [0, 8] and grid[height-1][width-1] not in [0, 8]:
        corner = [[grid[height-2][width-2], grid[height-2][width-1]],
                  [grid[height-1][width-2], grid[height-1][width-1]]]
        corner_row_start, corner_col_start = height-2, width-2

    if corner is None:
        logger.info("Could not find corner")
        return grid

    logger.info(f"Found corner at ({corner_row_start}, {corner_col_start}): {corner}")

    # Find the target value (non-0, non-8 value in the data region)
    target_value = None
    for row in range(height):
        for col in range(width):
            val = grid[row][col]
            if val not in [0, 8] and (row < corner_row_start or row > corner_row_start + 1 or
                                       col < corner_col_start or col > corner_col_start + 1):
                target_value = val
                break
        if target_value is not None:
            break

    if target_value is None:
        logger.info("Could not find target value")
        return grid

    logger.info(f"Target value to replace: {target_value}")

    # Find the data region boundaries (non-8, non-corner cells)
    data_rows = []
    data_cols = []
    for row in range(height):
        for col in range(width):
            # Skip corner cells and border (8s)
            if (corner_row_start <= row <= corner_row_start + 1 and
                corner_col_start <= col <= corner_col_start + 1):
                continue
            if grid[row][col] != 8:
                if row not in data_rows:
                    data_rows.append(row)
                if col not in data_cols:
                    data_cols.append(col)

    data_row_start = min(data_rows)
    data_row_end = max(data_rows)
    data_col_start = min(data_cols)
    data_col_end = max(data_cols)

    data_height = data_row_end - data_row_start + 1
    data_width = data_col_end - data_col_start + 1

    logger.info(f"Data region: rows {data_row_start}-{data_row_end}, cols {data_col_start}-{data_col_end}")
    logger.info(f"Data dimensions: {data_height} x {data_width}")

    # Create output grid
    output_data = [[grid[row][col] for col in range(width)] for row in range(height)]

    # Replace target values with corner values based on position in data region
    half_data_height = data_height // 2
    half_data_width = data_width // 2

    for row in range(height):
        for col in range(width):
            # Skip corner cells themselves
            if corner_row_start <= row <= corner_row_start + 1 and \
               corner_col_start <= col <= corner_col_start + 1:
                continue

            if grid[row][col] == target_value:
                # Calculate position relative to data region start
                data_row_offset = row - data_row_start
                data_col_offset = col - data_col_start

                # Map to corner quadrant
                corner_row = data_row_offset // half_data_height
                corner_col = data_col_offset // half_data_width

                # Ensure we stay within corner bounds (0 or 1)
                corner_row = min(corner_row, 1)
                corner_col = min(corner_col, 1)

                output_data[row][col] = corner[corner_row][corner_col]

    return Grid(output_data)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("58743b76", solve)
