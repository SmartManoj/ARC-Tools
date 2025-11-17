import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Create a 5x5 output with a symmetric pattern and cross of zeros.
    The output has 2x2 blocks in corners with a cross divider.
    '''
    # Create 5x5 output
    result = [[0 for _ in range(5)] for _ in range(5)]

    # Check each quadrant of the 6x6 input to determine the 2x2 pattern
    # Top-left quadrant (0-2, 0-2)
    tl = 8 if any(grid[r][c] == 8 for r in range(3) for c in range(3)) else 0
    # Top-right quadrant (0-2, 3-5)
    tr = 8 if any(grid[r][c] == 8 for r in range(3) for c in range(3, 6)) else 0
    # Bottom-left quadrant (3-5, 0-2)
    bl = 8 if any(grid[r][c] == 8 for r in range(3, 6) for c in range(3)) else 0
    # Bottom-right quadrant (3-5, 3-5)
    br = 8 if any(grid[r][c] == 8 for r in range(3, 6) for c in range(3, 6)) else 0

    # Create 2x2 pattern
    pattern = [[tl, tr], [bl, br]]

    # Place pattern in all 4 quadrants with cross divider at row 2 and col 2
    for qr in [0, 3]:
        for qc in [0, 3]:
            result[qr][qc] = pattern[0][0]
            result[qr][qc+1] = pattern[0][1]
            result[qr+1][qc] = pattern[1][0]
            result[qr+1][qc+1] = pattern[1][1]

    return Grid(result)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("b1fc8b8e", solve)
