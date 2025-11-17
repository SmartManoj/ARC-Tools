import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Find all red (2) pixels and create colored borders around them:
    - Adjacent gray (5) pixels (orthogonal) become orange (7)
    - Diagonal gray (5) pixels become yellow (4)
    '''
    result = grid.copy()
    width, height = grid.shape

    # Find all red pixels
    red_pixels = []
    for row in range(height):
        for col in range(width):
            if grid[row][col] == 2:
                red_pixels.append((row, col))

    # For each red pixel, color its neighbors
    for row, col in red_pixels:
        # Check orthogonal neighbors (become orange/7)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = row + dr, col + dc
            if 0 <= nr < height and 0 <= nc < width and grid[nr][nc] == 5:
                result[nr][nc] = 7

        # Check diagonal neighbors (become yellow/4)
        for dr, dc in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            nr, nc = row + dr, col + dc
            if 0 <= nr < height and 0 <= nc < width and grid[nr][nc] == 5:
                result[nr][nc] = 4

    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("9caba7c3", solve)
