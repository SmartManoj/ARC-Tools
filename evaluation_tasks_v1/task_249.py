import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Draw nested rectangles inside a gray (5) frame, with each level getting smaller.
    '''
    result = grid.copy()
    width, height = grid.shape
    
    # Find gray frame bounds
    min_r, max_r, min_c, max_c = height, -1, width, -1
    for row in range(height):
        for col in range(width):
            if grid[row][col] == 5:
                min_r, max_r = min(min_r, row), max(max_r, row)
                min_c, max_c = min(min_c, col), max(max_c, col)
    
    if max_r < 0:
        return result
    
    # Fill interior with nested pattern
    current_color = 2
    offset = 1
    while min_r + offset <= max_r - offset and min_c + offset <= max_c - offset:
        # Draw rectangle at current offset
        for col in range(min_c + offset, max_c - offset + 1):
            if result[min_r + offset][col] == 0:
                result[min_r + offset][col] = current_color
            if result[max_r - offset][col] == 0:
                result[max_r - offset][col] = current_color
        for row in range(min_r + offset, max_r - offset + 1):
            if result[row][min_c + offset] == 0:
                result[row][min_c + offset] = current_color
            if result[row][max_c - offset] == 0:
                result[row][max_c - offset] = current_color
        
        offset += 1
        current_color = 5 if current_color == 2 else 2
    
    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("a3f84088", solve)
