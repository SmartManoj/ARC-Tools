import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Sort overlapping colored rectangles by depth/layer.
    Multiple colored filled rectangles overlap, and the output reorganizes them.
    '''
    # Detect objects (colored rectangles)
    objects = detect_objects(grid)

    if not objects:
        return grid

    # Sort objects by size (smaller objects on top)
    objects.sort(key=lambda obj: len(obj.positions))

    # Reconstruct the grid with sorted layers
    result = grid.copy()

    # Redraw objects in order (largest first, so smallest is on top)
    for obj in reversed(objects):
        for r, c in obj.positions:
            result[r, c] = obj.color

    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("c6e1b8da", solve)
