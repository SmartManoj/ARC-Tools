import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    For each diamond-shaped object (made of 8s), add yellow (4) triangular extensions
    at the cardinal directions (north, south, east, west), pointing outward from the diamond.
    '''
    result = grid.copy()
    objects = detect_objects(grid)

    for obj in objects:
        if obj.color != 8:  # Only process cyan (8) objects
            continue

        # Find the bounding box
        min_r, max_r = obj.region.y1, obj.region.y2
        min_c, max_c = obj.region.x1, obj.region.x2
        center_r = (min_r + max_r) // 2
        center_c = (min_c + max_c) // 2

        # Find the widest part horizontally (rows with maximum width)
        row_widths = {}
        max_width = 0
        for r in range(min_r, max_r + 1):
            width = sum(1 for c in range(grid.width) if grid[r][c] == 8)
            row_widths[r] = width
            max_width = max(max_width, width)
        widest_rows = [r for r, w in row_widths.items() if w == max_width]
        mid_widest_r = widest_rows[len(widest_rows) // 2]

        # Add triangles at the cardinal directions
        # Pattern: at distance d from edge, fill center ± (2 - d)

        # Top triangle (pointing up from the top edge)
        for d in range(1, 3):
            r = min_r - d
            if r < 0:
                break
            spread = 2 - d
            for c in range(center_c - spread, center_c + spread + 1):
                if 0 <= c < grid.width and result[r][c] == 0:
                    result[r][c] = 4

        # Bottom triangle (pointing down from the bottom edge)
        for d in range(1, 3):
            r = max_r + d
            if r >= grid.height:
                break
            spread = 2 - d
            for c in range(center_c - spread, center_c + spread + 1):
                if 0 <= c < grid.width and result[r][c] == 0:
                    result[r][c] = 4

        # Left and Right triangles: need to iterate over all widest rows
        # and extend based on distance from the middle widest row
        for r in range(min_r, max_r + 1):
            if row_widths[r] != max_width:
                continue
            # Distance from the middle of widest rows
            dist_from_mid = abs(r - mid_widest_r)
            spread = max(0, 2 - dist_from_mid)

            # Left triangle
            for d in range(1, spread + 1):
                c = min_c - d
                if c >= 0 and result[r][c] == 0:
                    result[r][c] = 4

            # Right triangle
            for d in range(1, spread + 1):
                c = max_c + d
                if c < grid.width and result[r][c] == 0:
                    result[r][c] = 4

    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("9772c176", solve)
