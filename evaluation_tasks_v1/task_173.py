import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    For each non-zero colored pixel, draw a vertical and horizontal line
    extending toward the closer grid edge (top/bottom for vertical, left/right for horizontal).
    '''
    result = Grid([row[:] for row in grid])
    h, w = result.height, result.width

    # Find all non-zero pixels in the original grid
    pixels = []
    for r in range(h):
        for c in range(w):
            if grid[r][c] != 0:
                pixels.append((r, c, grid[r][c]))

    # Process each pixel
    for r, c, color in pixels:
        # Determine vertical direction based on distance to edges
        dist_to_top = r
        dist_to_bottom = h - r - 1

        if dist_to_top <= dist_to_bottom:
            # Draw vertical line upward
            for row in range(0, r + 1):
                result[row][c] = color
        else:
            # Draw vertical line downward
            for row in range(r, h):
                result[row][c] = color

        # Determine horizontal direction based on distance to edges
        dist_to_left = c
        dist_to_right = w - c - 1

        if dist_to_left <= dist_to_right:
            # Draw horizontal line leftward
            for col in range(0, c + 1):
                result[r][col] = color
        else:
            # Draw horizontal line rightward
            for col in range(c, w):
                result[r][col] = color

    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("705a3229", solve)
