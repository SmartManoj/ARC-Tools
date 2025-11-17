import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Find a blue (1) rectangle and map colored cells outside it to a 3x3 grid.
    The 3x3 output shows which regions (relative to the rectangle) contain colored cells.
    '''
    # Find the blue (1) rectangle boundaries
    blue_rows = []
    blue_cols = []
    for r in range(grid.height):
        for c in range(grid.width):
            if grid[r, c] == Color.BLUE:
                blue_rows.append(r)
                blue_cols.append(c)

    if not blue_rows:
        return Grid.empty(3, 3)

    min_r, max_r = min(blue_rows), max(blue_rows)
    min_c, max_c = min(blue_cols), max(blue_cols)

    # Find the color of cells (non-black, non-blue)
    target_color = None
    for r in range(grid.height):
        for c in range(grid.width):
            if grid[r, c] != Color.BLACK and grid[r, c] != Color.BLUE:
                target_color = grid[r, c]
                break
        if target_color:
            break

    if target_color is None:
        return Grid.empty(3, 3)

    # Create 3x3 output
    result = Grid.empty(3, 3)

    # Map colored cells to 3x3 regions
    for r in range(grid.height):
        for c in range(grid.width):
            if grid[r, c] == target_color:
                # Determine which region this cell belongs to
                out_r, out_c = 1, 1  # Default to center

                if r < min_r:
                    out_r = 0  # Top
                elif r > max_r:
                    out_r = 2  # Bottom

                if c < min_c:
                    out_c = 0  # Left
                elif c > max_c:
                    out_c = 2  # Right

                result[out_r, out_c] = target_color

    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("c8b7cc0f", solve)
