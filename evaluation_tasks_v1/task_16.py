import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Swaps colors in the grid based on a 2x2 color mapping in the top-left corner.

    Pattern:
    1. The top-left 2x2 corner remains unchanged
    2. For the rest of the grid, colors are swapped based on the 2x2 corner:
       - Color at [0,0] swaps with color at [0,1]
       - Color at [1,0] swaps with color at [1,1]
       - 0 (background) remains 0

    Example:
    If top-left 2x2 is:
    [[4, 2],
     [3, 7]]

    Then in the rest of the grid:
    - All 4's become 2's
    - All 2's become 4's
    - All 3's become 7's
    - All 7's become 3's
    '''
    # Extract the 2x2 color mapping from top-left corner
    c00 = grid[0][0]  # top-left
    c01 = grid[0][1]  # top-right
    c10 = grid[1][0]  # bottom-left
    c11 = grid[1][1]  # bottom-right

    # Create the color mapping
    color_map = {
        c00: c01,
        c01: c00,
        c10: c11,
        c11: c10,
        0: 0  # background stays background
    }

    # Create output grid
    output_data = []

    for r in range(grid.height):
        row = []
        for c in range(grid.width):
            # Keep the top-left 2x2 unchanged
            if r < 2 and c < 2:
                row.append(grid[r][c])
            else:
                # Apply color mapping
                original_color = grid[r][c]
                new_color = color_map.get(original_color, original_color)
                row.append(new_color)
        output_data.append(row)

    return Grid(output_data)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("0becf7df", solve)
