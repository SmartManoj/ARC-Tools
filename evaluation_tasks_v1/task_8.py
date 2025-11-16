import os
from arc_tools.grid import Grid
from arc_tools import logger
from helper import solve_task

def solve(grid: Grid):
    '''
    Connects pairs of same-colored markers with lines.

    Pattern:
    1. Find all pairs of markers with the same color
    2. If two markers of the same color are in the same row, draw a horizontal line between them
    3. If two markers of the same color are in the same column, draw a vertical line between them
    4. At intersections, vertical lines take precedence over horizontal lines

    Algorithm:
    - First, draw all horizontal lines
    - Then, draw all vertical lines (which will overwrite intersections)
    '''
    # Create a copy of the grid for output
    output_data = [list(row) for row in grid]

    # Find all colored markers (non-zero cells)
    markers = {}
    for r in range(grid.height):
        for c in range(grid.width):
            color = grid[r][c]
            if color != 0:
                if color not in markers:
                    markers[color] = []
                markers[color].append((r, c))

    # For each color, find pairs and draw lines
    # First pass: draw horizontal lines
    for color, positions in markers.items():
        if len(positions) == 2:
            r1, c1 = positions[0]
            r2, c2 = positions[1]

            # Check if they're in the same row (horizontal line)
            if r1 == r2:
                min_col = min(c1, c2)
                max_col = max(c1, c2)
                for c in range(min_col, max_col + 1):
                    output_data[r1][c] = color

    # Second pass: draw vertical lines (overwrites horizontal at intersections)
    for color, positions in markers.items():
        if len(positions) == 2:
            r1, c1 = positions[0]
            r2, c2 = positions[1]

            # Check if they're in the same column (vertical line)
            if c1 == c2:
                min_row = min(r1, r2)
                max_row = max(r1, r2)
                for r in range(min_row, max_row + 1):
                    output_data[r][c1] = color

    return Grid(output_data)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("070dd51e", solve)
