import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Double the grid width horizontally.
    If the first cell is 0:
        - Left half: copy of input
        - Right half: complement of reversed input (0->8, 2->0)
    If the first cell is 2:
        - Left half: complement of reversed input (0->8, 2->0)
        - Right half: copy of input
    '''
    h, w = grid.height, grid.width
    result = Grid([[0] * (w * 2) for _ in range(h)])

    # Helper function to complement: 0->8, 2->0
    def complement(val):
        return 8 if val == 0 else 0

    # Check the first cell value
    first_cell = grid[0][0]

    if first_cell == 0:
        # Left half: copy of input
        for r in range(h):
            for c in range(w):
                result[r][c] = grid[r][c]

        # Right half: complement of reversed input (0->8, 2->0)
        for r in range(h):
            for c in range(w):
                reversed_val = grid[r][w - 1 - c]  # reverse index
                result[r][w + c] = complement(reversed_val)
    else:  # first_cell == 2
        # Left half: complement of reversed input (0->8, 2->0)
        for r in range(h):
            for c in range(w):
                reversed_val = grid[r][w - 1 - c]  # reverse index
                result[r][c] = complement(reversed_val)

        # Right half: copy of input
        for r in range(h):
            for c in range(w):
                result[r][w + c] = grid[r][c]

    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("6f473927", solve)
