import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Transforms an NxN grid by:
    1. Tiling it 3x3 times (creating a 3N x 3N output)
    2. Adding red markers (color 2) as indicators:
       - For each row that contains a non-zero value at position j
       - Place a 2 at position (j-1) % width in the previous row (wrapping around)

    Pattern:
    - The input is repeated 3 times horizontally and 3 times vertically
    - Red markers are placed one position to the left and one row above each non-zero value
    - Positions and rows wrap around at boundaries
    '''
    height = len(grid)
    width = len(grid[0])

    # Create the base tiled grid (3x scaling)
    output_data = []
    for _ in range(3):  # Repeat 3 times vertically
        for row_idx in range(height):
            row = []
            for _ in range(3):  # Repeat 3 times horizontally
                row.extend(grid[row_idx])
            output_data.append(row)

    # Find non-zero positions in the original input
    markers = []
    for r in range(height):
        for c in range(width):
            if grid[r][c] != 0:
                # For a non-zero at (r, c), place marker at (r-1, c-1) with wrapping
                marker_row = (r - 1) % height
                marker_col = (c - 1) % width
                markers.append((marker_row, marker_col))

    # Place red markers (color 2) in all tiled copies
    for tile_r in range(3):
        for tile_c in range(3):
            for marker_row, marker_col in markers:
                # Calculate position in the output grid
                output_row = tile_r * height + marker_row
                output_col = tile_c * width + marker_col
                # Only place marker if current position is 0
                if output_data[output_row][output_col] == 0:
                    output_data[output_row][output_col] = 2

    return Grid(output_data)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("310f3251", solve)
