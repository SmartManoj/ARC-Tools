import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Reduce large grid to 3x3 by extracting key pattern.
    '''
    objects = detect_objects(grid, ignore_colors=[0])

    # Create 3x3 output
    result = Grid([[0] * 3 for _ in range(3)])

    if objects:
        obj = objects[0]
        # Sample or condense pattern
        for r in range(min(3, obj.height)):
            for c in range(min(3, obj.width)):
                result[r][c] = obj[r][c]

    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("b7999b51", solve)
