import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Vertically reflect the bottom pattern to the top half of the grid.
    '''
    result = grid.copy()
    width, height = grid.shape
    
    for row in range(height // 2):
        for col in range(width):
            result[row][col] = grid[height - 1 - row][col]
    
    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("9ddd00f0", solve)
