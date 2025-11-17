import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Assign colors 1-4 to gray (8) cells based on 2x2 block checkerboard pattern.
    Pattern: Divide grid into 2x2 blocks, assign color based on block position modulo 2.
    - Even row//2, even col//2 → color 1
    - Even row//2, odd col//2 → color 4
    - Odd row//2, even col//2 → color 3
    - Odd row//2, odd col//2 → color 2

    Note: This pattern works perfectly for some examples but not all.
    The actual pattern may be more complex and context-dependent.
    '''
    result = Grid([[0 for _ in range(len(grid[0]))] for _ in range(len(grid))])

    # Process each cell
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] != Color.BLACK.value:
                # Determine which 2x2 block this cell belongs to
                block_row = (row // 2) % 2
                block_col = (col // 2) % 2

                # Color based on block position in checkerboard pattern
                block_type = block_row * 2 + block_col
                color = [1, 4, 3, 2][block_type]

                result[row][col] = color

    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("626c0bcc", solve)
