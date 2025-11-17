import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Draw squares on the left based on colored pixels on the right edge.
    '''
    result = grid.copy()
    width, height = grid.shape
    
    row = 0
    while row < height:
        color = grid[row][width-1]
        if color != 0:
            size = 1
            while row + size < height and grid[row + size][width - 1] == color:
                size += 1
            
            # Draw square
            for r in range(row, min(row + size, height)):
                for c in range(min(size, width)):
                    result[r][c] = color
            
            row += size
        else:
            row += 1
    
    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("a406ac07", solve)
