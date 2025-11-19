import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Identifies a marker pattern (made of 1s) and uses it to determine
    what color to replace all 8s with. The marker is then cleared.

    Marker patterns:
    - Plus/cross (0 1 0, 1 1 1, 0 1 0) → color 2
    - Sparse (1 0 1, 0 1 0, 1 1 1) → color 3
    - Triangle (1 1 1, 1 0 1, 0 1 0) → color 7
    '''
    # Create a copy to modify
    output_grid = [[grid[y][x] for x in range(grid.width)] for y in range(grid.height)]

    # Find the marker pattern (cells with value 1)
    marker_cells = []
    for y in range(grid.height):
        for x in range(grid.width):
            if grid[y][x] == 1:
                marker_cells.append((x, y))

    if not marker_cells:
        return Grid(output_grid)

    # Get bounding box of marker
    min_x = min(x for x, y in marker_cells)
    max_x = max(x for x, y in marker_cells)
    min_y = min(y for x, y in marker_cells)
    max_y = max(y for x, y in marker_cells)

    # Extract normalized marker pattern (relative to top-left of bounding box)
    marker_pattern = set()
    for x, y in marker_cells:
        marker_pattern.add((x - min_x, y - min_y))

    # Define marker patterns
    plus_pattern = {(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)}
    triangle_pattern = {(0, 0), (1, 0), (2, 0), (0, 1), (2, 1), (1, 2)}
    sparse_pattern = {(0, 0), (2, 0), (1, 1), (0, 2), (1, 2), (2, 2)}

    # Determine target color based on marker pattern
    target_color = None
    if marker_pattern == plus_pattern:
        target_color = 2
    elif marker_pattern == triangle_pattern:
        target_color = 7
    elif marker_pattern == sparse_pattern:
        target_color = 3
    else:
        # If pattern doesn't match, try to identify by structure
        logger.info(f"Unknown marker pattern: {marker_pattern}")
        # Default fallback
        target_color = 2

    # Replace all 8s with target color and clear marker (1s to 0s)
    for y in range(grid.height):
        for x in range(grid.width):
            if grid[y][x] == 8:
                output_grid[y][x] = target_color
            elif grid[y][x] == 1:
                output_grid[y][x] = 0

    return Grid(output_grid)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("009d5c81", solve)
