import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Copy pattern elements between similar boxes.
    '''
    result = grid.copy()
    width, height = grid.shape
    
    # Find red boxes
    boxes = []
    visited = [[False] * width for _ in range(height)]
    
    for row in range(height):
        for col in range(width):
            if grid[row][col] == 2 and not visited[row][col]:
                # Find box bounds
                min_r, max_r, min_c, max_c = row, row, col, col
                stack = [(row, col)]
                box_points = []
                while stack:
                    r, c = stack.pop()
                    if r < 0 or r >= height or c < 0 or c >= width or visited[r][c]:
                        continue
                    if grid[r][c] in [0, 2, 3, 1, 6]:
                        visited[r][c] = True
                        box_points.append((r, c))
                        min_r, max_r = min(min_r, r), max(max_r, r)
                        min_c, max_c = min(min_c, c), max(max_c, c)
                        for dr, dc in [(0,1), (0,-1), (1,0), (-1,0)]:
                            stack.append((r+dr, c+dc))
                
                if box_points:
                    boxes.append((min_r, max_r, min_c, max_c, box_points))
    
    # Copy patterns between boxes
    if len(boxes) >= 2:
        for i in range(len(boxes)-1):
            b1 = boxes[i]
            b2 = boxes[i+1]
            for r, c in b1[4]:
                val = grid[r][c]
                if val not in [0, 2]:
                    offset_r, offset_c = r - b1[0], c - b1[2]
                    target_r, target_c = b2[0] + offset_r, b2[2] + offset_c
                    if 0 <= target_r < height and 0 <= target_c < width:
                        if grid[target_r][target_c] == 3:
                            result[target_r][target_c] = val
    
    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("a096bf4d", solve)
