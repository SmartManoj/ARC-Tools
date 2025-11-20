import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Fill rectangles with concentric layers using marker colors:
    - Find rectangle outline (color 1)
    - Find marker colors above/left of rectangle
    - Fill interior with concentric layers alternating marker colors
    '''
    output = [[grid[i][j] for j in range(grid.width)] for i in range(grid.height)]

    # Find rectangle (continuous outline of 1s)
    ones = [(r, c) for r in range(grid.height) for c in range(grid.width) if grid[r][c] == 1]
    if not ones:
        return grid

    min_r = min(r for r, c in ones)
    max_r = max(r for r, c in ones)
    min_c = min(c for r, c in ones)
    max_c = max(c for r, c in ones)

    # Get marker colors (non-0, non-1 colors above/left of rectangle)
    markers = []
    for r in range(min_r):
        for c in range(grid.width):
            if grid[r][c] not in [0, 1]:
                markers.append(grid[r][c])

    if not markers:
        return grid

    # Fill rectangle interior with concentric layers
    for r in range(min_r + 1, max_r):
        for c in range(min_c + 1, max_c):
            # Calculate distance to nearest edge (Manhattan distance to boundary)
            dist_to_edge = min(r - min_r, max_r - r, c - min_c, max_c - c)
            # Use marker color based on distance (clamped to last marker, not cycling)
            color_idx = min(dist_to_edge - 1, len(markers) - 1)
            output[r][c] = markers[color_idx]

    return Grid(output)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("99306f82", solve)
