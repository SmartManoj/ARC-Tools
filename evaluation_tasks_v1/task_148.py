import os
from arc_tools.grid import Grid
from arc_tools import logger
from helper import solve_task

def solve(grid: Grid):
    '''
    Connects diamond patterns with blue (1) lines.

    Pattern:
    1. Identify diamond patterns: a cell with value 0 surrounded by 4 cells with value 2
       in cardinal directions (up, down, left, right)
    2. For pairs of diamonds on the same row, fill the space between them with 1s
    3. For pairs of diamonds on the same column, fill the space between them with 1s
    4. The filling excludes the diamond cells themselves
    '''
    # Create a copy of the grid for output
    output_data = [[grid[r][c] for c in range(grid.width)] for r in range(grid.height)]

    # Find all diamond centers (0 surrounded by 2s in cardinal directions)
    diamonds = []
    for r in range(1, grid.height - 1):
        for c in range(1, grid.width - 1):
            if (grid[r][c] == 0 and
                grid[r-1][c] == 2 and
                grid[r+1][c] == 2 and
                grid[r][c-1] == 2 and
                grid[r][c+1] == 2):
                diamonds.append((r, c))

    logger.info(f"Found {len(diamonds)} diamonds at positions: {diamonds}")

    # Group diamonds by row for horizontal connections
    rows_dict = {}
    for r, c in diamonds:
        if r not in rows_dict:
            rows_dict[r] = []
        rows_dict[r].append(c)

    # Connect adjacent diamonds on the same row
    for r, cols in rows_dict.items():
        cols.sort()
        # Connect adjacent diamonds only (don't skip over other diamonds)
        for i in range(len(cols) - 1):
            c1 = cols[i]
            c2 = cols[i + 1]
            # Fill between the diamonds, excluding the diamond cells (±1 from center)
            for c in range(c1 + 2, c2 - 1):
                if output_data[r][c] == 0:
                    output_data[r][c] = 1
            logger.info(f"Connected diamonds at ({r},{c1}) and ({r},{c2}) horizontally")

    # Group diamonds by column for vertical connections
    cols_dict = {}
    for r, c in diamonds:
        if c not in cols_dict:
            cols_dict[c] = []
        cols_dict[c].append(r)

    # Connect adjacent diamonds on the same column
    for c, rows in cols_dict.items():
        rows.sort()
        # Connect adjacent diamonds only (don't skip over other diamonds)
        for i in range(len(rows) - 1):
            r1 = rows[i]
            r2 = rows[i + 1]
            # Fill between the diamonds, excluding the diamond cells (±1 from center)
            for r in range(r1 + 2, r2 - 1):
                if output_data[r][c] == 0:
                    output_data[r][c] = 1
            logger.info(f"Connected diamonds at ({r1},{c}) and ({r2},{c}) vertically")

    return Grid(output_data)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("60a26a3e", solve)
