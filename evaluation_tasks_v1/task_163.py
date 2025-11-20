import os
from arc_tools.grid import Grid
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Find two L-shaped structures made of 2s (each containing a 5).
    Draw a rectangular corridor filled with 4s connecting them.
    '''
    result = Grid([row[:] for row in grid])
    h, w = result.height, result.width

    # Find all connected components of 2s
    visited = [[False] * w for _ in range(h)]
    shapes = []

    def flood_fill(r, c):
        if r < 0 or r >= h or c < 0 or c >= w:
            return []
        if visited[r][c] or grid[r][c] != 2:
            return []
        visited[r][c] = True
        cells = [(r, c)]
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            cells.extend(flood_fill(r + dr, c + dc))
        return cells

    for r in range(h):
        for c in range(w):
            if not visited[r][c] and grid[r][c] == 2:
                shape = flood_fill(r, c)
                if shape:
                    shapes.append(shape)

    if len(shapes) != 2:
        return result

    def get_bbox(shape):
        rs = [r for r, c in shape]
        cs = [c for r, c in shape]
        return min(rs), max(rs), min(cs), max(cs)

    r1_min, r1_max, c1_min, c1_max = get_bbox(shapes[0])
    r2_min, r2_max, c2_min, c2_max = get_bbox(shapes[1])

    # Sort by row
    if r1_min <= r2_min:
        rtop_min, rtop_max, ctop_min, ctop_max = r1_min, r1_max, c1_min, c1_max
        rbot_min, rbot_max, cbot_min, cbot_max = r2_min, r2_max, c2_min, c2_max
    else:
        rtop_min, rtop_max, ctop_min, ctop_max = r2_min, r2_max, c2_min, c2_max
        rbot_min, rbot_max, cbot_min, cbot_max = r1_min, r1_max, c1_min, c1_max

    # Simple approach: fill from the corridor between shapes
    # Fill all rows from top shape to bottom shape
    for r in range(rtop_max, rbot_max):
        # For each row, determine column fill range
        # Find shape cells in this row
        shape_cells = [c for c in range(w) if grid[r][c] == 2 or grid[r][c] == 5]

        if not shape_cells:
            # No shape in this row - fill the gap
            c_left = min(ctop_min, cbot_min) - 1 if min(ctop_min, cbot_min) > 0 else 0
            c_right = max(ctop_max, cbot_max) + 1 if max(ctop_max, cbot_max) < w - 1 else w - 1

            # Adjust based on relative positions
            if ctop_max < cbot_min:  # top is left of bottom
                c_left = ctop_max - 1
                c_right = cbot_max
            elif cbot_max < ctop_min:  # bottom is left of top
                c_left = cbot_max - 1
                c_right = ctop_max + 1 if ctop_max < w - 1 else ctop_max

            for c in range(c_left, c_right + 1):
                if result[r][c] == 0:
                    result[r][c] = 4
        elif r >= rtop_min and r <= rtop_max:
            # Row has shape from top - extend towards bottom shape
            first_sc = min(shape_cells)
            last_sc = max(shape_cells)

            if ctop_max < cbot_min:
                # Top left of bottom - fill right
                c_fill_min = last_sc
                c_fill_max = cbot_max + 1 if cbot_max < w - 1 else cbot_max
            elif cbot_max < ctop_min:
                # Bottom left of top - fill right
                c_fill_min = last_sc
                c_fill_max = min(w - 1, last_sc + 2)
            else:
                # Overlapping - fill corridor
                c_fill_min = min(ctop_min, cbot_min) - 1 if min(ctop_min, cbot_min) > 0 else 0
                c_fill_max = max(ctop_max, cbot_max)

            for c in range(c_fill_min, c_fill_max + 1):
                if result[r][c] == 0:
                    result[r][c] = 4
        elif r >= rbot_min and r <= rbot_max:
            # Row has shape from bottom - extend towards gap or into gaps
            first_sc = min(shape_cells)
            last_sc = max(shape_cells)

            # Check for interior gaps
            interior_gaps = [c for c in range(first_sc, last_sc + 1) if grid[r][c] == 0]
            if interior_gaps:
                # Fill interior
                for c in interior_gaps:
                    result[r][c] = 4
            else:
                # Extend based on position
                if ctop_max < cbot_min:
                    # Fill towards the gap
                    for c in range(ctop_max - 1, first_sc):
                        if result[r][c] == 0:
                            result[r][c] = 4
                elif cbot_max < ctop_min:
                    # Fill extending right
                    for c in range(last_sc, min(w, last_sc + 3)):
                        if result[r][c] == 0:
                            result[r][c] = 4

    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("692cd3b6", solve)
