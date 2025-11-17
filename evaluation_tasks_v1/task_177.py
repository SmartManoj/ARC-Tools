import os
from arc_tools.grid import Grid
from arc_tools import logger
from helper import solve_task

def solve(grid: Grid):
    '''
    Find the bounding box of all non-zero cells.
    Extract and return the top-left 4x4 quadrant of that bounding box.
    '''
    h, w = grid.height, grid.width

    # Find bounding box of all non-zero cells
    min_r, max_r = float('inf'), -1
    min_c, max_c = float('inf'), -1

    for r in range(h):
        for c in range(w):
            if grid[r][c] != 0:
                min_r = min(min_r, r)
                max_r = max(max_r, r)
                min_c = min(min_c, c)
                max_c = max(max_c, c)

    # If no non-zero cells found, return empty grid
    if min_r == float('inf'):
        return Grid([[0] * 4 for _ in range(4)])

    # Extract top-left 4x4 quadrant from bounding box
    result = []
    for r in range(min_r, min_r + 4):
        row = []
        for c in range(min_c, min_c + 4):
            row.append(grid[r][c])
        result.append(row)

    return Grid(result)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("73182012", solve)
