import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Surround red (2) pixels in green (3) regions with blue (1) pixels.
    '''
    result = grid.copy()
    width, height = grid.shape
    
    red_pixels = []
    for row in range(height):
        for col in range(width):
            if grid[row][col] == 2:
                red_pixels.append((row, col))
    
    for row, col in red_pixels:
        for dr, dc in [(0,1), (0,-1), (1,0), (-1,0), (1,1), (1,-1), (-1,1), (-1,-1)]:
            nr, nc = row + dr, col + dc
            if 0 <= nr < height and 0 <= nc < width and grid[nr][nc] == 3:
                result[nr][nc] = 1
    
    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("a04b2602", solve)
