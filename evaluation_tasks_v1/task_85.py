import os
from arc_tools.grid import Grid
from helper import solve_task

def solve(grid: Grid):
    '''
    Pattern: Grid has a template of gray (5) cells arranged in 3x3 blocks,
    and a colored region that serves as a color map.

    Each 3x3 block of grays is filled with the color from the corresponding
    position in the color map. All 5s in a block are replaced with the color,
    while 0s remain 0.

    Example:
    - Color map at position [i][j] contains color C
    - Block at position (i, j) in the grid has all its 5s replaced with color C
    '''

    # Step 1: Find the colored region (non-0, non-5 cells)
    colored_cells = []
    for r in range(grid.height):
        for c in range(grid.width):
            if grid[r][c] != 0 and grid[r][c] != 5:
                colored_cells.append((r, c, grid[r][c]))

    if not colored_cells:
        return grid  # No colored region found

    # Get bounding box of colored region
    min_r = min(r for r, c, v in colored_cells)
    max_r = max(r for r, c, v in colored_cells)
    min_c = min(c for r, c, v in colored_cells)
    max_c = max(c for r, c, v in colored_cells)

    # Extract color map
    color_map = []
    for r in range(min_r, max_r + 1):
        row = []
        for c in range(min_c, max_c + 1):
            row.append(grid[r][c])
        color_map.append(row)

    # Step 2: Find the first gray block (3x3 with 5s)
    first_block_r = None
    first_block_c = None

    for r in range(grid.height - 2):
        for c in range(grid.width - 2):
            # Check for a 3x3 block with 5s (center may be 0 or 5)
            if grid[r][c] == 5 and grid[r][c+1] == 5 and grid[r][c+2] == 5:
                first_block_r = r
                first_block_c = c
                break
        if first_block_r is not None:
            break

    if first_block_r is None:
        return grid  # No blocks found

    # Step 3: Fill each block with corresponding color from color map
    # Blocks are spaced 4 units apart (3 for block + 1 separator)
    output_data = [[grid[r][c] for c in range(grid.width)] for r in range(grid.height)]

    block_spacing = 4  # Standard spacing between blocks

    for block_row_idx in range(len(color_map)):
        for block_col_idx in range(len(color_map[0])):
            # Calculate position of this block
            block_r = first_block_r + block_row_idx * block_spacing
            block_c = first_block_c + block_col_idx * block_spacing

            # Check if block is within grid bounds
            if block_r + 2 >= grid.height or block_c + 2 >= grid.width:
                continue

            # Get color for this block
            color = color_map[block_row_idx][block_col_idx]

            # Fill the 3x3 block: replace all 5s with the color
            for dr in range(3):
                for dc in range(3):
                    r = block_r + dr
                    c = block_c + dc
                    if grid[r][c] == 5:
                        output_data[r][c] = color

    return Grid(output_data)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("33b52de3", solve)
