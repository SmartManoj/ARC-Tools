import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Find 2x2 squares of color 2 (red), identify the 4 corner colors around each square,
    and draw diagonal lines from each corner color to the opposite corner.
    '''
    import copy

    # Create a mutable copy of the grid
    output = [[grid[row][col] for col in range(grid.width)] for row in range(grid.height)]

    # Find all 2x2 squares of color 2
    squares_2x2 = []
    for row in range(grid.height - 1):
        for col in range(grid.width - 1):
            if (grid[row][col] == 2 and grid[row][col+1] == 2 and
                grid[row+1][col] == 2 and grid[row+1][col+1] == 2):
                squares_2x2.append((row, col))

    # For each 2x2 square, find corner colors and draw diagonals
    for sq_row, sq_col in squares_2x2:
        # The 2x2 square occupies rows sq_row to sq_row+1 and cols sq_col to sq_col+1
        # Find the 4 corner colors (one cell away from each corner)
        corners = {}

        # Top-left corner (one cell up and left from the square)
        if sq_row > 0 and sq_col > 0:
            color = grid[sq_row-1][sq_col-1]
            if color != 0 and color != 2:
                corners['top_left'] = (sq_row-1, sq_col-1, color)

        # Top-right corner (one cell up and right from the square)
        if sq_row > 0 and sq_col + 2 < grid.width:
            color = grid[sq_row-1][sq_col+2]
            if color != 0 and color != 2:
                corners['top_right'] = (sq_row-1, sq_col+2, color)

        # Bottom-left corner (one cell down and left from the square)
        if sq_row + 2 < grid.height and sq_col > 0:
            color = grid[sq_row+2][sq_col-1]
            if color != 0 and color != 2:
                corners['bottom_left'] = (sq_row+2, sq_col-1, color)

        # Bottom-right corner (one cell down and right from the square)
        if sq_row + 2 < grid.height and sq_col + 2 < grid.width:
            color = grid[sq_row+2][sq_col+2]
            if color != 0 and color != 2:
                corners['bottom_right'] = (sq_row+2, sq_col+2, color)

        # Draw diagonal lines extending from corners to grid edges
        # Draw \ diagonal (top-left to bottom-right direction)
        if 'top_left' in corners or 'bottom_right' in corners:
            # Get colors (use 0 if corner doesn't exist)
            tl_color = corners['top_left'][2] if 'top_left' in corners else 0
            br_color = corners['bottom_right'][2] if 'bottom_right' in corners else 0

            # Swap: top-left gets bottom-right color, bottom-right gets top-left color
            draw_diagonal_line(output, sq_row, sq_col, sq_row+1, sq_col+1,
                             -1, -1, br_color, grid)  # Extend up-left from top-left
            draw_diagonal_line(output, sq_row+1, sq_col+1, sq_row, sq_col,
                             1, 1, tl_color, grid)  # Extend down-right from bottom-right

        # Draw / diagonal (top-right to bottom-left direction)
        if 'top_right' in corners or 'bottom_left' in corners:
            tr_color = corners['top_right'][2] if 'top_right' in corners else 0
            bl_color = corners['bottom_left'][2] if 'bottom_left' in corners else 0

            # Swap: top-right gets bottom-left color, bottom-left gets top-right color
            draw_diagonal_line(output, sq_row, sq_col+1, sq_row+1, sq_col,
                             -1, 1, bl_color, grid)  # Extend up-right from top-right
            draw_diagonal_line(output, sq_row+1, sq_col, sq_row, sq_col+1,
                             1, -1, tr_color, grid)  # Extend down-left from bottom-left

    return Grid(output)

def draw_diagonal_line(output, start_row, start_col, end_row, end_col, dr, dc, color, grid):
    '''
    Draw a diagonal line in direction (dr, dc) starting from near a corner of the 2x2 square.
    '''
    if color == 0:  # Skip if no color to draw
        return

    # Start from outside the 2x2 square
    r, c = start_row + dr, start_col + dc

    # Draw until we reach the edge of the grid
    while 0 <= r < grid.height and 0 <= c < grid.width:
        if grid[r][c] != 2:  # Don't overwrite the 2x2 square
            output[r][c] = color
        r += dr
        c += dc

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("85fa5666", solve)
