import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Extract a pattern from colored rectangles based on blue markers.
    Blue cells mark corners of a region containing colored rectangles.
    The output extracts the pattern within the marked region.
    '''
    # Find blue (1) marker cells
    blue_cells = []
    for r in range(grid.height):
        for c in range(grid.width):
            if grid[r, c] == Color.BLUE:
                blue_cells.append((r, c))

    if len(blue_cells) < 4:
        return grid

    # Find the bounding box of blue markers
    rows = [r for r, c in blue_cells]
    cols = [c for r, c in blue_cells]
    min_r, max_r = min(rows), max(rows)
    min_c, max_c = min(cols), max(cols)

    # Extract the region
    height = max_r - min_r + 1
    width = max_c - min_c + 1
    result = Grid.empty(height, width)

    for r in range(height):
        for c in range(width):
            result[r, c] = grid[min_r + r, min_c + c]

    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("c62e2108", solve)
