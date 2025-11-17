import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Extract a pattern from a colored hollow rectangle based on a marker.
    Find hollow rectangles and extract the one indicated by a colored marker.
    '''
    # Find colored hollow rectangles using object detection
    objects = detect_objects(grid)

    # Find marker cells (isolated colored cells)
    marker_color = None
    for r in range(grid.height):
        for c in range(grid.width):
            cell = grid[r, c]
            if cell != Color.BLACK:
                # Check if this is an isolated cell (potential marker)
                neighbors = sum(1 for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]
                               if 0 <= r + dr < grid.height and 0 <= c + dc < grid.width
                               and grid[r + dr, c + dc] == cell)
                if neighbors == 0:
                    marker_color = cell
                    break
        if marker_color:
            break

    # Find the object that matches the marker color or contains it
    for obj in objects:
        if obj.color == marker_color or marker_color in [grid[r, c] for r, c in obj.positions]:
            # Extract this object's bounding box
            return obj.to_grid()

    # Fallback: return first non-trivial object
    if objects:
        for obj in objects:
            if len(obj.positions) > 4:
                return obj.to_grid()

    return grid

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("c658a4bd", solve)
