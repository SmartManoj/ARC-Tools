import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Add colored borders around detected objects.
    '''
    result = grid.copy()
    objects = detect_objects(grid, ignore_colors=[0])

    for obj in objects:
        color = obj.color
        # Determine border color
        border_color = 2 if color == 3 else 4

        # Add border around object
        for r in range(max(0, obj.top-1), min(result.height, obj.bottom+2)):
            for c in range(max(0, obj.left-1), min(result.width, obj.right+2)):
                if result[r][c] == 0:
                    # Check if adjacent to object
                    for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                        nr, nc = r+dr, c+dc
                        if 0 <= nr < result.height and 0 <= nc < result.width:
                            if grid[nr][nc] == color:
                                result[r][c] = border_color
                                break

    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("b7fb29bc", solve)
