import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Connect all red (2) dots with green (3) lines using a tree structure.
    Find a backbone (horizontal or vertical line) and connect all red dots to it.
    '''
    result = grid.copy()

    # Find all red (2) cells
    red_cells = []
    for r in range(grid.height):
        for c in range(grid.width):
            if grid[r, c] == Color.RED:
                red_cells.append((r, c))

    if len(red_cells) < 2:
        return result

    # Determine if backbone should be horizontal or vertical
    # and at which row/column
    rows = [r for r, c in red_cells]
    cols = [c for r, c in red_cells]

    # Try to find a row or column that minimizes total connection length
    # Use median as a good heuristic
    median_row = sorted(rows)[len(rows) // 2]
    median_col = sorted(cols)[len(cols) // 2]

    # Calculate total distance for horizontal backbone (at median_row)
    h_distance = sum(abs(r - median_row) for r, c in red_cells)
    # Calculate total distance for vertical backbone (at median_col)
    v_distance = sum(abs(c - median_col) for r, c in red_cells)

    if v_distance <= h_distance:
        # Use vertical backbone at median_col
        backbone_col = median_col

        # Connect each red dot to the backbone
        for r, c in red_cells:
            if c < backbone_col:
                # Draw horizontal line from c to backbone_col
                for cc in range(c + 1, backbone_col):
                    result[r, cc] = Color.GREEN
            elif c > backbone_col:
                # Draw horizontal line from backbone_col to c
                for cc in range(backbone_col + 1, c):
                    result[r, cc] = Color.GREEN

        # Draw the vertical backbone
        min_r = min(rows)
        max_r = max(rows)
        for r in range(min_r, max_r + 1):
            if result[r, backbone_col] == Color.BLACK:
                result[r, backbone_col] = Color.GREEN
    else:
        # Use horizontal backbone at median_row
        backbone_row = median_row

        # Connect each red dot to the backbone
        for r, c in red_cells:
            if r < backbone_row:
                # Draw vertical line from r to backbone_row
                for rr in range(r + 1, backbone_row):
                    result[rr, c] = Color.GREEN
            elif r > backbone_row:
                # Draw vertical line from backbone_row to r
                for rr in range(backbone_row + 1, r):
                    result[rr, c] = Color.GREEN

        # Draw the horizontal backbone
        min_c = min(cols)
        max_c = max(cols)
        for c in range(min_c, max_c + 1):
            if result[backbone_row, c] == Color.BLACK:
                result[backbone_row, c] = Color.GREEN

    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("bf89d739", solve)
