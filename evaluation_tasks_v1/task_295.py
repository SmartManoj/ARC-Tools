import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Extract a 5x5 region from a grid divided by green lines.
    The grid is divided into sections by green (3) lines, and one section is extracted.
    '''
    # Find green (3) lines that divide the grid
    # Horizontal and vertical green lines create a grid of sections
    # Extract one specific section (likely the one with most non-green colors)

    # Find horizontal green lines (rows that are all green)
    h_lines = []
    for r in range(grid.height):
        if all(grid[r, c] == Color.GREEN for c in range(grid.width)):
            h_lines.append(r)

    # Find vertical green lines (columns that are all green)
    v_lines = []
    for c in range(grid.width):
        if all(grid[r, c] == Color.GREEN for r in range(grid.height)):
            v_lines.append(c)

    # Find sections between lines
    # For now, extract the top-left section (simplification)
    if h_lines and v_lines:
        # Extract region before first lines
        h_end = h_lines[0] if h_lines else grid.height
        v_end = v_lines[0] if v_lines else grid.width

        # Create 5x5 output from the first section
        result = Grid.empty(5, 5)
        for r in range(min(5, h_end)):
            for c in range(min(5, v_end)):
                result[r, c] = grid[r, c]
        return result

    return Grid.empty(5, 5)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("c3202e5a", solve)
