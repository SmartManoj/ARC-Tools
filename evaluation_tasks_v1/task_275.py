import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Expand small patterns into larger grids.
    '''
    # Find objects and expand them
    objects = detect_objects(grid, ignore_colors=[0])

    if not objects:
        return grid

    # Determine output size
    out_size = 18
    result = Grid([[0] * out_size for _ in range(out_size)])

    # Replicate pattern
    for obj in objects:
        scale = 3
        for r in range(obj.height):
            for c in range(obj.width):
                val = obj[r][c]
                for dr in range(scale):
                    for dc in range(scale):
                        nr, nc = obj.top + r * scale + dr, obj.left + c * scale + dc
                        if nr < out_size and nc < out_size:
                            result[nr][nc] = val

    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("b4a43f3b", solve)
