import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Transform regions containing colored pattern markers by tiling the pattern.

    For each rectangular region:
    1. Extract the small pattern defined by non-zero, non-background colored pixels
    2. Tile that pattern across the entire region

    Example: A 2x2 pattern [[1,1],[1,0]] tiles to fill an 8x6 region by repeating
    the pattern both horizontally and vertically.
    '''
    result = grid.copy()

    # Find all rectangular regions (objects), ignoring the background color 8
    objects = detect_objects(grid, ignore_colors=[8], go_diagonal=False)

    for obj in objects:
        # Get the bounding box of the object
        min_r, max_r = obj.region.y1, obj.region.y2
        min_c, max_c = obj.region.x1, obj.region.x2

        # Find the bounding box of the colored pattern (non-zero, non-8 pixels)
        pattern_min_r, pattern_max_r = None, None
        pattern_min_c, pattern_max_c = None, None

        for r in range(min_r, max_r + 1):
            for c in range(min_c, max_c + 1):
                val = grid[r][c]
                if val not in [0, 8]:
                    if pattern_min_r is None:
                        pattern_min_r = r
                        pattern_max_r = r
                        pattern_min_c = c
                        pattern_max_c = c
                    else:
                        pattern_min_r = min(pattern_min_r, r)
                        pattern_max_r = max(pattern_max_r, r)
                        pattern_min_c = min(pattern_min_c, c)
                        pattern_max_c = max(pattern_max_c, c)

        if pattern_min_r is None:
            continue

        # Extract the pattern
        pattern_height = pattern_max_r - pattern_min_r + 1
        pattern_width = pattern_max_c - pattern_min_c + 1
        pattern = [[grid[pattern_min_r + dr][pattern_min_c + dc]
                    for dc in range(pattern_width)]
                   for dr in range(pattern_height)]

        # Tile the pattern across the entire region
        for r in range(min_r, max_r + 1):
            for c in range(min_c, max_c + 1):
                if grid[r][c] == 8:
                    continue

                # Calculate the position within the pattern
                pattern_r = (r - min_r) % pattern_height
                pattern_c = (c - min_c) % pattern_width
                result[r][c] = pattern[pattern_r][pattern_c]

    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("a57f2f04", solve)
