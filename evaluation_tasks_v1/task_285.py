import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Reduce grid size by extracting key pattern.
    '''
    # Find the pattern
    objects = detect_objects(grid, ignore_colors=[0])

    # Create 4x4 output
    result = Grid([[0] * 4 for _ in range(4)])

    if objects:
        obj = objects[0]
        for r in range(min(4, obj.height)):
            for c in range(min(4, obj.width)):
                result[r][c] = obj[r][c]

    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("bbb1b8b6", solve)
