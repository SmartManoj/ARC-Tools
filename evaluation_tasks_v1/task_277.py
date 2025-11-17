import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Condense grid by sampling every Nth cell.
    '''
    # Create 3x4 output
    result = Grid([[0] * 4 for _ in range(3)])

    # Sample from input
    scale_r = grid.height // 3
    scale_c = grid.width // 4

    for r in range(3):
        for c in range(4):
            # Sample from corresponding region
            sr, sc = r * scale_r, c * scale_c
            if sr < grid.height and sc < grid.width:
                result[r][c] = grid[sr][sc]

    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("b7cb93ac", solve)
