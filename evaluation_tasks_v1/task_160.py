import os
from arc_tools.grid import Grid
from arc_tools import logger
from helper import solve_task

def solve(grid: Grid):
    '''
    Find the 4x4 block of 3s (marker region).
    Extract the vertically reflected 4x4 region from the grid.
    The reflection maps each row i to row (15 - i) in the 16x16 grid.
    '''

    # Find the 4x4 block of 3s
    min_r = max_r = min_c = max_c = None
    h, w = grid.height, grid.width

    for r in range(h):
        for c in range(w):
            if grid[r][c] == 3:
                if min_r is None:
                    min_r = max_r = r
                    min_c = max_c = c
                else:
                    min_r = min(min_r, r)
                    max_r = max(max_r, r)
                    min_c = min(min_c, c)
                    max_c = max(max_c, c)

    # If no 3s found, return empty 4x4 grid
    if min_r is None:
        return Grid([[0] * 4 for _ in range(4)])

    # Calculate reflected position using vertical mirror around center
    # For a 16x16 grid (rows 0-15), reflection maps row i to row (15 - i)
    reflected_start = 15 - max_r  # row where reflection of row max_r maps to
    reflected_end = 15 - min_r    # row where reflection of row min_r maps to

    # Extract the reflected region (from reflected_end down to reflected_start)
    result = []
    for r in range(reflected_end, reflected_start - 1, -1):
        row = [grid[r][c] for c in range(min_c, max_c + 1)]
        result.append(row)

    return Grid(result)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("67b4a34d", solve)
