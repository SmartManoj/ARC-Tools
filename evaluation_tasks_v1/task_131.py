import os
from arc_tools.grid import Grid
from arc_tools import logger
from helper import solve_task


def solve(grid: Grid):
    '''
    Pattern: Find cross/plus shapes (made of 3s) and connect them with diagonal
    lines (2s) when they are perfectly aligned diagonally.

    Steps:
    1. Detect all cross/plus shapes (5 cells forming a + pattern with value 3)
    2. Find the center of each cross
    3. For each pair of crosses, if they're perfectly diagonal (|Δrow| = |Δcol|),
       draw a line of 2s between them
    '''
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0

    # Create output as a copy of input
    output = [[grid[r][c] for c in range(width)] for r in range(height)]

    # Find all cross centers
    crosses = []
    for r in range(1, height - 1):
        for c in range(1, width - 1):
            # Check if this is the center of a cross (+ shape)
            if (grid[r][c] == 3 and
                grid[r-1][c] == 3 and  # top
                grid[r+1][c] == 3 and  # bottom
                grid[r][c-1] == 3 and  # left
                grid[r][c+1] == 3):    # right
                crosses.append((r, c))

    # Connect crosses that are perfectly diagonal
    for i in range(len(crosses)):
        for j in range(i + 1, len(crosses)):
            r1, c1 = crosses[i]
            r2, c2 = crosses[j]

            dr = abs(r2 - r1)
            dc = abs(c2 - c1)

            # Check if they're perfectly diagonal
            if dr == dc and dr > 0:
                # Draw diagonal line between them
                # Determine direction
                row_step = 1 if r2 > r1 else -1
                col_step = 1 if c2 > c1 else -1

                # Draw line from center1 to center2 (excluding the centers themselves)
                r, c = r1 + row_step, c1 + col_step
                while (r, c) != (r2, c2):
                    # Only place 2s, don't overwrite 3s
                    if output[r][c] == 0:
                        output[r][c] = 2
                    r += row_step
                    c += col_step

    return Grid(output)


if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("55059096", solve)
