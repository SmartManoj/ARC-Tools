import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Draw red (2) cross patterns around each green (3) pixel.
    '''
    result = grid.copy()
    width, height = grid.shape
    
    green_pixels = []
    for row in range(height):
        for col in range(width):
            if grid[row][col] == 3:
                green_pixels.append((row, col))
    
    for row, col in green_pixels:
        # Draw vertical and horizontal lines
        for dr in range(-2, 3):
            if 0 <= row + dr < height and grid[row + dr][col] == 0:
                result[row + dr][col] = 2
        for dc in range(-2, 3):
            if 0 <= col + dc < width and grid[row][col + dc] == 0:
                result[row][col + dc] = 2
    
    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("9def23fe", solve)
