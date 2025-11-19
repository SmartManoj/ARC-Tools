import os
from arc_tools.grid import Grid
from arc_tools import logger
from helper import solve_task

def solve(grid: Grid):
    '''
    Pattern Analysis:
    - Find rows and columns with 2+ occurrences of value 1
    - Fill those rows/columns with 1s
    - Find all contiguous 2-blocks (connected components of 2s)
    - If a 2-block intersects with any filled row/column, convert the ENTIRE block to 1s
    '''
    # Create a copy of the grid
    output_grid = [[grid[y][x] for x in range(grid.width)] for y in range(grid.height)]

    # Count 1s in each row
    rows_to_fill = set()
    for r in range(grid.height):
        count = sum(1 for c in range(grid.width) if grid[r][c] == 1)
        if count >= 2:
            rows_to_fill.add(r)

    # Count 1s in each column
    cols_to_fill = set()
    for c in range(grid.width):
        count = sum(1 for r in range(grid.height) if grid[r][c] == 1)
        if count >= 2:
            cols_to_fill.add(c)

    # Find all contiguous 2-blocks using flood fill
    visited = [[False] * grid.width for _ in range(grid.height)]
    blocks = []

    def flood_fill(start_r, start_c):
        """Find all cells in a contiguous block of 2s"""
        stack = [(start_r, start_c)]
        block_cells = []
        while stack:
            r, c = stack.pop()
            if r < 0 or r >= grid.height or c < 0 or c >= grid.width:
                continue
            if visited[r][c] or grid[r][c] != 2:
                continue
            visited[r][c] = True
            block_cells.append((r, c))
            # Check 4 neighbors
            stack.extend([(r-1, c), (r+1, c), (r, c-1), (r, c+1)])
        return block_cells

    # Find all 2-blocks
    for r in range(grid.height):
        for c in range(grid.width):
            if grid[r][c] == 2 and not visited[r][c]:
                block = flood_fill(r, c)
                if block:
                    blocks.append(block)

    # Check which blocks intersect with rows/columns to fill
    blocks_to_convert = set()
    for i, block in enumerate(blocks):
        for r, c in block:
            if r in rows_to_fill or c in cols_to_fill:
                blocks_to_convert.add(i)
                break

    # Convert intersecting blocks to 1s
    for i in blocks_to_convert:
        for r, c in blocks[i]:
            output_grid[r][c] = 1

    # Fill rows with 2+ occurrences of 1
    for r in rows_to_fill:
        for c in range(grid.width):
            if output_grid[r][c] == 0:
                output_grid[r][c] = 1

    # Fill columns with 2+ occurrences of 1
    for c in cols_to_fill:
        for r in range(grid.height):
            if output_grid[r][c] == 0:
                output_grid[r][c] = 1

    return Grid(output_grid)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("0d87d2a6", solve)
