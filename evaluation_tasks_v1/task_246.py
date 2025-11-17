import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Fill the black region with a pattern of yellow (4) and blue (1) pixels.
    '''
    result = grid.copy()
    width, height = grid.shape
    
    # Find the boundary between colored and black regions
    boundary_col = width
    for col in range(width):
        for row in range(height):
            if grid[row][col] == 0:
                boundary_col = min(boundary_col, col)
                break
    
    # Fill with pattern
    for row in range(height):
        for col in range(boundary_col, width):
            if grid[row][col] == 0:
                # Checkerboard-like pattern
                if (row + col) % 2 == 0:
                    result[row][col] = 4 if (row % 3 != col % 3) else 1
                else:
                    result[row][col] = 1 if (row % 2 == 0) else 4
    
    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("9f27f097", solve)
