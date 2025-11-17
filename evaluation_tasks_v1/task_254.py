import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Color 8s with alternating colors 2 and 5.
    This is a complex bipartite graph coloring problem - placeholder uses simple checkerboard.
    TODO: Implement proper bipartite coloring of adjacent 8-cells.
    '''
    result = grid.copy()
    for r in range(grid.height):
        for c in range(grid.width):
            if grid[r][c] == 8:
                # Simple alternating pattern - may need refinement
                result[r][c] = 2 if (r + c) % 2 == 0 else 5
    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("a8610ef7", solve)
