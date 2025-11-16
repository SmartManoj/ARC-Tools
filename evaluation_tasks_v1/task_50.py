import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Pattern: Find a 3x3 colored block and transform it by:
    1. Top row: Create diagonal rays going upward (left goes up-left, middle up, right up-right)
    2. Middle row: Extend horizontally (left value fills left, middle stays, right value fills right)
    3. Bottom row: Create diagonal rays going downward (left goes down-left, middle down, right goes down-right)
    '''
    height, width = len(grid), len(grid[0])

    # Find the 3x3 non-zero block
    block_rows = set()
    block_cols = set()
    for r in range(height):
        for c in range(width):
            if grid[r][c] != 0:
                block_rows.add(r)
                block_cols.add(c)

    if len(block_rows) < 3 or len(block_cols) < 3:
        return grid

    # Get the three rows of the block
    rows = sorted(block_rows)
    top_row_idx = rows[0]
    mid_row_idx = rows[1]
    bot_row_idx = rows[2]

    # Get the three columns
    cols = sorted(block_cols)
    left_col = cols[0]
    mid_col = cols[1]
    right_col = cols[2]

    # Extract values from each row
    top_left = grid[top_row_idx][left_col]
    top_mid = grid[top_row_idx][mid_col]
    top_right = grid[top_row_idx][right_col]

    mid_left = grid[mid_row_idx][left_col]
    mid_mid = grid[mid_row_idx][mid_col]
    mid_right = grid[mid_row_idx][right_col]

    bot_left = grid[bot_row_idx][left_col]
    bot_mid = grid[bot_row_idx][mid_col]
    bot_right = grid[bot_row_idx][right_col]

    # Create output grid (copy of input)
    output = [[grid[r][c] for c in range(width)] for r in range(height)]

    # 1. Top row: Create diagonal rays going upward
    for i in range(1, top_row_idx + 1):
        row = top_row_idx - i
        # Left diagonal (up-left)
        col = left_col - i
        if 0 <= col < width:
            output[row][col] = top_left
        # Middle stays in same column
        if 0 <= row < height:
            output[row][mid_col] = top_mid
        # Right diagonal (up-right)
        col = right_col + i
        if col < width:
            output[row][col] = top_right

    # 2. Middle row: Extend horizontally
    # Left value fills to the left
    for c in range(left_col + 1):
        output[mid_row_idx][c] = mid_left
    # Right value fills to the right
    for c in range(right_col, width):
        output[mid_row_idx][c] = mid_right

    # 3. Bottom row: Create diagonal rays going downward
    for i in range(1, height - bot_row_idx):
        row = bot_row_idx + i
        # Left diagonal (down-left)
        col = left_col - i
        if 0 <= col < width:
            output[row][col] = bot_left
        # Middle stays in same column
        if row < height:
            output[row][mid_col] = bot_mid
        # Right diagonal (down-right)
        col = right_col + i
        if col < width:
            output[row][col] = bot_right

    return Grid(output)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("1d398264", solve)
