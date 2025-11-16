import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Pattern: Extract a shape (color 8) and tile it horizontally based on marker count (color 4)

    1. Find all positions with color 8 (the shape to replicate)
    2. Count positions with color 4 (markers indicating repetitions)
    3. Extract the bounding box of the shape
    4. Normalize shape to 3 rows (pad with 0s at top if needed)
    5. Tile the shape horizontally by the number of markers
    '''
    # Find all positions with color 8 (the shape)
    shape_positions = []
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] == 8:
                shape_positions.append((r, c))

    # Count markers (color 4)
    marker_count = 0
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] == 4:
                marker_count += 1

    # Find bounding box of shape
    min_r = min(pos[0] for pos in shape_positions)
    max_r = max(pos[0] for pos in shape_positions)
    min_c = min(pos[1] for pos in shape_positions)
    max_c = max(pos[1] for pos in shape_positions)

    # Extract shape
    shape_height = max_r - min_r + 1
    shape_width = max_c - min_c + 1

    shape = []
    for r in range(min_r, max_r + 1):
        row = []
        for c in range(min_c, max_c + 1):
            row.append(grid[r][c])
        shape.append(row)

    # Pad to 3 rows if needed (add rows of 0s at the top)
    while len(shape) < 3:
        shape.insert(0, [0] * shape_width)

    # Tile horizontally by marker count
    output_data = []
    for row in shape:
        output_row = row * marker_count
        output_data.append(output_row)

    return Grid(output_data)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("4852f2fa", solve)
