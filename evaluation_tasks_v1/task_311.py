import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Find two pixels with value 8 and connect them with green (3) lines.
    If row distance is small (<=2), draw a rectangle. Otherwise, draw a bowtie pattern.
    '''
    result = grid.copy()

    # Find all pixels with value 8
    positions_8 = []
    for r in range(grid.height):
        for c in range(grid.width):
            if grid[r][c] == 8:
                positions_8.append((r, c))

    if len(positions_8) != 2:
        return result

    (r1, c1), (r2, c2) = positions_8
    row_dist = abs(r2 - r1)
    col_dist = abs(c2 - c1)

    if row_dist <= 2:
        # Draw a rectangle
        min_r, max_r = min(r1, r2), max(r1, r2)
        min_c, max_c = min(c1, c2), max(c1, c2)

        # Draw horizontal lines on rows of the 8s, excluding the 8s themselves
        for c in range(min_c - 1, max_c):
            if c != c1 and c != c2:
                if 0 <= c < grid.width and result[r1][c] == 0:
                    result[r1][c] = 3
                if 0 <= c < grid.width and result[r2][c] == 0:
                    result[r2][c] = 3

        # Draw vertical lines on middle rows
        for r in range(min_r + 1, max_r):
            if 0 <= min_c - 1 < grid.width and result[r][min_c - 1] == 0:
                result[r][min_c - 1] = 3
            if 0 <= max_c + 1 < grid.width and result[r][max_c - 1] == 0:
                result[r][max_c - 1] = 3
    else:
        # Draw bowtie pattern
        row_dir = 1 if r2 > r1 else -1
        col_dir = 1 if c2 > c1 else -1

        # Determine starting row
        if r1 == 0 or r1 == grid.height - 1:
            start_r = r1
            num_rows = row_dist + 1
        else:
            start_r = r1 + row_dir
            num_rows = row_dist - 1

        # Left line: starts at same column as 8, goes straight then diagonal
        r, c = start_r, c1
        for i in range(num_rows):
            if 0 <= r < grid.height and 0 <= c < grid.width and result[r][c] == 0:
                result[r][c] = 3
            r += row_dir
            if i >= num_rows - row_dist + 1:
                c += col_dir

        # Right line: starts one step away, stays put briefly, then diagonal, then stays
        r, c = start_r, c1 + (-1 if c2 < c1 else 1)
        for i in range(num_rows):
            if 0 <= r < grid.height and 0 <= c < grid.width and result[r][c] == 0:
                result[r][c] = 3
            r += row_dir
            if 0 < i < num_rows - 2:
                c += col_dir

    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("cb227835", solve)
